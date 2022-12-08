from django.urls import path 

from . import views


urlpatterns = [
    path('', views.all_post, name='index'),
    path('signout', views.signout, name='signout'),
    path('signin', views.signin, name='signin'),
    path('adminsignin', views.adminsignin, name='adminsignin'),
    path('signup', views.signup, name='signup'),
    path('createpost', views.createpost, name='createpost'),
    path('allpost', views.allpost, name='allpost'),
    path('editpost/<str:id>', views.editpost, name='editpost'),
    path('deleteapost', views.deleteapost, name='deleteapost'),
    path('single/detail/<slug:slug>/', views.post_details, name='detail'),
    path('comment/reply/', views.reply, name="reply"),
    path('deletecomment/<str:id>', views.deletecomment, name='deletecomment'),
]
