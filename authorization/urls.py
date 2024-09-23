from .views import (
    CompanySubscriptionView,
    CompanySubscriptionDetailByCompanyUuidView,
    EngageModuleView,
    HrModuleView,
    ConnectModuleView,
    TrainingModuleView,
    UserSubscriptionListView,
    UserSubscriptionDetailsView,
    UserGroupView,
    WebUserFactoryPermissionView
)
from django.urls import path

module_list = {
    'get': 'list',
    'post': 'create'
}

module_detail = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
}

urlpatterns = [
    path('engage', EngageModuleView.as_view(module_list), name='engage-list'),
    path('engage/<uuid>', EngageModuleView.as_view(module_detail), name='engage-details'),
    path('hr', HrModuleView.as_view(module_list), name='hr-list'),
    path('hr/<uuid>', HrModuleView.as_view(module_detail), name='hr-details'),
    path('connect', ConnectModuleView.as_view(module_list), name='connect-list'),
    path('connect/<uuid>', ConnectModuleView.as_view(module_detail), name='connect-details'),
    path('training', TrainingModuleView.as_view(module_list), name='training-list'),
    path('training/<uuid>', TrainingModuleView.as_view(module_detail), name='training-details'),
    path('subscriptions', CompanySubscriptionView.as_view(module_list), name='company-subscription-list'),
    path('subscriptions/subscription', CompanySubscriptionDetailByCompanyUuidView.as_view(module_detail),
         name='company-subscription-detail-by-company-uuid'),
    path('subscriptions/<company_uuid>', CompanySubscriptionView.as_view(module_detail),
         name='company-subscription-detail'),
    path('user-subscriptions', UserSubscriptionListView.as_view(module_list), name='user-subscription-list'),
    path('user-subscriptions/<administrator_uuid>', UserSubscriptionDetailsView.as_view(module_detail),
         name='user-subscription-details'),
    path('user-groups', UserGroupView.as_view(module_list), name='user-group-list'),
    path('user-groups/<uuid>', UserGroupView.as_view(module_detail), name='user-group-details'),
    path('user/factories', WebUserFactoryPermissionView.as_view(module_list), name='user-factories'),
    path('user/factories/<admin_uuid>', WebUserFactoryPermissionView.as_view(module_detail), name='user-factoy')
]
