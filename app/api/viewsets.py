from rest_framework import viewsets
from .serializers import userSerializers
from django.contrib.auth.models import User
from app.models import Post

 
class userviewsets(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = userSerializers