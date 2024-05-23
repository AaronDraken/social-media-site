from django.contrib import admin
from .models import Community,Post,Comment,Like,Chat,Follow,Notification,Profile,Online

# Register your models here.
class communityAdmin(admin.ModelAdmin):
    list_display=['id','name','category']
class postAdmin(admin.ModelAdmin):
    list_display=['id','user','community','file','caption','datetime','fileType']
class commentAdmin(admin.ModelAdmin):
    list_display=['id','post','comment']
class likeAdmin(admin.ModelAdmin):
    list_display=['user','post']
class chatAdmin(admin.ModelAdmin):
    list_display=['id','sender','reciever','message','datetime']
class followAdmin(admin.ModelAdmin):
    list_display=['user','follower','community','is_user']
class notificationAdmin(admin.ModelAdmin):
    list_display=['user1','user2','action','post','datetime','is_read']
class profileAdmin(admin.ModelAdmin):
    list_display=['user','bio','pfp']

admin.site.register(Community,communityAdmin)
admin.site.register(Post,postAdmin)
admin.site.register(Comment,commentAdmin)
admin.site.register(Like,likeAdmin)
admin.site.register(Chat,chatAdmin)
admin.site.register(Follow,followAdmin)
admin.site.register(Notification,notificationAdmin)
admin.site.register(Profile,profileAdmin)
admin.site.register(Online)