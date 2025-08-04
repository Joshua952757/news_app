from django import forms
from .models import Article, Newsletter, Publisher, Profile
from django.contrib.auth.models import User


class PublisherForm(forms.ModelForm):
    """Form for creating and updating Publisher objects."""
    class Meta:
        model = Publisher
        fields = ['name', 'content']


class ArticleForm(forms.ModelForm):
    """Form for creating and updating Article objects."""
    class Meta:
        model = Article
        fields = ['title', 'content', 'publisher']


class NewsletterForm(forms.ModelForm):
    """Form for creating and updating Newsletter objects."""
    class Meta:
        model = Newsletter
        fields = ['title', 'content', 'publisher']