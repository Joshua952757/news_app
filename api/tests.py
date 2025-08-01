# api/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from bronewsapp.models import Profile, Article, Publisher 

User = get_user_model()


class SubscribedJournalistArticlesAPITest(APITestCase):

    """Test for Journalist Articles, only subscribed."""
    
    def setUp(self):
        self.reader = User.objects.create_user(username='reader', password='pwd')
        self.journalist = User.objects.create_user(username='journalist', password='pwd')
        self.editor = User.objects.create_user(username='editor', password='pwd')
        self.other_journalist = User.objects.create_user(username='other_jrnlst', password='pwd')

        self.reader.profile.role = Profile.Role.READER
        self.reader.profile.save()

        self.journalist.profile.role = Profile.Role.JOURNALIST
        self.journalist.profile.save()
        
        self.editor.profile.role = Profile.Role.EDITOR
        self.editor.profile.save()

        self.other_journalist.profile.role = Profile.Role.JOURNALIST
        self.other_journalist.profile.save()

        pub = Publisher.objects.create(name='Simple Pub', admin=self.journalist)

        self.article_approved = Article.objects.create(
            title='Approved Article', content='Ok.', 
            author=self.journalist, publisher=pub, is_approved=True
        )
        self.article_unapproved = Article.objects.create(
            title='Unapproved Article', content='No.', 
            author=self.journalist, publisher=pub, is_approved=False
        )
        self.article_other_jrnlst = Article.objects.create(
            title='Other Jrnlst Article', content='.', 
            author=self.other_journalist, publisher=pub, is_approved=True
        )

        self.reader.profile.sub_journalist.add(self.journalist)

        self.url = reverse('api_subscribed_journalist_articles')

    def test_reader_gets_subscribed_articles(self):
        """Test reader gets articles from subscription"""
        self.client.force_authenticate(user=self.reader)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.article_approved.title)
        
        self.assertNotIn(self.article_unapproved.title, [a['title'] for a in response.data])
        self.assertNotIn(self.article_other_jrnlst.title, [a['title'] for a in response.data])

    def test_no_subscriptions_gets_empty_list(self):
        """Test no empty list in subscruortions"""
        self.reader.profile.sub_journalist.clear()
        self.client.force_authenticate(user=self.reader)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_non_reader_forbidden(self):
        "Testing if the non reader is forbidden access."
        self.client.force_authenticate(user=self.editor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_unauthorized(self):
        """testing unauthenticated and unauthorized."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)