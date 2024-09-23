import datetime
import requests

from rest_framework import status

from auth.settings import ORGANIZATION_BASE_URL
from commons.utils import get_logger

logger = get_logger()


def organization_worker_info_update(worker_uuid, company_uuid):

    url = ORGANIZATION_BASE_URL + '/companies/' + \
        company_uuid + '/workers/' + worker_uuid
    worker_update_response = requests.put(
        url, json={'joined_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    if worker_update_response.status_code == status.HTTP_200_OK:
        logger.info('successfully Worker Joined_at updated.')
    else:
        logger.info('Worker Joined_at update failed.')


def get_worker_details(uuid):
    url = ORGANIZATION_BASE_URL + '/workers/{}'.format(uuid)

    try:
        response = requests.get(url)
        if response.status_code == status.HTTP_200_OK:
            return response.json()
    except Exception as e:
        logger.error("Unable to get worker data: {}".format(e))

    return None
