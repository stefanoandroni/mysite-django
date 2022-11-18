from . import settings
from .forms import ArticleForm, CommentForm
from .models import Article, Comment, FrontPage
from .utils import HtmxOnlyMixin

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

# - - - - - - - - - - - - - - - - - - - - CBV (Class Based View) - - - - - - - - - - - - - - - - - - - - #

# - - - - - - - - - -
# Article CRUD  
# - - - - - - - - - -

# Create
class ArticleCreateView(LoginRequiredMixin, CreateView):
    context_object_name = 'article_obj'
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article-create.html' 

    def form_valid(self, form):
        # Set foreign keys before saving
        form.instance.author = self.request.user
        return super().form_valid(form)

# Retrieve (Detail)
class ArticleDetailView(LoginRequiredMixin, DetailView):
    context_object_name = 'article_obj'
    model = Article
    template_name = 'articles/article-detail.html' 

# Retrieve (List)
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'articles/article-list.html'
    paginate_by = settings.ARTICLES_PAGINATE_BY
    topic = None # ArticleTopicQuery
    query = None # String

    def get_template_names(self):
        if self.request.htmx:
            return 'articles/partials/article-list-elements.html'
        return 'articles/article-list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.topic is not None and self.query is not None: # True: if from search.search_view
            context['query'] = self.query
            context['topic'] = self.topic
        return context

# Update
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    context_object_name = 'article_obj'
    model = Article
    form_class = ArticleForm
    template_name = 'articles/article-update.html'

    def test_func(self):
        return self.request.user == self.get_object().author

# Delete
class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('profiles:home')
   
    def test_func(self):
        return self.request.user == self.get_object().author

# - - - - - - - - - -
# Comment CRUD    
# - - - - - - - - - -

# Create
class CommentCreateHxView(HtmxOnlyMixin, LoginRequiredMixin, CreateView):
    context_object_name = 'comment_obj'
    model = Comment
    form_class = CommentForm
        
    def get_success_url(self):
        return self.object.article.get_hx_comment_list_url()

    def form_valid(self, form):
        # Set foreign keys before saving
        parent_obj = get_object_or_404(Article, slug=self.kwargs.get('parent_slug'))
        form.instance.article = parent_obj
        form.instance.author = self.request.user
        return super().form_valid(form)

# Retrieve (Detail)   
class CommentDetailHxView(HtmxOnlyMixin, LoginRequiredMixin, DetailView):
    context_object_name = 'comment_obj'
    model = Comment
    pk_url_kwarg = 'id'
    template_name = 'articles/partials/comment-inline.html'    
        
class CommentBodyDetailHxView(CommentDetailHxView):
    template_name = 'articles/partials/comment-inline.html'

# Retrieve (List)
class CommentListHxView(HtmxOnlyMixin,LoginRequiredMixin, ListView):
    context_object_name = 'comment_list'
    model = Comment
    template_name = 'articles/partials/comment-list.html'  
    
    parent_obj = None # Article: Comments' parent (from kwargs)
    qs_all = False # Boolean: True if all comments are requested (from GET request's parameters) ?qs=all
    excess_comments = 0 # Int: number of comments that exceed the limit set in settings.NUMBER_OF_COMMENTS_DISPLAYED

    def setup(self, request, *args, **kwargs):
        self.parent_obj = get_object_or_404(Article, slug=kwargs.get('parent_slug'))
        self.qs_all = True if request.GET.get('qs') == "all" else False
        comments_count = self.parent_obj.get_comments().count()
        comments_excess = comments_count - settings.NUMBER_OF_COMMENTS_DISPLAYED
        self.excess_comments = (comments_excess) if comments_excess > 0 else 0
        return super().setup(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_obj'] = self.parent_obj
        context['comment_form'] = CommentForm()
        context['excess_comments'] = self.excess_comments
        context['qs_all'] = self.qs_all
        return context  

    def get_queryset(self, *args, **kwargs):
        if self.qs_all:
            qs = self.parent_obj.get_comments()
        else: 
            qs = self.parent_obj.get_comments_on_load() 
        return qs
     
# Update
class CommentUpdateHxView(HtmxOnlyMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    context_object_name = 'comment_obj'
    model = Comment
    form_class = CommentForm
    template_name = 'articles/partials/comment-update-form.html'
    pk_url_kwarg = 'id'
    
    def get_success_url(self):
        kwargs = {
            'parent_slug': self.object.article.slug,
            'id': self.object.id,
        }
        return reverse('articles:hx-comment-detail-body', kwargs=kwargs)

    def test_func(self):
        return self.request.user == self.get_object().author

# Delete
class CommentDeleteHxView(HtmxOnlyMixin, LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('articles:hx-comment-delete-response')

    def test_func(self):
        return self.request.user == self.get_object().author

# - - - - - - - - - -
# FrontPage    
# - - - - - - - - - -

# Retrieve
class ArticleHomeView(LoginRequiredMixin, TemplateView):
    context_object_name = 'front_page_obj'
    template_name = 'articles/article-front-page.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['front_page_obj'] = FrontPage.objects.get_current()
        return context

# - - - - - - - - - - - - - - - - - - - - FBV (Function Based View) - - - - - - - - - - - - - - - - - - - - #
# Note: no longer updated after switching to CBV

# def article_image_upload_view(request, parent_slug):
#     # print(request.GET)
#     # print(request.POST)
#     # print(parent_id)
#     # print(request.FILES.get('image'))
#     template_name = 'articles/upload-image.html'
#     if request.htmx:
#         template_name = 'articles/partials/upload-image-form.html'
#     try:
#         parent_obj = Article.objects.get(slug=parent_slug, author=request.user)
#     except:
#         parent_obj = None

#     if parent_obj is None:
#         raise Http404

#     form = ArticleImageForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         obj = form.save(commit=False)
#         # obj.recipe_id = parent_id # another way to set a related foreign key
#         obj.article = parent_obj
#         obj.save()

#     return render(request, template_name, {'form': form})

# @login_required
# def comment_create_hx_view(request, parent_slug=None):
#     if not request.htmx: 
#         raise Http404
#     try:
#         parent_obj = Article.objects.get(slug=parent_slug)
#     except:
#         parent_obj = None
#     try: # needed?
#         author = request.user
#     except:
#         author = None
#     if parent_obj is None or author is None:
#         return HttpResponse("Not Found")
#     form = CommentForm(request.POST or None)
#     context = {
#         'comment_form': form,
#         'article_obj': parent_obj
#     }
#     if form.is_valid():
#         new_comment = form.save(commit=False)
#         new_comment.article = parent_obj
#         new_comment.author = request.user # to check before if is not None?
#         new_comment.save()
#         context['comment_obj'] = new_comment
#         context['comment_form'] = CommentForm(None)
#         return render(request, 'articles/partials/comment-inline.html', context) 

#     return render(request, 'articles/partials/comment-form.html', context)  #!!

# @login_required
# def comment_detail_hx_view(request, id=None):
#     if not request.htmx: 
#         raise Http404
#     try:
#         obj = Comment.objects.get(id=id)
#     except:
#         obj = None
#     if obj is None:
#         return HttpResponse("Not Found") # ?
#     context = {
#         'comment_obj': obj
#     }
#     return render(request, 'articles/partials/comment-inline.html', context) 

# def article_comment_list_hx_view(request, article_slug=None):
#     if not request.htmx: 
#         raise Http404
#     try:
#         obj = Article.objects.get(slug=article_slug)
#     except:
#         obj = None
#     if obj is None:
#         return HttpResponse("Not Found")
#     context = {
#         'object': obj
#     }
#     return render(request, 'articles/partials/comment-list.html', context) 