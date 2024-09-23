from rest_framework import serializers
import datetime

from authentication.serializers import UserListSerializer
from .models import (
    EngageModule,
    HrModule,
    ConnectModule,
    TrainingModule,
    CompanySubscriptions,
    UserSubscriptions,
    UserGroup,
    WebUserFactoryPermission
)
from .utils import validate_uuid4


# Create your serializers here.
class EngageModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EngageModule
        read_only_fields = ('id', 'uuid')
        fields = (
            'id',
            'uuid',
            'company_uuid',
            'start_date',
            'end_date'
        )


class HrModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HrModule
        read_only_fields = ('id', 'uuid')
        fields = (
            'id',
            'uuid',
            'company_uuid',
            'start_date',
            'end_date'
        )


class ConnectModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectModule
        read_only_fields = ('id', 'uuid')
        fields = (
            'id',
            'uuid',
            'company_uuid',
            'start_date',
            'end_date'
        )


class TrainingModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingModule
        read_only_fields = ('id', 'uuid')
        fields = (
            'id',
            'uuid',
            'company_uuid',
            'start_date',
            'end_date'
        )


class CompanySubscriptionsModuleSerializer(serializers.ModelSerializer):
    package_uuid = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_uuid4]
    )
    company_uuid = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_uuid4]
    )

    class Meta:
        model = CompanySubscriptions
        fields = (
            'uuid',
            'package_uuid',
            'company_uuid',
            'engage',
            'hr',
            'connect',
            'training',
            'expire_date'
        )
        extra_kwargs = {
            'uuid': {'read_only': True}
        }


class CompanySubscriptionsUpdateModuleSerializer(serializers.ModelSerializer):
    engage = serializers.BooleanField()
    hr = serializers.BooleanField()
    connect = serializers.BooleanField()
    training = serializers.BooleanField()

    class Meta:
        model = CompanySubscriptions
        fields = (
            'uuid',
            'package_uuid',
            'company_uuid',
            'engage',
            'hr',
            'connect',
            'training',
            'expire_date'
        )
        extra_kwargs = {
            'uuid': {'read_only': True}
        }

    def update(self, instance, validated_data):
        """
        Overriding the default update method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record

        """
        module_results_dict = {}
        modules = {
            "hr": HrModule,
            "connect": ConnectModule,
            "training": TrainingModule,
            "engage": EngageModule
        }
        for module_name, value in validated_data.items():
            if module_name in modules.keys():
                if value:
                    module_results_dict[module_name], _ = modules[module_name].objects.update_or_create(
                        company_uuid=instance.company_uuid,
                        defaults={"start_date": datetime.datetime.now()}
                    )
                else:
                    module_results_dict[module_name] = None

        user_subscriptions = instance.user_company_subscription.all()
        primary_user_subscription = UserSubscriptions.objects.get(company_subscription_id__exact=instance.id,
                                                                  user_group__name__iexact="primary_admin")
        instance.engage = primary_user_subscription.engage = module_results_dict["engage"]
        instance.hr = primary_user_subscription.hr = module_results_dict["hr"]
        instance.connect = primary_user_subscription.connect = module_results_dict["connect"]
        instance.training = primary_user_subscription.training = module_results_dict["training"]

        instance.save(update_fields=['hr', 'connect', 'training', 'engage'])
        primary_user_subscription.save(update_fields=['hr', 'connect', 'training', 'engage'])
        for module_key in module_results_dict.copy():
            if module_results_dict[module_key]:
                module_results_dict.pop(module_key)
        if module_results_dict:
            user_subscriptions.update(**module_results_dict)
        return instance


class CompanySubscriptionsDetailModuleSerializer(serializers.ModelSerializer):
    engage = EngageModuleSerializer()
    hr = HrModuleSerializer()
    training = TrainingModuleSerializer()
    connect = ConnectModuleSerializer()

    package_uuid = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_uuid4]
    )
    company_uuid = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_uuid4]
    )

    class Meta:
        model = CompanySubscriptions
        fields = (
            'id',
            'uuid',
            'package_uuid',
            'company_uuid',
            'engage',
            'hr',
            'connect',
            'training',
            'expire_date',
            'on_boarding_date'
        )
        extra_kwargs = {
            'uuid': {'read_only': True},
            'id': {'read_only': True}
        }


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        read_only_fields = ('id', 'uuid')
        fields = (
            'id',
            'uuid',
            'name'
        )


class UserSubscriptionsModuleSerializer(serializers.ModelSerializer):
    administrator_uuid = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_uuid4]
    )
    company_uuid = serializers.CharField(
        max_length=150,
        required=True,
        validators=[validate_uuid4]
    )
    user_group = serializers.CharField(
        max_length=20,
        required=True
    )

    class Meta:
        model = UserSubscriptions
        read_only_fields = ('id', 'uuid', 'company_subscription')
        fields = (
            'uuid',
            'company_subscription',
            'administrator_uuid',
            'company_uuid',
            'user_group',
            'engage',
            'hr',
            'connect',
            'training'
        )

    def create(self, validated_data):
        """
        Overriding the default create method of the Model serializer.
        :param validated_data: data containing all the details of student
        :return: returns a successfully created student record
        """
        company_uuid = validated_data.pop('company_uuid')
        user_group_name = validated_data.pop('user_group')
        company_subscription = CompanySubscriptions.objects.get(company_uuid=company_uuid)
        user_group, _ = UserGroup.objects.get_or_create(name=user_group_name)
        user_subscription = UserSubscriptions.objects.create(company_subscription=company_subscription,
                                                             user_group=user_group,
                                                             **validated_data)
        return user_subscription


class UserSubscriptionsDetailModuleSerializer(serializers.ModelSerializer):
    engage = EngageModuleSerializer()
    hr = HrModuleSerializer()
    training = TrainingModuleSerializer()
    connect = ConnectModuleSerializer()
    company_subscription = CompanySubscriptionsDetailModuleSerializer()
    user_group = UserGroupSerializer()

    class Meta:
        model = UserSubscriptions
        fields = (
            'id',
            'uuid',
            'company_subscription',
            'administrator_uuid',
            'user_group',
            'engage',
            'hr',
            'connect',
            'training'
        )

        read_only_fields = ('id', 'uuid',)


class UserSubscriptionsUpdateModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSubscriptions
        read_only_fields = ('id', 'uuid', 'company_subscription', 'administrator_uuid')
        fields = (
            'id',
            'uuid',
            'company_subscription',
            'administrator_uuid',
            'user_group',
            'engage',
            'hr',
            'connect',
            'training'
        )


class FactoryPermissionSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(format='hex_verbose')
    permission = serializers.BooleanField(required=True)


class WebUserFactoryPermissionPostSerializer(serializers.Serializer):
    factory_permissions = serializers.ListField(
        child=FactoryPermissionSerializer()
    )


class WebUserFactoryPermissionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = WebUserFactoryPermission
        fields = [
            'uuid',
            'user',
            'factory'
        ]
        read_only_fields = ('uuid',)


class WebUserFactoryPermissionDetailsSerializer(serializers.ModelSerializer):
    user = UserListSerializer(read_only=True)

    class Meta:
        model = WebUserFactoryPermission
        fields = [
            'uuid',
            'user',
            'factory'
        ]
        read_only_fields = ('uuid',)
