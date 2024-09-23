from django.contrib import admin
from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'company_uuid', 'phone', 'email', 'user_type', 'last_login', 'date_joined', ]
    search_fields = ('uuid', 'company_uuid', 'phone', 'email')
    list_filter = ('groups', 'is_active', 'is_superuser')


admin.site.register(User, UserAdmin)
