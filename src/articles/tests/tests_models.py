from PIL import Image

from ..models import Article, ArticleTopic, Comment, FrontPage
from ..settings import NUMBER_OF_COMMENTS_DISPLAYED, RATIO_HEIGHT, RATIO_WIDTH

from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()

class ArticleTestCase(TestCase):

    def setUp(self) -> None:
        self.number_of_articles = 3
        self.number_of_comments_article_a = 7
        self.number_of_comments_article_b = 3

        self.user_a = User.objects.create(username='user1', password='passworduser1')
        self.user_a_id = self.user_a.id

        self.article_a = Article.objects.create(
            author          = self.user_a,
            title           = "Title a",
            summary_text    = "Article a - summary_text", 
            content         = "Article a - content", 
            topic           = ArticleTopic.CHRONICLE
        )
        self.article_b = Article.objects.create(
            author          = self.user_a,
            title           = "Title b",
            summary_text    = "Article b - summary_text", 
            content         = "Article b - content", 
            topic           = ArticleTopic.CHRONICLE
        )
        self.article_c = Article.objects.create(
            author          = self.user_a,
            title           = "Title c",
            summary_text    = "Article c - summary_text", 
            content         = "Article c - content", 
            topic           = ArticleTopic.SPORT
        )

        for i in range(0,self.number_of_comments_article_a):
            Comment.objects.create(
                author      = self.user_a,
                article     = self.article_a,
                content     = "Comment content"
            )
        for i in range(0,self.number_of_comments_article_b):
            Comment.objects.create(
                author      = self.user_a,
                article     = self.article_b,
                content     = "Comment content"
            )

    def test_queryset_exists(self):
        qs = Article.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Article.objects.all()
        self.assertEqual(qs.count(), self.number_of_articles)

    def test_search_manager_query_only(self):
        # Author ['user1']
        qs = Article.objects.search(query='user1')
        self.assertEqual(qs.count(), 3)
        # Author ['user2']
        qs = Article.objects.search(query='user2')
        self.assertEqual(qs.count(), 0)
        # Title ['Title a']
        qs = Article.objects.search(query='Title a')
        self.assertEqual(qs.count(), 1)
        # Title ['Title']
        qs = Article.objects.search(query='Title')
        self.assertEqual(qs.count(), 3)
        # Content ['content']
        qs = Article.objects.search(query='content')
        self.assertEqual(qs.count(), 3)
        # Content ['qwerty']
        qs = Article.objects.search(query='qwerty')
        self.assertEqual(qs.count(), 0)

    def test_search_manager_none_query(self):
        # Empty string
        qs = Article.objects.search(query='')
        self.assertEqual(qs.count(), 0)
        # None
        qs = Article.objects.search(query=None)
        self.assertEqual(qs.count(), 0)

    def test_search_manager_query_only_case_insensitive(self):
        # Author ['uSEr1']
        qs = Article.objects.search(query='uSEr1')
        self.assertEqual(qs.count(), 3)
        # Author ['User2']
        qs = Article.objects.search(query='User2')
        self.assertEqual(qs.count(), 0)
        # Title ['Title A']
        qs = Article.objects.search(query='Title a')
        self.assertEqual(qs.count(), 1)
        # Title ['TITLE']
        qs = Article.objects.search(query='TITLE')
        self.assertEqual(qs.count(), 3)
        # Content ['Content']
        qs = Article.objects.search(query='Content')
        self.assertEqual(qs.count(), 3)
        # Content ['qWErty']
        qs = Article.objects.search(query='qWErty')
        self.assertEqual(qs.count(), 0)

    def test_search_manager_with_topic(self):
        # Topic [CHRONICLE]
        qs = Article.objects.search(query='Title', topic=ArticleTopic.CHRONICLE)
        self.assertEqual(qs.count(), 2)
        # Topic [SPORT]
        qs = Article.objects.search(query='Title', topic=ArticleTopic.SPORT)
        self.assertEqual(qs.count(), 1)
        # Topic [POLITICS]
        qs = Article.objects.search(query='Title', topic=ArticleTopic.POLITICS)
        self.assertEqual(qs.count(), 0) 
    
    def test_default_image(self):
        self.assertTrue(self.article_a.image is not None) # weak

    def test_uploaded_image_ratio(self):
        im = Image.open(self.article_a.image)
        width, height = im.size
        self.assertEqual(round(width/height,2), round(RATIO_WIDTH/RATIO_HEIGHT,2)) # precision (two decimals)

    def test_get_comments(self):
        # article_a
        qs = self.article_a.get_comments()
        self.assertEqual(qs.count(), self.number_of_comments_article_a)
        # article_b
        qs = self.article_b.get_comments()
        self.assertEqual(qs.count(), self.number_of_comments_article_b) 

    def test_get_number_of_comments(self):
        # article_a
        qs = self.article_a.get_number_of_comments()
        self.assertEqual(qs, self.number_of_comments_article_a)
        # article_b
        qs = self.article_b.get_number_of_comments()
        self.assertEqual(qs, self.number_of_comments_article_b) 

    def test_get_comments_on_load(self):
        # article_a
        article = self.article_a
        qs_load = article.get_comments_on_load().count()
        qs_all = article.get_number_of_comments()
        self.assertEqual(qs_load, NUMBER_OF_COMMENTS_DISPLAYED if qs_all>=NUMBER_OF_COMMENTS_DISPLAYED else qs_all)
        # article_b
        article = self.article_b
        qs_load = article.get_comments_on_load().count()
        qs_all = article.get_number_of_comments()
        self.assertEqual(qs_load, NUMBER_OF_COMMENTS_DISPLAYED if qs_all>=NUMBER_OF_COMMENTS_DISPLAYED else qs_all)


class CommentTestCase(TestCase):
    
    def setUp(self) -> None:
        self.number_of_comments_article_a = 10
        self.user_a = User.objects.create(username='user1', password='passworduser1')

        self.article_a = Article.objects.create(
            author          = self.user_a,
            title           = "Title a",
            summary_text    = "Article a - summary_text", 
            content         = "Article a - content", 
            topic           = ArticleTopic.CHRONICLE
        )

        for i in range(0,self.number_of_comments_article_a):
            Comment.objects.create(
                author      = self.user_a,
                article     = self.article_a,
                content     = "Comment content"
            )

    def test_queryset_exists(self):
        qs = Comment.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Comment.objects.all()
        self.assertEqual(qs.count(), self.number_of_comments_article_a)


class FrontPageTestCase(TestCase):
    
    def setUp(self) -> None:
        self.user_a = User.objects.create(username='user1', password='passworduser1')

        self.article_a = Article.objects.create(
            author          = self.user_a,
            title           = "Title a",
            summary_text    = "Article a - summary_text", 
            content         = "Article a - content", 
            topic           = ArticleTopic.CHRONICLE
        )
        
        self.fp1 = FrontPage.objects.create(
            active      = True,
            a0          = self.article_a,
            a1          = self.article_a,
            a2          = self.article_a,
            a3          = self.article_a,
            a4          = self.article_a,
            a5          = self.article_a,
            a6          = self.article_a,
            a7          = self.article_a,
            a8          = self.article_a
        )
        self.fp2 = FrontPage.objects.create(
            active      = False,
            a0          = self.article_a,
            a1          = self.article_a,
            a2          = self.article_a,
            a3          = self.article_a,
            a4          = self.article_a,
            a5          = self.article_a,
            a6          = self.article_a,
            a7          = self.article_a,
            a8          = self.article_a
        )

    def test_get_current(self):
        current_fp = FrontPage.objects.get_current()
        self.assertEqual(current_fp, self.fp1)
    
    def test_get_current_new_all_constraints(self):
        current_fp_before = FrontPage.objects.get_current()
        fp = FrontPage.objects.create(
            active      = True,
            a0          = self.article_a,
            a1          = self.article_a,
            a2          = self.article_a,
            a3          = self.article_a,
            a4          = self.article_a,
            a5          = self.article_a,
            a6          = self.article_a,
            a7          = self.article_a,
            a8          = self.article_a
        )
        current_fp_after = FrontPage.objects.get_current()
        self.assertEqual(current_fp_after, fp)
        self.assertNotEqual(current_fp_before, current_fp_after)

    def test_get_current_new_false_active_constraint(self):
        current_fp_before = FrontPage.objects.get_current()
        fp = FrontPage.objects.create(
            active      = False,
            a0          = self.article_a,
            a1          = self.article_a,
            a2          = self.article_a,
            a3          = self.article_a,
            a4          = self.article_a,
            a5          = self.article_a,
            a6          = self.article_a,
            a7          = self.article_a,
            a8          = self.article_a
        )
        current_fp_after = FrontPage.objects.get_current()
        self.assertEqual(current_fp_before, current_fp_after)

    def test_get_current_new_null_article_constraint(self):
        current_fp_before = FrontPage.objects.get_current()
        fp = FrontPage.objects.create(
            active      = True,
            a0          = None,
            a1          = self.article_a,
            a2          = self.article_a,
            a3          = self.article_a,
            a4          = self.article_a,
            a5          = self.article_a,
            a6          = self.article_a,
            a7          = self.article_a,
            a8          = self.article_a
        )
        current_fp_after = FrontPage.objects.get_current()
        self.assertNotEqual(current_fp_before, current_fp_after)
        self.assertEqual(current_fp_after, None)
