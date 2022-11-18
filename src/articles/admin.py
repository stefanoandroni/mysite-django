from .models import Article, Comment, FrontPage

from django.contrib import admin

class ArticleAdmin(admin.ModelAdmin):
    list_display    = ('id', 'title', 'topic', 'slug', 'timestamp', 'updated')
    search_fields   = ('title', 'content', 'slug', 'author__username')
    readonly_fields = ('timestamp', 'updated')
    raw_id_fields   = ('author',)

class CommentAdmin(admin.ModelAdmin):
    list_display    = ('id', 'author', 'article', 'article_id', 'timestamp', 'updated')
    search_fields   = ('content', 'author__username', 'article__title')
    readonly_fields = ('timestamp', 'updated')
    raw_id_fields   = ('author', 'article')

class FrontPageAdmin(admin.ModelAdmin):
    list_display    = ('id', 'active', 'timestamp')
    readonly_fields = ('timestamp',)
    raw_id_fields   = ('a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FrontPage, FrontPageAdmin)

