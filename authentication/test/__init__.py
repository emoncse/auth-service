import datetime
import random
import uuid
import string
import factory
import factory.fuzzy
from ..models import User
from commons.enums import MOBILE


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    phone = ''.join(random.choice(string.digits) for x in range(11))
    email = factory.LazyAttribute(lambda a: '{0}.{1}@example.com'.format(a.first_name, a.last_name).lower())
    company_uuid = str(uuid.uuid4())
    is_staff = True
    is_active = True
    user_type = MOBILE
    date_joined = factory.LazyFunction(datetime.datetime.utcnow)
    is_deleted = False
    uuid = email
