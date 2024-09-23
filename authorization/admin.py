from django.contrib import admin
from .models import (
    CompanySubscriptions, 
    EngageModule, 
    HrModule, 
    ConnectModule, 
    TrainingModule, 
    UserSubscriptions,
    WebUserFactoryPermission
)


class HrModuleModuleAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date']
    search_fields = ('uuid',)


admin.site.register(HrModule, HrModuleModuleAdmin)


class ConnectModuleAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date']
    search_fields = ('uuid',)


admin.site.register(ConnectModule, ConnectModuleAdmin)


class TrainingModuleAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date']
    search_fields = ('uuid',)


admin.site.register(TrainingModule, TrainingModuleAdmin)


class EngageModuleAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date']
    search_fields = ('uuid',)


admin.site.register(EngageModule, EngageModuleAdmin)


class CompanySubscriptionsAdmin(admin.ModelAdmin):
    list_display = ['company_uuid', 'package_uuid', 'engage', 'hr', 'connect', 'training', 'on_boarding_date',
                    'expire_date']
    search_fields = ('company_uuid', 'package_uuid',)
    list_filter = ('engage', 'hr', 'connect', 'training',)


admin.site.register(CompanySubscriptions, CompanySubscriptionsAdmin)


class UserSubscriptionsAdmin(admin.ModelAdmin):
    list_display = ['administrator_uuid', 'user_group', 'company_subscription', 'engage', 'hr', 'connect', 'training']
    search_fields = ('administrator_uuid',)
    list_filter = ('user_group', 'company_subscription',)


admin.site.register(UserSubscriptions, UserSubscriptionsAdmin)


class WebUserFactoryPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'factory']
    search_fields = ('factory',)


admin.site.register(WebUserFactoryPermission, WebUserFactoryPermissionAdmin)
