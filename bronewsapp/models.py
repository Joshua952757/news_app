from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile


class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    admin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="managed_publishers",
        limit_choices_to={'profile__role': "ADMIN"}
    )
    content = models.TextField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Model for an article.
    """
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'profile__role': "JOURNALIST"}
    )
    content = models.TextField(null=True, blank=True, default=None)
    
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    """
    Model for a newsletter.
    """
    title = models.CharField(max_length=255)

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'profile__role': "JOURNALIST"}
    )
    content = models.TextField(null=True, blank=True, default=None)

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    