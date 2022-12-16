from django.contrib import admin
from app.models import LikePost, Post, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(Comment)


