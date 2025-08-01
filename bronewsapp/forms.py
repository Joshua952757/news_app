from django import forms
from .models import Article, Newsletter, Publisher, Profile
from django.contrib.auth.models import User


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'content']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']
        
    
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'publisher']