from django.contrib import admin

# Register your models here.
from models import *
admin.site.register(SCUser)
admin.site.register(Post)
#admin.site.register(Pubblication)
admin.site.register(Like)
admin.site.register(Cat)