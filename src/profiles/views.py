from .utils import HtmxOnlyMixin
from articles.models import Article, Comment

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, TemplateView

# - - - - - - - - - - - - - - - - - - - - CBV (Class Based View) - - - - - - - - - - - - - - - - - - - - #

class ProfileHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tot_comments'] = Comment.objects.filter(author=self.request.user).count()
        context['tot_articles'] = Article.objects.filter(author=self.request.user).count()
        context['tot_comments_recived'] = Comment.objects.filter(article__author=self.request.user).count()
        return context

class ArticleListHxView(HtmxOnlyMixin, LoginRequiredMixin, ListView):
    context_object_name = 'article_list'
    model = Article
    template_name = 'profiles/partials/article-table.html'

    def get_queryset(self, *args, **kwargs):
        qs = Article.objects.filter(author=self.request.user)
        return qs

class CommentListHxView(HtmxOnlyMixin, LoginRequiredMixin, ListView):
    context_object_name = 'comment_list'
    model = Comment
    template_name = 'profiles/partials/comment-table.html'

    def get_queryset(self, *args, **kwargs):
        qs = Comment.objects.filter(author=self.request.user)
        return qs