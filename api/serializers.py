from rest_framework import serializers
from bronewsapp.models import Article


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'publisher', 'is_approved'] 