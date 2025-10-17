from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'tweetapp'

urlpatterns = [
    path('', views.listtweet, name='listtweet'),#domanin.com/tweetapp
    path('addtweet/', views.addtweet, name='addtweet'),#domanin.com/tweetapp/listtweet
    path('addtweetbyform',views.addtweetbyform, name="addtweetbyform"),
    path('addtweetbymodelform',views.addtweetbymodelform, name="addtweetbymodelform"),
    path('signup/',views.SignUpView.as_view(), name="signup"),
    path('deletetweet/<int:id>',views.deletetweet, name="deletetweet")
]
 