from django.urls import path
from . import views
# from .views import createPost

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/<str:categ>', views.explore, name='explore'),
    path('popular/', views.popular, name='popular'),
    path('chats/', views.chat, name='chats'),
    path('search/', views.search, name='search'),
    path('chatDisp/<str:rec>', views.chatDisp, name='chatDisp'),
    path('msgSend/<str:rec>', views.msgSend, name='msgSend'),
    path('notifications/', views.notif, name='notifications'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    path('register/', views.userReg, name='register'),
    path('profile/<str:username>', views.viewProfile, name='profile'),
    path('updateProfile/', views.updateProfile, name='updateProfile'),
    path('community/<str:name>', views.viewCommunity, name='community'),
    path('createPost/', views.createPost, name='createPost'),
    path('comments/<str:pk>', views.comments, name='comments'),
    path('likes/<str:pk>', views.likes, name='likes'),
    path('follow/<str:username>', views.follow, name='follow'),
    path('followCommunity/<str:name>', views.followComm, name='followCommunity'),
]
