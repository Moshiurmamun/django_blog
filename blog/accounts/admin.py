from django.contrib import admin
from accounts.models import UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_info', 'city','website', 'phone')

    def user_info(self, obj):
        return obj.description

    def get_queryset(self, request):
        queryset = super(UserProfileAdmin, self).get_queryset(request)
        queryset = queryset.order_by('-phone', 'user') # here 'user' used for alphabetical oder ascending of the user names
        return queryset

    user_info.short_description = 'info' # here info override user_info (USER INFO now showed INFO)


admin.site.register(UserProfile, UserProfileAdmin)
