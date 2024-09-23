import json
import datetime
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import get_object_or_404
from django.db.models import Q

from auth.settings import redis
from rest_framework import generics, viewsets, parsers, renderers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer

from .models import User
from .serializers import (
    UserListSerializer,
    VerifyTokenSerializer,
    UserVerifySerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    WorkerSerializer,
    AdminSerializer,
    AdminUpdateSerializer,
    WorkerUpdateSerializer,
    PasswordReGenerateSerializer,
    CodeGenerateByIDSerializer,
    VerifyCodeAndCreateAccessTokenSerializer,
    SetNewPasswordSerializer
)
from .validators import (
    phone_validate,
    email_validate,
    uuid_validate,
    inactive_validate
)
from .utils import (create_access_token, password_generator, code_generator, generate_access_key, get_user_by_username, decode_token)
from commons.enums import WEB, MOBILE
from auth.settings import OTP_EXPIRE_TIME, OTP_LENGTH, SET_PASSWORD_TIMEOUT


class BaseAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer


class JSONWebTokenWebAuth(BaseAuthToken):

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        return create_access_token(serializer, login_type=WEB)


class JSONWebTokenMobileAuth(BaseAuthToken):

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        return create_access_token(serializer, login_type=MOBILE)
        

class AdminsViews(viewsets.ModelViewSet):
    serializer_class = AdminSerializer
    user_type = WEB

    def get_queryset(self):
        queryset = User.objects.filter(
            is_deleted=False,
            user_type=self.user_type,
            is_superuser=False
        )
        return queryset

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        uuid = request.data.get('uuid', None)

        inactive_user = inactive_validate(uuid)
        if inactive_user:
            kwargs['uuid'] = inactive_user.uuid
            kwargs['post'] = True
            request.data['is_deleted'] = False
            return self.update(request, *args, **kwargs)

        serializer = AdminSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            instance = serializer.save(
                uuid=uuid,
                user_type=self.user_type
            )

            password = password_generator()
            instance.set_password(password)
            instance.save()

            return Response({'username': instance.email, 'password': password}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        user = get_object_or_404(User, is_deleted=False, uuid=kwargs.get('uuid'))
        serializer = UserListSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = None
        if kwargs.get('post'):
            user = get_object_or_404(User, is_deleted=True, uuid=kwargs.get('uuid'))
        else:
            user = get_object_or_404(User, is_deleted=False, uuid=kwargs.get('uuid'))

        serializer = AdminUpdateSerializer(instance=user, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(User, is_deleted=False, uuid=kwargs.get('uuid'))
        user.is_deleted = True
        user.save()
        return Response({'uuid': user.uuid}, status=status.HTTP_204_NO_CONTENT)


class WorkersView(viewsets.ModelViewSet):
    serializer_class = WorkerSerializer
    user_type = MOBILE

    def get_queryset(self):
        queryset = User.objects.filter(
            is_deleted=False,
            user_type=self.user_type,
            is_superuser=False
        )
        return queryset

    def create(self, request, *args, **kwargs):
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        uuid = request.data.get('uuid', None)

        inactive_user = inactive_validate(uuid)
        if inactive_user:
            kwargs['uuid'] = inactive_user.uuid
            kwargs['post'] = True
            request.data['is_deleted'] = False
            return self.update(request, *args, **kwargs)

        if email:
            username = email
        
        if phone:
            username = phone

        serializer = WorkerSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            instance = serializer.save(
                uuid=uuid,
                user_type=self.user_type
            )

            password = password_generator()
            instance.set_password(password)
            instance.save()

            return Response({'username': username, 'password': password}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        user = get_object_or_404(User, is_deleted=False, uuid=kwargs.get('uuid'))
        serializer = UserListSerializer(user, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = None
        if kwargs.get('post'):
            user = get_object_or_404(User, is_deleted=True, uuid=kwargs.get('uuid'))
        else:
            user = get_object_or_404(User, is_deleted=False, uuid=kwargs.get('uuid'))

        serializer = WorkerUpdateSerializer(instance=user, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(User, is_deleted=False, uuid=kwargs.get('uuid'))
        user.is_deleted = True
        user.last_login = None
        user.company_uuid = None
        user.save()
        return Response({'uuid': user.uuid}, status=status.HTTP_204_NO_CONTENT)


class TokenVerifyView(APIView):
    serializer_class = VerifyTokenSerializer

    def post(self, request):
        try:
            token = request.data['access_token']
        except KeyError:
            return Response({'error': 'Please give access token'}, status=status.HTTP_400_BAD_REQUEST)

        user = redis.get(token)
        if not user:
            return Response({'error': 'Please give valid access token'}, status=status.HTTP_400_BAD_REQUEST)
        user_object = json.loads(user.decode('utf-8'))
        return Response(user_object, status=status.HTTP_200_OK)


class LogoutView(APIView):
    serializer_class = VerifyTokenSerializer

    def post(self, request):
        token = request.data.get('access_token', "")
        redis.delete(token)
        return Response({'status': status.HTTP_200_OK, 'message': 'Successfully logout'}, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        try:
            user = User.objects.get(uuid=self.kwargs.get('uuid'))
            return user
        except User.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            return Response({'error': 'User Does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"error": "Password is Wrong"}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({"success": 'Password Successfully Changed'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordReGenerateView(generics.CreateAPIView):
    serializer_class = PasswordReGenerateSerializer

    def create(self, request, *args, **kwargs):
        serializer = PasswordReGenerateSerializer(data=request.data)
        if serializer.is_valid():
            user_uuid = serializer.data.get('user_uuid')
            user = get_object_or_404(User, uuid=user_uuid)
            new_password = password_generator()
            user.set_password(new_password)
            user.save()

            if user.email:
                username = user.email
            else:
                username = user.phone

            return Response({'username': username, 'password': new_password}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CodeGenerateByIDView(generics.CreateAPIView):
    serializer_class = CodeGenerateByIDSerializer

    def create(self, request, *args, **kwargs):
        serializer = CodeGenerateByIDSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('user_phone_or_email')
            user_type = serializer.data.get('user_type')

            user, response = get_user_by_username(username, user_type)
            if not user:
                return response

            code = code_generator(OTP_LENGTH)
            payload = {
                'code': code,
                'username': username,
                'user_type': user.user_type,
                'verified': False
            }
            payload = json.dumps(payload)
            redis.set(username, payload)
            redis.expire(username, OTP_EXPIRE_TIME)

            return Response({'secret_code': code}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeAndCreateAccessTokenView(generics.CreateAPIView):
    serializer_class = VerifyCodeAndCreateAccessTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = VerifyCodeAndCreateAccessTokenSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.data.get('secret_code')
            username = serializer.data.get('user_phone_or_email')
            
            redis_payload = redis.get(username)
            if not redis_payload:
                return Response({'error': 'Your secret code is expired. Please generate new one.'}, status=status.HTTP_408_REQUEST_TIMEOUT)

            payload_dict = json.loads(redis_payload)

            if code == payload_dict.get('code'):
                payload_dict['verified'] = True
                payload_dict['datetime'] = str(datetime.datetime.now())

                access_key = generate_access_key(username, payload_dict)

                payload = json.dumps(payload_dict)
                redis.set(access_key, payload)
                redis.expire(access_key, SET_PASSWORD_TIMEOUT)
                redis.delete(username)

                return Response({'access_key': access_key}, status=status.HTTP_200_OK)
            return Response({'error': 'Code not matched'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class SetNewPasswordView(generics.UpdateAPIView):
    serializer_class = SetNewPasswordSerializer

    def update(self, request, *args, **kwargs):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.data.get('password')
            access_key = serializer.data.get('access_key')

            redis_payload = redis.get(access_key)
            if not redis_payload:
                return Response({'error': 'Your access key is expired.'}, status=status.HTTP_408_REQUEST_TIMEOUT)

            payload_dict = json.loads(redis_payload)
            username = payload_dict.get('username')

            data = decode_token(access_key)
            data = data.get(username)

            user_type = data.get('user_type')

            user, response = get_user_by_username(username, user_type)
            if not user:
                return response
            
            user.set_password(password)
            user.save()

            redis.delete(access_key)

            return Response({'success': 'Successfully Password Changed'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

