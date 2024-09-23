import django_filters
from .models import UserSubscriptions


class UserSubscriptionFilter(django_filters.FilterSet):
    company_uuid = django_filters.UUIDFilter(field_name="company_subscription__company_uuid")

    class Meta:
        model = UserSubscriptions
        fields = ['administrator_uuid', 'user_group__uuid', 'engage__uuid', 'hr__uuid', 'connect__uuid',
                  'training__uuid']
