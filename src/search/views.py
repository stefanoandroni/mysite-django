from .utils import HtmxOnlyMixin
from .settings import NUMBER_OF_ARTICLES_DISPLAYED
from articles.models import Article, ArticleTopicQuery
from articles.views import ArticleListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView
from django.shortcuts import render

# - - - - - - - - - - - - - - - - - - - - CBV (Class Based View) - - - - - - - - - - - - - - - - - - - - #

class LoadSearchHxView(HtmxOnlyMixin, LoginRequiredMixin, TemplateView):
    template_name = 'search/search-form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_topic_list'] = ArticleTopicQuery
        return context  

# to implement search_view CB

# - - - - - - - - - - - - - - - - - - - - FBV (Function Based View) - - - - - - - - - - - - - - - - - - - - #

def search_view(request):
    if not request.user.is_authenticated:
        return Http404
    query = request.GET.get('q')
    query_topic = request.GET.get('topic')
    if query_topic not in ArticleTopicQuery: # or none
        query_topic = ArticleTopicQuery.ALL
    query_topic = ArticleTopicQuery(query_topic)
    if request.htmx:
        context = {
            'article_topic_list': ArticleTopicQuery,
            'selected_topic': query_topic,
        }
        if query == None or len(query) == 0:
            return HttpResponse()
    qs = Article.objects.search(query, topic=query_topic)
    if request.htmx:
        context['queryset'] = qs[:NUMBER_OF_ARTICLES_DISPLAYED]
        template = "search/partials/results.html"  
        return render(request, template, context)
    return ArticleListView.as_view(queryset = qs, topic=query_topic, query=query)(request)

# def load_search_hx_view(request): # TemplateView
#     if not request.htmx: 
#         raise Http404
#     context = {
#         'article_topic_list': ArticleTopicQuery,
#     }
#     return render(request, "search/search-form.html", context)
