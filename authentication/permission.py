from rest_framework import permissions
from authorization.models import UserSubscriptions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


def get_permissions(payload, user):
    subscription = UserSubscriptions.objects.filter(
        company_subscription__company_uuid=user.company_uuid,
        administrator_uuid=user.uuid
    )

    engage, connect, training, hr = False, False, False, False

    if subscription.exists():
        engage = subscription.filter(engage__isnull=False).exists()
        connect = subscription.filter(connect__isnull=False).exists()
        training = subscription.filter(training__isnull=False).exists()
        hr = subscription.filter(hr__isnull=False).exists()

    payload['authorize'] = {
        'engage': engage,
        'connect': connect,
        'training': training,
        'hr': hr
    }
    payload['user_group'] = subscription.first().user_group.name
    return payload
