from django.contrib import admin
from .models import Thread, Comment
from mptt.admin import MPTTModelAdmin

admin.site.register(Thread)
admin.site.register(Comment, MPTTModelAdmin)
