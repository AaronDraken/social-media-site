from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Community(models.Model):
    name=models.CharField(max_length=255,unique=True)
    categ_list=[('Games','Games'),('News','News'),('Entertainment','Entertainment')]
    category=models.CharField(max_length=255, choices=categ_list)
    img=models.FileField(upload_to='media',default='defaultCom.png')

class Post(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    community=models.ForeignKey(Community, on_delete=models.CASCADE)
    file=models.FileField(upload_to='media',blank=True,null=True)
    caption=models.CharField(max_length=255)
    datetime=models.DateTimeField(auto_now_add=True)
    type_list=[('Video','Video'),('Image','Image'),('None','None')]
    fileType=models.CharField(max_length=255,choices=type_list)
    likesCount=models.IntegerField(default=0)
    commentsCount=models.IntegerField(default=0)

class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    comment=models.CharField(max_length=255)

class Follow(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user',blank=True,null=True)
    follower=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_follower')
    community=models.ForeignKey(Community, on_delete=models.CASCADE, blank=True,null=True)
    is_user=models.BooleanField(default=True)

class Like(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)

class Chat(models.Model):
    sender=models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    reciever=models.ForeignKey(User, on_delete=models.CASCADE, related_name='reciever')
    message=models.CharField(max_length=255)
    datetime=models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    pfp=models.FileField(upload_to='media',default='media/default.jpg')
    bio=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.user.username 

class Notification(models.Model):
    user1=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_1') #sender
    user2=models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_2') #reciever
    profile=models.ForeignKey(Profile, on_delete=models.CASCADE)
    action_list=[('Like','Like'),('Comment','Comment'),('Follow','Follow')]
    action=models.CharField(max_length=255,choices=action_list)
    post=models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    datetime=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

class Online(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    online=models.BooleanField(default=False)