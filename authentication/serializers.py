from django.contrib.auth.models import Group
from .models import User
from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from commons.enums import WEB, MOBILE
from .validators import required, phone_validate, email_validate
from auth.settings import OTP_LENGTH


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
            'uuid',
            'phone',
            'email',
            'company_uuid',
            'user_type'
        ]
        read_only_fields = ['uuid']


class WorkerSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(max_length=150, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True, validators=[UniqueValidator(queryset=User.objects.filter(user_type=MOBILE, is_deleted=False))])
    phone = serializers.CharField(required=False, allow_null=True, allow_blank=True, validators=[UniqueValidator(queryset=User.objects.filter(user_type=MOBILE, is_deleted=False))])
    company_uuid = serializers.UUIDField(validators=[required])

    class Meta:
        model = User
        fields = [
            'uuid',
            'phone',
            'email',
            'company_uuid',
            'user_type',
            'is_deleted'
        ]
        read_only_fields = ['user_type', 'is_deleted']


    def validate(self, data):
        phone = data.get('phone', None)
        email = data.get('email', None)
        if not email and not phone:
            raise serializers.ValidationError('Please give email or phone')
        return data


class WorkerUpdateSerializer(WorkerSerializer):
    uuid = serializers.CharField(read_only=True)
    is_deleted = serializers.BooleanField(required=False)
    company_uuid = serializers.UUIDField()


class AdminSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField(max_length=150, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.filter(user_type=WEB, is_deleted=False))])
    phone = serializers.CharField(required=False, allow_null=True, allow_blank=True, validators=[UniqueValidator(queryset=User.objects.filter(user_type=WEB, is_deleted=False))])
    company_uuid = serializers.UUIDField(validators=[required])
    
    class Meta:
        model = User
        fields = [
            'uuid',
            'phone',
            'email',
            'company_uuid',
            'user_type',
            'is_deleted'
        ]
        read_only_fields = ['user_type', 'is_deleted']


class AdminUpdateSerializer(AdminSerializer):
    uuid = serializers.CharField(read_only=True)
    is_deleted = serializers.BooleanField(required=False)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'uuid',
            'phone',
            'email',
            'company_uuid',
            'user_type',
            'is_deleted'
        ]


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')


class VerifyTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)

    class Meta:
        fields = [
            'access_token'
        ]


class AuthorizeSerializer(serializers.Serializer):
    engage = serializers.BooleanField()
    hr = serializers.BooleanField()
    connect = serializers.BooleanField()
    training = serializers.BooleanField()


class UserVerifySerializer(serializers.ModelSerializer):
    authorize = AuthorizeSerializer()

    class Meta:
        model = User
        fields = [
            'id',
            'uuid',
            'phone',
            'email',
            'company_uuid',
            'user_type',
            'authorize'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        fields = [
            'old_password',
            'new_password'
        ]


class PasswordReGenerateSerializer(serializers.Serializer):
    user_uuid = serializers.UUIDField(required=True, allow_null=False)


class CodeGenerateByIDSerializer(serializers.Serializer):
    user_phone_or_email = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    user_type = serializers.CharField(required=True, allow_blank=False, allow_null=False)


class VerifyCodeAndCreateAccessTokenSerializer(serializers.Serializer):
    secret_code = serializers.CharField(required=True, allow_blank=False, allow_null=False, max_length=OTP_LENGTH, min_length=OTP_LENGTH)
    user_phone_or_email = serializers.CharField(required=True, allow_blank=False, allow_null=False)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    access_key = serializers.CharField(required=True, allow_blank=False, allow_null=False)

