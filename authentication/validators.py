from .models import User
from uuid import UUID


def phone_validate(phone, user_type):
    try:
        User.objects.get(phone=phone, is_deleted=False, user_type=user_type)
        exist = False
    except User.DoesNotExist:
        exist = True
    except User.MultipleObjectsReturned:
        exist = False
    return exist


def email_validate(email, user_type):
    try:
        User.objects.get(email=email, is_deleted=False, user_type=user_type)
        exist = False
    except User.DoesNotExist:
        exist = True
    except User.MultipleObjectsReturned:
        exist = False
    return exist


def uuid_validate(uuid):
    try:
        uuid = UUID(uuid, version=4)
    except ValueError:
        return False

    try:
        User.objects.get(is_deleted=False, uuid=uuid)
        exist = False
    except User.DoesNotExist:
        exist = True
    except User.MultipleObjectsReturned:
        exist = False
    return exist


def inactive_validate(uuid):
    try:
        exist = User.objects.get(is_deleted=True, uuid=uuid)
    except User.DoesNotExist:
        exist = False
    except User.MultipleObjectsReturned:
        exist = False

    return exist
        

def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')
