from django.contrib import admin
from .models import UserProfile, PickUpRequest


class PickUpRequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PickUpRequest._meta.fields]
    class Meta:
        model = PickUpRequest

class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields]
    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PickUpRequest, PickUpRequestAdmin)
