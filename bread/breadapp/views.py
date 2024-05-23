from django.shortcuts import render,redirect
from .models import Post,Comment,Community,Like,Follow,Notification,Chat,Profile,Online
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.core.mail import send_mail
from datetime import datetime

# Create your views here.
def home(req):
    user=req.user
    if user.is_authenticated:
        following=Follow.objects.filter(follower=user,is_user=True)
        followingComms=Follow.objects.filter(follower=user,is_user=False)
        pfp=Profile.objects.get(user=user)
        notifCount=Notification.objects.filter(user2=user,is_read=False).count()
        postsList=[]
        posts=Post.objects.none()
        for x in following:
            postsIterate=Post.objects.filter(user=x.user)
            postsList.append(postsIterate)
        for x in followingComms:
            postsIterate=Post.objects.filter(community=x.community)
            postsList.append(postsIterate)
        for x in postsList:
            posts=(posts | x).order_by('-datetime')
        context={'post':posts,'pfp':pfp,'notifCount':notifCount}
        return render(req,'index.html',context)
    else:
        posts=Post.objects.all().order_by('-datetime')
        context={'post':posts}
        return render(req,'index.html',context)

def explore(req,categ):
    if categ == 'All':
        posts=Post.objects.all().order_by('-datetime')
    else:
        comms=Community.objects.filter(category=categ)
        posts=Post.objects.none()
        postsList=[]
        for x in comms:
            postsIterate=Post.objects.filter(community=x)
            postsList.append(postsIterate)
        for x in postsList:
            posts=(posts | x).order_by('-datetime')
    user=req.user
    if user.is_authenticated:
        notifCount=Notification.objects.filter(user2=user,is_read=False).count()
        pfp=Profile.objects.get(user=req.user)
        context={'post':posts,'pfp':pfp,'notifCount':notifCount}
    else:
        context={'post':posts}
    return render(req,'index.html',context)

def popular(req):
    posts=Post.objects.all().order_by('-likesCount')
    user=req.user
    if user.is_authenticated:
        notifCount=Notification.objects.filter(user2=user,is_read=False).count()
        pfp=Profile.objects.get(user=req.user)
        context={'post':posts,'pfp':pfp,'notifCount':notifCount}
    else:
        context={'post':posts}
    return render(req,'index.html',context)

def chat(req):
    user=req.user
    if user.is_authenticated:
        followers=Follow.objects.filter(user=user,is_user=True)
        pfp=Profile.objects.get(user=user)
        notifCount=Notification.objects.filter(user2=user,is_read=False).count()
        onlineCheck=Online.objects.filter()
        res=[]
        for x in followers:
            pfp2=Profile.objects.get(user=x.follower)
            res.append(pfp2) 
        context={'followers':followers,'pfp':pfp,'notifCount':notifCount,'online':onlineCheck,'pfp2':res}
        return render(req,'chat.html',context)
    else:
        messages.error(req,"Login to access Messaging Feature.")
        return redirect('/login')

def chatDisp(req,rec):
    # followers list
    followers=Follow.objects.filter(user=req.user,is_user=True)
    pfp=Profile.objects.get(user=req.user)
    notifCount=Notification.objects.filter(user2=req.user,is_read=False).count()
    # chatbox
    user=req.user
    reciever=User.objects.get(username=rec)
    disp=Profile.objects.get(user=reciever)
    to_send=User.objects.filter(username=rec)
    msg1=Chat.objects.filter(sender=user,reciever=reciever).order_by('datetime')
    msg2=Chat.objects.filter(sender=reciever,reciever=user).order_by('datetime')
    msg=(msg1 | msg2)

    onlineCheck=Online.objects.filter()
    res=[]
    for x in followers:
        pfp2=Profile.objects.get(user=x.follower)
        res.append(pfp2) 

    context={'msg':msg,"reciever":to_send,'followers':followers,'pfp':pfp,'disp':disp,'notifCount':notifCount,'online':onlineCheck,'pfp2':res}
    return render(req,'chat.html',context)

def msgSend(req,rec):
    msg=req.POST['msg']
    user=User.objects.get(username=req.user)

    reciever=User.objects.get(username=rec)

    Chat.objects.create(sender=user,reciever=reciever,message=msg)
    return redirect('/chatDisp/'+rec)

def createPost(req):
    user=req.user
    if user.is_authenticated:
        notifCount=Notification.objects.filter(user2=user,is_read=False).count()
        if req.method=='GET':
            community=Community.objects.all()
            pfp=Profile.objects.get(user=user)
            return render(req,'post.html',{'community':community,'pfp':pfp,'notifCount':notifCount})
        else:
            try:
                community=Community.objects.get(name=req.POST['community'])
                caption=req.POST['caption']
                fileType=req.POST['fileType']
                if fileType == 'None':
                    Post.objects.create(user=user,community=community,caption=caption,fileType=fileType)
                else:
                    file=req.FILES['file']
                    Post.objects.create(user=user,community=community,caption=caption,file=file,fileType=fileType)
                messages.success(req,'Post Created Successfully')
                return redirect('/')
            except:
                messages.error(req,'Please Enter the data correctly and fill all fields.')
                return redirect('/createPost')
    else:
        messages.error(req,'You need to Login to post.')
        return redirect('/login')

def notif(req):
    user=req.user
    if user.is_authenticated:
        notifs=Notification.objects.all().order_by('-datetime').filter(user2=user)
        pfp=Profile.objects.get(user=user)
        context={'notif':notifs,'pfp':pfp}
        Notification.objects.filter(user2=user).update(is_read=True)
        return render(req,'notif.html',context)
    else:
        messages.error(req,'Login to access your notifications.')
        return redirect('/')

def userLogin(req):
    try:
        if req.method=='GET':
            return render(req,'login.html')
        else:
            username = req.POST["username"]
            password = req.POST["password"]
            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                new=Online.objects.create(user=req.user,online=True)
                print(new)
                # Mail sending
                send_mail(
                "User Logged in Successfully",
                "New login detected in ur account at "+datetime.now().strftime("%c"),
                "",#sender mail
                [""], #reciever mail
                fail_silently=False,
                )

                messages.success(req,"Logged In Successfully. Welcome!")
                return redirect('/')
            else:
                messages.error(req,"Username/Password is incorrect. Please Try again.")
                return render(req,'login.html')
    except:
            messages.error(req,'Something went wrong. Try again')
            return render(req,'login.html')

def userLogout(req):
    try:
        Online.objects.get(user=req.user).delete()
        logout(req)
        messages.success(req,'You have logged out. See you soon!')
        return redirect('/')
    except:
        messages.error(req,'Something went wrong. Try again')
        return redirect('/')

def userReg(req):
    if req.method=='GET':
        return render(req,'register.html')
    else:
        username=req.POST['username']
        fname=req.POST['fname']
        lname=req.POST['lname']
        email=req.POST['email']
        password=req.POST['password']
        password2=req.POST['password2']

        if password==password2:
            if validate_password(password) == None:
                try:
                    User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=password)
                    messages.success(req,'Account Created Successfully.')
                    check=User.objects.get(username=username)
                    Profile.objects.create(user=check)
                    return redirect('/login')
                except:
                    messages.error(req,'Please check to make sure all details as added correctly.')
                    return render(req,'register.html')
            else:
                messages.error(req,'Your password can’t be too similar to your other personal information. Your password must contain at least 8 characters. Your password can’t be a commonly used password. Your password can’t be entirely numeric. Try Again')
                return render(req,'register.html')
        else:
            messages.error(req,'Password and confirm password do not match. Try again')
            return render(req,'register.html')

def viewProfile(req,username):
    u=req.user
    user=User.objects.get(username=username)
    followers=Follow.objects.filter(user=user).count()
    following=Follow.objects.filter(follower=user).count()
    posts=Post.objects.filter(user=user).order_by('-datetime')
    profile=Profile.objects.get(user=user.id)
    if u.is_authenticated:
        notifCount=Notification.objects.filter(user2=user,is_read=False).count()
        pfp=Profile.objects.get(user=u)
        if user == req.user:
            context={'viewUser':user,'followersCount':followers,'followingCount':following,'post':posts,'is_user':False,'profile':profile,'pfp':pfp,'notifCount':notifCount}
        else:
            is_following=Follow.objects.filter(user=user,follower=req.user)
            if is_following:
                context={'viewUser':user,'followersCount':followers,'followingCount':following,'post':posts,'is_user':True,'is_following':True,'profile':profile,'pfp':pfp,'notifCount':notifCount}
            else:
                context={'viewUser':user,'followersCount':followers,'followingCount':following,'post':posts,'is_user':True,'is_following':False,'profile':profile,'pfp':pfp,'notifCount':notifCount}
    else:
        context={'viewUser':user,'followersCount':followers,'followingCount':following,'post':posts,'profile':profile}
    return render(req,'viewProfile.html',context)

def updateProfile(req):
    if req.method == 'GET':
        profile=Profile.objects.get(user=req.user)
        pfp=Profile.objects.get(user=req.user)
        notifCount=Notification.objects.filter(user2=req.user,is_read=False).count()
        return render(req,"editProfile.html",{'profile':profile,'pfp':pfp,'notifCount':notifCount})
    else:
        try:
            prof=Profile.objects.get(user=req.user)
            prof.bio=req.POST['bio']
            prof.pfp=req.FILES['pfp']
            prof.save()
            return redirect('/profile/'+ req.user.username)
        except:
            messages.error(req,'Something Went Wrong. Try again')
            return redirect('/updateProfile')

def viewCommunity(req,name):
    u=req.user
    comm=Community.objects.get(name=name)
    followers=Follow.objects.filter(community=comm).count()
    posts=Post.objects.filter(community=comm).order_by('-datetime')
    if u.is_authenticated:
        notifCount=Notification.objects.filter(user2=u,is_read=False).count()
        pfp=Profile.objects.get(user=u)
        is_following=Follow.objects.filter(community=comm,follower=req.user)
        if is_following:
            context={'community':comm,'post':posts,'followersCount':followers,'is_following':True,'pfp':pfp,'notifCount':notifCount}
        else:
            context={'community':comm,'post':posts,'followersCount':followers,'is_following':False,'pfp':pfp,'notifCount':notifCount}
        return render(req,'viewCommunity.html',context)
    else:
        context={'community':comm,'post':posts,'followersCount':followers,'is_following':False}
    return render(req,'viewCommunity.html',context)

def search(req):
    user=req.user
    if req.method == 'POST':
        query=req.POST.get('search')
        res=User.objects.filter(Q(username__icontains = query)|Q(first_name__icontains = query)|Q(last_name__icontains = query))
        res2=Community.objects.filter(Q(name__icontains = query)|Q(category__icontains = query))
        proflist=[]
        for x in res:
            profile=Profile.objects.filter(user=x.id)
            print(profile)
            proflist.append(profile)
        print(proflist)
        if user.is_authenticated:
            notifCount=Notification.objects.filter(user2=user,is_read=False).count()
            pfp=Profile.objects.get(user=user)
            return render(req,'search.html',{'users':res,'community':res2,'profile':proflist,'pfp':pfp,'notifCount':notifCount})
        else:
            return render(req,'search.html',{'users':res,'community':res2,'profile':proflist})
    
def comments(req,pk):
    if req.method == 'GET':
        comments=Comment.objects.filter(post=pk)
        user=req.user
        if user.is_authenticated:
            notifCount=Notification.objects.filter(user2=user,is_read=False).count()
            pfp=Profile.objects.get(user=user)
            return render(req,'comments.html',{'comments':comments,'pk':pk,'pfp':pfp,'notifCount':notifCount})
        else:
            return render(req,'comments.html',{'comments':comments,'pk':pk})
    else:
        user=req.user
        if user.is_authenticated:
            post=Post.objects.get(id=pk)
            profile=Profile.objects.get(user=req.user)
            Comment.objects.create(post=post,user=req.user,comment=req.POST['comment'])
            post.commentsCount+=1
            post.save()
            Notification.objects.create(user1=user,user2=post.user,profile=profile,action='Comment',post=post)
            return redirect('/comments/'+pk)
        else:
            messages.error(req,'Login to be able to comment on post.')
            return redirect('/login')

def likes(req,pk):
    post=Post.objects.get(id=pk)
    user=req.user
    if user.is_authenticated:
        like=Like.objects.filter(user=user,post=post)
        if like:
            like.delete()
            Notification.objects.get(user1=user,user2=post.user,action='Like',post=post).delete()
            post.likesCount-=1
            post.save()
        else:
            newlike=Like.objects.create(user=user,post=post)
            newlike.save()
            profile=Profile.objects.get(user=req.user)
            Notification.objects.create(user1=user,user2=post.user,profile=profile,action='Like',post=post)
            post.likesCount+=1
            post.save()            
        return redirect('/')
    else:
        messages.error(req,'Login to like a post')
        return redirect('/')

def follow(req,username):
    user=req.user
    usercheck=User.objects.get(username=username)
    if user.is_authenticated:
        followcheck=Follow.objects.filter(user=usercheck,follower=user)
        if followcheck:
            followcheck.delete()
            Notification.objects.get(user1=user,user2=usercheck,action='Follow').delete()
            messages.success(req,'Unfollowed Successfully')
        else:
            Follow.objects.create(user=usercheck,follower=req.user)
            profile=Profile.objects.get(user=user.id)
            Notification.objects.create(user1=user,user2=usercheck,profile=profile,action='Follow')
            messages.success(req,'Followed Successfully')
        return redirect('/profile/'+ username)
    else:
        messages.error(req,'Login to Follow users')
        return redirect('/login')

def followComm(req,name):
    user=req.user
    comm=Community.objects.get(name=name)
    if user.is_authenticated:
        followcheck=Follow.objects.filter(community=comm,follower=user)
        if followcheck:
            followcheck.delete()
            messages.success(req,'Unfollowed Successfully')
        else:
            Follow.objects.create(community=comm,follower=user,is_user=False)
            messages.success(req,'Followed Successfully')
        return redirect('/community/'+ name)
    else:
        messages.error(req,'Login to Follow Community')
        return redirect('/login')