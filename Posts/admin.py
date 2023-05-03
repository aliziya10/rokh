from django.contrib import admin
from .models import Tag,Comments
from django.db import models


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag',)

admin.site.register(Tag, TagsAdmin)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_id','user_id','text','parent_id')

admin.site.register(Comments, CommentAdmin)