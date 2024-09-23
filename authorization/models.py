import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from commons.models import BaseModel
from authentication.models import User


class EngageModule(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, auto_created=True)
    company_uuid = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text=_('UUID from company table')
    )
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return str(self.uuid)


class HrModule(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, auto_created=True)
    company_uuid = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text=_('UUID from company table')
    )
    start_date = models.DateTimeField(auto_now_add=True, auto_now=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return str(self.uuid)


class ConnectModule(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, auto_created=True)
    company_uuid = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text=_('UUID from company table')
    )
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return str(self.uuid)


class TrainingModule(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, auto_created=True)
    company_uuid = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text=_('UUID from company table')
    )
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return str(self.uuid)


class CompanySubscriptions(BaseModel):
    package_uuid = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text=_('UUID from organization package table')
    )
    company_uuid = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text=_('UUID from company table')
    )
    engage = models.OneToOneField(EngageModule, on_delete=models.DO_NOTHING, null=True, blank=True,
                                  related_name='company_engage_module_subscription')
    hr = models.OneToOneField(HrModule, on_delete=models.DO_NOTHING, null=True, blank=True,
                              related_name='company_hr_module_subscription')
    connect = models.OneToOneField(ConnectModule, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name='company_connect_module_subscription')
    training = models.OneToOneField(TrainingModule, on_delete=models.DO_NOTHING, null=True, blank=True,
                                    related_name='company_training_module_subscription')
    on_boarding_date = models.DateTimeField(auto_now_add=True)
    expire_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta:
        verbose_name = _('company_subscription')
        verbose_name_plural = _('company_subscriptions')

    def __str__(self):
        return str(self.uuid)


class UserGroup(BaseModel):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class UserSubscriptions(BaseModel):
    company_subscription = models.ForeignKey(CompanySubscriptions, on_delete=models.DO_NOTHING, null=True, blank=True,
                                             related_name='user_company_subscription')
    administrator_uuid = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text=_('UUID for organization administrator')
    )
    user_group = models.ForeignKey(UserGroup, on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name='user_group_subscriptions')
    engage = models.ForeignKey(EngageModule, on_delete=models.DO_NOTHING, null=True, blank=True,
                               related_name='user_engage_module_subscription')
    hr = models.ForeignKey(HrModule, on_delete=models.DO_NOTHING, null=True, blank=True,
                           related_name='user_hr_module_subscription')
    connect = models.ForeignKey(ConnectModule, on_delete=models.DO_NOTHING, null=True, blank=True,
                                related_name='user_connect_module_subscription')
    training = models.ForeignKey(TrainingModule, on_delete=models.DO_NOTHING, null=True, blank=True,
                                 related_name='user_training_module_subscription')

    def __str__(self):
        return str(self.uuid)


class WebUserFactoryPermission(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_factories')
    factory = models.CharField(max_length=150)

    # class Meta:
    #     unique_together = ('user', 'factory')
