from django.contrib import admin

# Register your models here.
from models import *


class SCUserAdmin(admin.ModelAdmin):
	list_display = ('username','first_name', 'last_name','birth_date','is_superuser')
	list_filter = ['date_joined']
	search_fields = ['username','first_name','last_name']

class PostAdmin (admin.ModelAdmin):
    list_display = ('id','content','post_date','post_type')
    list_filter = ['post_date','post_type']
    search_fields = ['id','post_type']

class LikeAdmin(admin.ModelAdmin):
    list_display = ('id','like_date','like_user','like_post')
    list_filter = ['like_date']

admin.site.register(SCUser, SCUserAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Like,LikeAdmin)
admin.site.register(ChatRoom)
admin.site.register(Crono_chat)
