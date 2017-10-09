from django.contrib import admin
from .models import UserProfile, PickUpRequest

def delete_model(modeladmin, request, queryset):
    for obj in queryset:
        user_profile = obj.user.profile
        if user_profile.user_points >= obj.points:
            user_profile.user_points -= obj.points
            user_profile.save()
        obj.delete()

delete_model.short_description = "Удалить как исполненный"

class PickUpRequestAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PickUpRequest._meta.fields]
    actions = [delete_model]
    class Meta:
        model = PickUpRequest

class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields]
    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PickUpRequest, PickUpRequestAdmin)
