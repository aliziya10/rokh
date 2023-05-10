from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# from Posts.models import Post
from .models import *
# from Accounts.models import TicketAnswer

admin.site.register(Slides)

admin.site.register(Menu)

class TeamAdmin(admin.ModelAdmin):
    list_display = ("id","label","link")

admin.site.register(Teammate,TeamAdmin)

admin.site.register(RokhInfo)


# admin.site.register(TicketAnswer)


class PostAdmin(admin.ModelAdmin):

    def Tags(self, obj):
        return ", ".join([str(p) for p in obj.tags.all()])
    list_display = ("id","title","author","dateOfPublish")


# admin.site.register(Post,PostAdmin)