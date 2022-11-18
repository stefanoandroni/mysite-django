"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from .views import ArticleCreateView, ArticleDetailView, ArticleDeleteView, ArticleHomeView, ArticleUpdateView, ArticleListView, CommentCreateHxView, CommentListHxView, CommentUpdateHxView, CommentDetailHxView, CommentDeleteHxView, CommentBodyDetailHxView

from django.urls import include, path
from django.views.generic.base import TemplateView

app_name = 'articles'

urlpatterns = [
    path('', ArticleHomeView.as_view(), name='home'),
    path('create/', ArticleCreateView.as_view(), name='article-create'),
    path('list/', ArticleListView.as_view(), name='article-list'),
    path('search/', include('search.urls', namespace='search')),
    path('<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
    path('<slug:slug>/update/', ArticleUpdateView.as_view(), name='article-update'),
    path('<slug:slug>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    
    path('hx/comment-delete-response/', TemplateView.as_view(template_name='articles/partials/comment-inline-delete-response.html'), name='hx-comment-delete-response'),
    path('hx/<slug:parent_slug>/comment/', CommentListHxView.as_view(), name='hx-comment-list'),
    path('hx/<slug:parent_slug>/comment/<int:id>/delete/', CommentDeleteHxView.as_view(), name='hx-comment-delete'), # parent_slug not used 
    path('hx/<slug:parent_slug>/comment/<int:id>/update/', CommentUpdateHxView.as_view(), name='hx-comment-update'), # parent_slug not used 
    path('hx/<slug:parent_slug>/comment/<int:id>/update-response/', CommentBodyDetailHxView.as_view(), name='hx-comment-detail-body'), # parent_slug not used
    path('hx/<slug:parent_slug>/comment/<int:id>/', CommentDetailHxView.as_view(), name='hx-comment-detail'), # parent_slug not used 
    path('hx/<slug:parent_slug>/comment/create/', CommentCreateHxView.as_view(), name='hx-comment-create'), 
] 



