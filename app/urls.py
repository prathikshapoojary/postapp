from django.urls import path
from . import views
app_name = "polls"

urlpatterns = [
    path('',views.home, name='home'),
    path('post/', views.postlist, name='postlist'),
    path('<int:post_id>/like/', views.like, name='like'),
    path('<int:post_id>/comment/', views.comment, name='comment'),
    path('logout/', views.logout_user, name='logout'),
]
