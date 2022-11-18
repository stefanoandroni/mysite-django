from autoslug import AutoSlugField

from . import settings as app_settings
from .utils import make_thumbnail

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.urls import reverse

# - - - - - - - - - - - - - - - - - - - - User - - - - - - - - - - - - - - - - - - - - #

User = settings.AUTH_USER_MODEL

# - - - - - - - - - - - - - - - - - - - Article - - - - - - - - - - - - - - - - - - - - #

class ArticleTopic(models.TextChoices):
    CHRONICLE   = "c", "Chronicle"
    POLITICS    = "p", "Politics"
    SPORT       = "s", "Sport"
    ECONOMY     = "e", "Economy"

class ArticleTopicQuery(models.TextChoices): # bad (inheritance? no / or hardcode const 'All')
    ALL         = "a", "All"
    CHRONICLE   = "c", "Chronicle"
    POLITICS    = "p", "Politics"
    SPORT       = "s", "Sport"
    ECONOMY     = "e", "Economy"

# Article Custom Query Manager
class ArticleQuerySet(models.QuerySet):
    def search(self, query=None, topic=ArticleTopicQuery.ALL): # (?) improve the management of topic subquerying
        if query is None or query == "":
            return self.none()
        # if topic not in ArticleTopicQuery:
        #     return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)
        if topic != ArticleTopicQuery.ALL:
            lookups &= Q(topic=topic)
        return self.filter(lookups)

# Article Custom Model Manager
class ArticleManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self.db)

    def search(self, query=None, *args, **kwargs):
        return self.get_queryset().search(query=query, *args, **kwargs)

class Article(models.Model):
    author          = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title           = models.CharField(max_length=120) 
    summary_text    = models.TextField(max_length=220) 
    content         = models.TextField()
    topic           = models.CharField(max_length=1, choices=ArticleTopic.choices, default=ArticleTopic.CHRONICLE)
    image           = models.ImageField(upload_to='articles/', default="articles/default/article_image.png") # is the default image allocation correct? (No?) 

    timestamp       = models.DateTimeField(auto_now_add=True)
    updated         = models.DateTimeField(auto_now=True)

    slug            = AutoSlugField(populate_from='title', unique=True) # 3rd package: django-autoslug

    objects         = ArticleManager() 

    class Meta:
        ordering = ["-timestamp"]

    def save(self, *args, **kwargs):
        self.image = make_thumbnail(self.image) # Crop uploaded image
        super().save(*args, **kwargs)
    
    @property
    def name(self):
        return self.title
    
    @property
    def user(self):
        return self.author

    def __str__(self):
        return f"Article [{self.title}] ({self.author})"

    def get_absolute_url(self):
        kwargs = {
            "slug": self.slug  
        }
        return reverse("articles:article-detail", kwargs=kwargs)
    
    def get_edit_url(self):
        kwargs = {
            "slug": self.slug  
        }
        return reverse("articles:article-update", kwargs=kwargs)
    
    def get_delete_url(self):
        kwargs = {
            "slug": self.slug  
        }
        return reverse("articles:article-delete", kwargs=kwargs)

    def get_hx_comment_list_url(self):
        kwargs = {
            "parent_slug": self.slug  
        }
        return reverse('articles:hx-comment-list', kwargs=kwargs)
    
    def get_hx_comment_create_url(self):
        kwargs = {
            "parent_slug": self.slug  
        }
        return reverse('articles:hx-comment-create', kwargs=kwargs)

    def get_comments(self):
        qs = self.comment_set.all().order_by('-timestamp')
        return qs

    def get_comments_on_load(self): 
        return self.get_comments()[:app_settings.NUMBER_OF_COMMENTS_DISPLAYED]

    def get_number_of_comments(self): # here?
        # return self.get_comments().count()
        return self.comment_set.all().count()

# - - - - - - - - - - - - - - - - - - - Comment - - - - - - - - - - - - - - - - - - - - #

class Comment(models.Model):
    author      = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    article     = models.ForeignKey(Article, on_delete=models.CASCADE)
    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-timestamp"]
        
    def __str__(self):
        return f"Comment [{self.id}]"
    
    def get_absolute_url(self):
        kwargs = {
            "id": self.id,
            "parent_slug": self.article.slug
        }
        return reverse("articles:hx-comment-detail", kwargs=kwargs)
    
    def get_hx_url(self):
        kwargs = {
            "id": self.id,
            "parent_slug": self.article.slug
        }
        return reverse('articles:hx-comment-detail', kwargs=kwargs)

    def get_hx_edit_url(self):
        kwargs = {
            "id": self.id,
            "parent_slug": self.article.slug
        }
        return reverse('articles:hx-comment-update', kwargs=kwargs)
    
    def get_hx_delete_url(self):
        kwargs = {
            "id": self.id,
            "parent_slug": self.article.slug
        }
        return reverse('articles:hx-comment-delete', kwargs=kwargs)

# - - - - - - - - - - - - - - - - - - - FrontPage - - - - - - - - - - - - - - - - - - - - #

# FrontPage Custom Query Manager
class FrontPageQuerySet(models.QuerySet):
    def get_current(self):
        # current front page = the most recent front page among the active ones
        obj = self.filter(active=True).order_by('-timestamp').first()
        if obj is not None:
            if None not in [obj.a0, obj.a1, obj.a2, obj.a3, obj.a4, obj.a5, obj.a6, obj.a7, obj.a8]:
                return obj
        return None 

# FrontPage Custom Model Manager
class FrontPageManager(models.Manager):
    def get_queryset(self):
        return FrontPageQuerySet(self.model, using=self.db)

    def get_current(self):
        return self.get_queryset().get_current()

class FrontPage(models.Model): # bad model
    active      = models.BooleanField(default=False)
    timestamp   = models.DateTimeField(auto_now_add=True)
    a0          = models.ForeignKey(Article, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    a1          = models.ForeignKey(Article, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    a2          = models.ForeignKey(Article, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    a3          = models.ForeignKey(Article, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    a4          = models.ForeignKey(Article, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    a5          = models.ForeignKey(Article, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    a6          = models.ForeignKey(Article, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    a7          = models.ForeignKey(Article, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    a8          = models.ForeignKey(Article, related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    
    objects     = FrontPageManager()
    # method set_active() to make all others not active

    def __str__(self):
        return f"FrontPage [{self.id}]"