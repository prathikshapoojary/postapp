from rest_framework import serializers
from app.models import Post, LikePost, Comment
from django.contrib.auth.models import User

class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']
     
class CommentSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = Comment
        fields =  '__all__' 

class PostSerializers(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField('get_comment')

    def get_comment(self,instance):
        c1=Comment.objects.filter(post=instance)
        
        return CommentSerializers(c1,many=True).data
    class Meta:
        model = Post
        # fields =  '__all__' 
        fields =  ['url','id','user','title','type_of_media','media','description','created_at','likes','comment']
        
class LikePostSerializers(serializers.ModelSerializer):
 
    class Meta:
        model = LikePost
        fields =  '__all__' 
        

        
# class PostSerializers(serializers.ModelSerializer):
#     comment = serializers.SerializerMethodField('get_comment')
    
#     def get_comment(self,instance):         
#         q1=Comment.objects.filter(id=instance)
#         return CommentSerializers(q1, many=True).data


#     class Meta:
#         model=Post
#         fields = ['id','comment']
   