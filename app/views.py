from ctypes import sizeof
import os
import codecs
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from app.models import Post
from base64 import decodestring
from .models import LikePost, Post, Comment
from django.contrib.auth import authenticate, login, logout
import base64
import codecs
import io
from .form import UploadFileForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.paginator import Paginator
from .serializers import PostSerializers
from rest_framework.response import Response
# Create your views here.
 
def post_detail(request, pk):
    try:
        post_cm = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer =PostSerializers(post_cm)
    return JsonResponse(serializer.data)


def home(request):
    return render(request,'login.html')

@login_required()
@csrf_exempt
def postlist(request):
   

    try:
        # p = Paginator(Post.objects.all(),2)
        # page = request.GET.get('page')
        # posts_p = p.get_page(page)

        data = Post.objects.all()
        comment_data = Comment.objects.all()
        form = UploadFileForm(request.POST)
        current_user = request.user
        
        if request.method == "POST":
            if form.data.get('delete_comment_id') != None:
                comment_id = form.data['delete_comment_id']
                Comment.objects.filter(id=comment_id,user_id=request.user.id).delete()
            elif form.data.get('type_of_media') != None:
                title = form.data['title']
                type_of_media = dict(form.fields['type_of_media'].choices)[form.data['type_of_media']]
                if type_of_media == "Video" or type_of_media == "Image":
                    file = request.FILES['post_file']
                    post =Post.objects.create(user_id=request.user.id,title=title,type_of_media=form.data['type_of_media'], media=file.read(),description=form.data['description'] )
                    post.save()
                else:
                    post_content = bytes(form.data['post_content'],"utf-8")
                    post = Post.objects.create(user_id=request.user.id,title=title,type_of_media=form.data['type_of_media'], media=post_content,description=form.data['description'] )
                    post.save()
            elif form.data.get('delete_post_id') != None:
                post_id = form.data['delete_post_id']
                Post.objects.filter(id=post_id,user_id=request.user.id).delete()
            else:
                post_id = form.data['post_id']
                is_liked = LikePost.objects.filter(user= User.objects.filter(id=current_user.id ).first(),post=Post.objects.filter(id=post_id).first()).count() > 0
                if not is_liked:
                    like = LikePost.objects.create(user= User.objects.filter(id=current_user.id ).first(),post=Post.objects.filter(id=post_id).first())
                    like.save()
                else:
                    LikePost.objects.filter(user= User.objects.filter(id=current_user.id ).first(),post=Post.objects.filter(id=post_id).first()).delete()
        
            if form.data.get('post_comment') != None:
                post_id = form.data['post_id']
                post_comment = form.data['post_comment']
                comment = Comment.objects.create(user_id=request.user.id,post_id=post_id,text=post_comment)

        

        for index in range(len(data)):
            data[index].likes = LikePost.objects.filter(post = Post.objects.filter(id=data[index].id).first()).count()
            data[index].is_liked = LikePost.objects.filter(post = Post.objects.filter(id=data[index].id).first(),user= User.objects.filter(id=current_user.id ).first()).count() > 0
            data[index].comments = Comment.objects.filter(post = Post.objects.filter(id=data[index].id).first()).prefetch_related()
            data[index].user_can_delete = data[index].user == current_user
            
            if data[index].type_of_media == '3':
                textdata = data[index].media
                data[index].base64 =  textdata.decode("utf-8")
                data[index].media = data[index].base64
            else:
                if data[index].type_of_media == '1':
                    data[index].base64 = "data:image/jpeg;base64,"+base64.b64encode(data[index].media).decode('utf-8');
                elif data[index].type_of_media == '2':
                    data[index].base64 = "data:video/mp4;base64,"+base64.b64encode(data[index].media).decode('utf-8');
        return render (request, 'postlist.html',{'post_data':data,'form':form,'comment_data':comment_data,'current_user': current_user,'posts_p':posts_p})
    except Exception as e:
        return redirect('/project/post/')
    

def logout_user(request):
    logout(request)
    return redirect('login')

def like(request):
    return 0

def comment(request):
    return 0
