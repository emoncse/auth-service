import jwt
import datetime
import json
import string
import secrets

from django.utils import timezone
from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response

from commons.enums import WEB, MOBILE
from commons.utils import get_logger
from auth.settings import redis, SECRET_KEY
from authorization.models import WebUserFactoryPermission

from .permission import get_permissions
from .models import User
from .internal_requests import organization_worker_info_update, get_worker_details

logger = get_logger()


def get_user_by_username(username, user_type):
    user = None

    try:
        user = User.objects.filter(is_deleted=False, user_type=user_type).get(Q(email=username) | Q(phone=username))
        return user, user
    except User.DoesNotExist:
        user = None
        return user, Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        user = None
        return user, Response({'error': '{}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)


def decode_token(encoded, algorithms='HS512'):
    data = jwt.decode(encoded, SECRET_KEY, algorithms=algorithms)
    return data


def generate_access_key(key, payload):
    access_key = jwt.encode({key: payload}, SECRET_KEY, algorithm='HS512')
    return access_key


def code_generator(otp_length=6):
    alphabet = string.digits
    code = ''.join(secrets.choice(alphabet) for i in range(otp_length))
    return code


def password_generator():
    alphabet = string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(4))
    return password


def update_last_login(user, login_type=MOBILE):
    if not user.last_login and login_type == MOBILE:
        try:
            organization_worker_info_update(worker_uuid=user.uuid, company_uuid=user.company_uuid)
        except Exception as e:
            logger.error("Unable to update joint_at field, error: {}".format(e))
            pass
        
    user.last_login = timezone.now()
    user.save()

    return user


def create_access_token(serializer, login_type=''):
    if serializer.is_valid():
        username = serializer.data.get('username')

        user, response = get_user_by_username(username, login_type)
        if not user:
            return Response({'error': 'Unauthorized User'}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'phone': user.phone,
            'email': user.email,
            'datetime': str(datetime.datetime.now()),
            'permissions': {}
        }

        token = jwt.encode(payload, SECRET_KEY)

        if login_type == MOBILE:
            user = update_last_login(user, login_type=MOBILE)
            worker = get_worker_details(user.uuid)

            if worker:
                payload['factory'] = worker.get('factory', [])
                payload['position'] = worker.get('position', [])
                payload['department'] = worker.get('department', [])

        if login_type == WEB:
            payload = get_permissions(payload, user)
            factories = WebUserFactoryPermission.objects.filter(
                is_deleted=False, 
                user=user
            ).values_list('factory', flat=True)
            payload['permissions']['factories'] = list(factories)

        payload['uuid'] = user.uuid
        payload['company_uuid'] = user.company_uuid
        payload['user_type'] = user.user_type

        try:
            redis.set(token, json.dumps(payload))
        except ConnectionError:
            pass
            logger.error('Redis server not connected')

        return Response({'access_token': token}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
