from django.contrib.auth import get_user_model
from .models import User
from django.db.models import Q
from commons.enums import WEB, MOBILE


class WebAuthBackend(object):
    """
    Custom auth Backend for Web User to perform authentication via phone or email
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        my_user_model = get_user_model()
        try:
            user = User.objects.filter(is_deleted=False, user_type=WEB).get(Q(uuid=username) | Q(email=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except:
            return None

    def get_user(self, uuid):
        my_user_model = get_user_model()
        try:
            user = User.objects.get(pk=uuid)
            return user
        except User.DoesNotExist:
            return None


class MobileAuthBackend(object):
    """
    Custom auth Backend for Web User to perform authentication via phone or email
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        my_user_model = get_user_model()
        try:
            user = User.objects.filter(is_deleted=False, user_type=MOBILE).get(Q(uuid=username) | Q(email=username) | Q(phone=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except:
            return None

    def get_user(self, uuid):
        my_user_model = get_user_model()
        try:
            user = User.objects.get(pk=uuid)
            return user
        except User.DoesNotExist:
            return None

