from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts import models

User = get_user_model()


# Register your models here.

class LoginLogAdmin(admin.ModelAdmin):
    list_filter = ("suspicious", "successful", "created_at")
    search_fields = ("email", "reject_reason")


admin.site.register(User)
admin.site.register(models.LoginLog, LoginLogAdmin)
