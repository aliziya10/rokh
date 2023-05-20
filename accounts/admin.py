from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
# Register your models here.
# admin.site.register(User)
admin.site.register(Profile)

class Usera(UserAdmin):
    def passwords(self,obj):
        a=str(User.objects.values_list("password").get(id=obj.id)[0])
        # if a=="" or a is None:
        #     return
        return a



    list_display = ("id","username","phone","email","passwords")
    # readonly_fields = ('password',)
    fieldsets = (
            ("Specifications", {"fields": ("username","phone","password","email")}),
            ("Permissions", {"fields": ("groups","user_permissions","is_staff", "is_active","is_superuser",'is_doctor')}),
    )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide', 'extrapretty'),
    #         'fields': ('name', 'password1', 'password2',"email","groups", "is_staff", "is_active", "is_superuser"),
    #
    #     }),
    # )
    add_fieldsets = (
        ("Specifications", {"fields": ("username","phone","password1","password2", "email")}),
        ("Permissions", {"fields": ("groups", 'user_permissions',"is_staff", "is_active", "is_superuser",'is_doctor')}),
    )
    # radio_fields = {"group": admin.VERTICAL}

    ordering = ("id",)


admin.site.register(User,Usera)

admin.site.register(Expertise)