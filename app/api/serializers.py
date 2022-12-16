
from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Post

 
class userSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = Post
        fields =  '__all__'