from django.urls import path
from .views import subscribed_journalist_articles_api

urlpatterns = [
    path("sub-articles/", subscribed_journalist_articles_api, name='api_subscribed_journalist_articles'),
]