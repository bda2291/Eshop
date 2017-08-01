from django.contrib import admin
from .models import UserProfile, PickUpRequest


class PickUpRequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PickUpRequest._meta.fields]
    class Meta:
        model = PickUpRequest

admin.site.register(UserProfile)
admin.site.register(PickUpRequest, PickUpRequestAdmin)
