from django.contrib import admin
from .models import Publisher, Article, Newsletter

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Article)
admin.site.register(Newsletter)