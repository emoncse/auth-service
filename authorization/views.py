from rest_framework import viewsets, status
from rest_framework.response import Response
from authentication.models import User
from .serializers import (
    CompanySubscriptionsModuleSerializer,
    CompanySubscriptionsDetailModuleSerializer,
    CompanySubscriptionsUpdateModuleSerializer,
    EngageModuleSerializer,
    ConnectModuleSerializer,
    HrModuleSerializer,
    TrainingModuleSerializer,
    UserGroupSerializer,
    UserSubscriptionsDetailModuleSerializer,
    UserSubscriptionsModuleSerializer,
    UserSubscriptionsUpdateModuleSerializer,
    WebUserFactoryPermissionDetailsSerializer,
    WebUserFactoryPermissionListSerializer,
    WebUserFactoryPermissionPostSerializer
)
from .models import (
    CompanySubscriptions,
    EngageModule,
    HrModule,
    ConnectModule,
    TrainingModule,
    UserSubscriptions,
    UserGroup,
    WebUserFactoryPermission
)
from .utils import StandardResultsSetPagination
from .filters import UserSubscriptionFilter


class CompanySubscriptionView(viewsets.ModelViewSet):
    lookup_field = 'company_uuid'
    pagination_class = None
    serializer_dict = {
        'create': CompanySubscriptionsModuleSerializer,
        'update': CompanySubscriptionsUpdateModuleSerializer,
        'list': CompanySubscriptionsDetailModuleSerializer,
        'retrieve': CompanySubscriptionsDetailModuleSerializer
    }

    def get_serializer_class(self):
        return self.serializer_dict[self.action]

    def get_queryset(self):
        queryset = CompanySubscriptions.objects.all()
        return queryset

    def update(self, request, *args, **kwargs):
        company_uuid = self.kwargs.get('company_uuid')
        try:
            object_instance = CompanySubscriptions.objects.get(company_uuid=company_uuid)
        except CompanySubscriptions.DoesNotExist:
            return Response({'error': 'Company Subscription Does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CompanySubscriptionsUpdateModuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update(instance=object_instance, validated_data=request.data)
            detail_serializer = CompanySubscriptionsDetailModuleSerializer(object_instance)
            return Response(detail_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanySubscriptionDetailByCompanyUuidView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return CompanySubscriptionsDetailModuleSerializer

    def get_queryset(self):
        queryset = CompanySubscriptions.objects.all()
        return queryset

    def retrieve(self, request, *args, **kwargs):
        company_uuid = self.request.query_params.get('company_uuid')
        try:
            object_instance = CompanySubscriptions.objects.get(company_uuid=company_uuid)
        except CompanySubscriptions.DoesNotExist:
            return Response({'error': 'Company Subscription Does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CompanySubscriptionsDetailModuleSerializer(object_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EngageModuleView(viewsets.ModelViewSet):
    serializer_class = EngageModuleSerializer
    pagination_class = StandardResultsSetPagination

    def get_object(self):
        try:
            engage = EngageModule.objects.get(uuid=self.kwargs.get('uuid'))
            return engage
        except EngageModule.DoesNotExist:
            return None

    def get_queryset(self):
        queryset = EngageModule.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = EngageModuleSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        object_instance = self.get_object()
        if not object_instance:
            return Response({'error': 'EngageModule Does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EngageModuleSerializer(object_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        object_instance = self.get_object()
        if not object_instance:
            return Response({'error': 'EngageModule Does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EngageModuleSerializer(instance=object_instance, data=request.data,
                                            context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConnectModuleView(viewsets.ModelViewSet):
    serializer_class = ConnectModuleSerializer
    pagination_class = StandardResultsSetPagination

    def get_object(self):
        try:
            connect = ConnectModule.objects.get(uuid=self.kwargs.get('uuid'))
            return connect
        except ConnectModule.DoesNotExist:
            return None

    def get_queryset(self):
        queryset = ConnectModule.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = ConnectModuleSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        object_instance = self.get_object()
        if not object_instance:
            return Response({'error': 'Connect Module Does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ConnectModuleSerializer(object_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        object_instance = self.get_object()
        if not object_instance:
            return Response({'error': 'Connect Module Does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ConnectModuleSerializer(instance=object_instance, data=request.data,
                                             context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HrModuleView(viewsets.ModelViewSet):
    serializer_class = HrModuleSerializer
    pagination_class = StandardResultsSetPagination

    def get_object(self):
        try:
            hr = HrModule.objects.get(uuid=self.kwargs.get('uuid'))
            return hr
        except HrModule.DoesNotExist:
            return None

    def get_queryset(self):
        queryset = HrModule.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = HrModuleSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        object_instance = self.get_object()
        if not object_instance:
            return Response({'error': 'HrModule Does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CompanySubscriptionsModuleSerializer(object_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        object_instance = self.get_object()
        if not object_instance:
            return Response({'error': 'HrModule Does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HrModuleSerializer(instance=object_instance, data=request.data,
                                        context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrainingModuleView(viewsets.ModelViewSet):
    serializer_class = TrainingModuleSerializer
    pagination_class = StandardResultsSetPagination

    def get_object(self):
        try:
            training = TrainingModule.objects.get(uuid=self.kwargs.get('uuid'))
            return training
        except TrainingModule.DoesNotExist:
            return None

    def get_queryset(self):
        queryset = TrainingModule.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = TrainingModuleSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        object_instance = self.get_object()
        if not object_instance:
            return Response({'error': 'Training Module Does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TrainingModuleSerializer(object_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        object_instance = self.get_object()
        if not object_instance:
            return Response({'error': 'Training Module Does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TrainingModuleSerializer(instance=object_instance, data=request.data,
                                              context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserGroupView(viewsets.ModelViewSet):
    serializer_class = UserGroupSerializer
    pagination_class = StandardResultsSetPagination

    def get_object(self):
        try:
            group = UserGroup.objects.get(uuid=self.kwargs.get('uuid'))
            return group
        except UserGroup.DoesNotExist:
            return None

    def get_queryset(self):
        queryset = UserGroup.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = UserGroupSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None, **kwargs):
        object_instance = self.get_object()
        if not object_instance:
            return Response({'error': 'UserGroup does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserGroupSerializer(object_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        object_instance = self.get_object()
        if not object_instance:
            return Response({'error': 'UserGroup Does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserGroupSerializer(instance=object_instance, data=request.data,
                                         context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSubscriptionListView(viewsets.ModelViewSet):
    filterset_class = UserSubscriptionFilter
    serializer_class = UserSubscriptionsDetailModuleSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = UserSubscriptions.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = UserSubscriptionsModuleSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user_subscription_instance = serializer.create(validated_data=request.data)
            detail_serializer = UserSubscriptionsDetailModuleSerializer(user_subscription_instance)
            return Response(detail_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSubscriptionDetailsView(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionsDetailModuleSerializer
    lookup_field = 'administrator_uuid'

    def get_queryset(self):
        queryset = UserSubscriptions.objects.filter(is_deleted=False).order_by('id')
        return queryset

    def retrieve(self, request, pk=None, **kwargs):
        try:
            user_subscription = UserSubscriptions.objects.get(is_deleted=False,
                                                              administrator_uuid=self.kwargs.get('administrator_uuid'))
        except UserSubscriptions.DoesNotExist:
            return Response({'error': 'User Subscription Does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSubscriptionsDetailModuleSerializer(user_subscription)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        try:
            user_subscription = UserSubscriptions.objects.get(is_deleted=False,
                                                              administrator_uuid=self.kwargs.get('administrator_uuid'))
        except UserSubscriptions.DoesNotExist:
            return Response({'error': 'User Subscriber Does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({'error': 'This company has not authorize for this module!'},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('hr'):
            if user_subscription.company_subscription.hr:
                if request.data.get('hr') != user_subscription.company_subscription.hr.id:
                    return response
            else:
                return response

        if request.data.get('engage'):
            if user_subscription.company_subscription.engage:
                if request.data.get('engage') != user_subscription.company_subscription.engage.id:
                    return response
            else:
                return response

        if request.data.get('connect'):
            if user_subscription.company_subscription.connect:
                if request.data.get('connect') != user_subscription.company_subscription.connect.id:
                    return response
            else:
                return response

        if request.data.get('training'):
            if user_subscription.company_subscription.training:
                if request.data.get('training') != user_subscription.company_subscription.training.id:
                    return response
            else:
                return response

        serializer = UserSubscriptionsUpdateModuleSerializer(instance=user_subscription, data=request.data,
                                                             context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return self.retrieve(request, pk=None, **kwargs)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            user_subscription = UserSubscriptions.objects.get(is_deleted=False,
                                                              administrator_uuid=kwargs.get('administrator_uuid'))
        except UserSubscriptions.DoesNotExist:
            return Response(
                {"administrator_uuid": kwargs.get('administrator_uuid'), "status": status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND)

        user_subscription.is_deleted = True
        user_subscription.save()

        return Response({"administrator_uuid": kwargs.get('administrator_uuid'), "status": status.HTTP_204_NO_CONTENT},
                        status=status.HTTP_204_NO_CONTENT)


class WebUserFactoryPermissionView(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WebUserFactoryPermissionPostSerializer
        return WebUserFactoryPermissionDetailsSerializer

    def get_queryset(self):
        queryset = WebUserFactoryPermission.objects.filter(is_deleted=False)
        return queryset

    def get_permission_details(self, admin_uuid):
        queryset = WebUserFactoryPermission.objects.filter(
            is_deleted=False, 
            user__uuid=admin_uuid
        ).values_list('factory', flat=True)

        obj = {
            'admin_uuid': admin_uuid,
            'factory_uuid': queryset
        }
        return obj

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        admin_uuid = kwargs.get('admin_uuid')
        
        return Response(self.get_permission_details(admin_uuid), status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        admin_uuid = kwargs.get('admin_uuid')

        try:
            user = User.objects.get(uuid=admin_uuid, is_deleted=False)
        except User.DoesNotExist:
            return Response({'error': 'User Not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = WebUserFactoryPermissionPostSerializer(data=request.data)

        if serializer.is_valid():
            for data in serializer.data.get('factory_permissions'):
                if data.get('permission'):
                    obj, created = WebUserFactoryPermission.objects.update_or_create(
                        factory=data.get('uuid'),
                        user= user
                    )
                else:
                    try:
                        permission = WebUserFactoryPermission.objects.get(is_deleted=False, factory=data.get('uuid'), user=user).delete()
                    except WebUserFactoryPermission.DoesNotExist:
                        pass

            return Response(self.get_permission_details(admin_uuid), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
