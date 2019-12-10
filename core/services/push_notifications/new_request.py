#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gcm import *
from gcm.gcm import GCMAuthenticationException
import logging

# from pyfcm import FCMNotification
from pyfcm import FCMNotification

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PushNotification:
    # gcm = GCM("AIzaSyBmPImQM647_Y8B9RDLNP369-P1RQp6fSY")
    gcm = GCM("AIzaSyBxU6rVK8-B7ro9G72h3zRehk1i1JjCtiY")

    # gcm = GCM("AAAAbJRUy5U:APA91bHXw43Jlye_Cthdd_dXVnLLYE9oKNjFt-z8BpYeEPFIVCcP2P_tnsdTY8VooqJEL5rREMk0UWJ1B4W5Xy-dbaLKc88C_g88VAnYjjEjviDOOts7AJ0Lgp_lC_PTlQNh2_5qfwJJ")

    @staticmethod
    def push(reg_ids, data):
        FCMSend(reg_ids, data)
        return True,
        # response = True,
        # try:
        #     response = True, PushNotification.gcm.json_request(registration_ids=reg_ids, data=data)
        #
        # except GCMAuthenticationException:
        #     logger.error("Run filter shekan :(", exc_info=True)
        #     response = False,
        #
        # except:
        #     if 'errors' in response:
        #         for error, reg_ids in response['errors'].items():
        #             # Check for errors and act accordingly
        #             if error in ['NotRegistered', 'InvalidRegistration']:
        #                 # Remove reg_ids from database
        #                 for reg_id in reg_ids:
        #                     print("Removing reg_id: {0} from db".format(reg_id))
        #     response = False,
        # return response


def FCMSend(reg_id, data):
    server_key = 'AAAAbJRUy5U:APA91bHXw43Jlye_Cthdd_dXVnLLYE9oKNjFt-z8BpYeEPFIVCcP2P_tnsdTY8VooqJEL5rREMk0UWJ1B4W5Xy-dbaLKc88C_g88VAnYjjEjviDOOts7AJ0Lgp_lC_PTlQNh2_5qfwJJ'
    push_service = FCMNotification(api_key=server_key)

    return push_service.single_device_data_message(registration_id=reg_id, data_message=data)

if __name__ == '__main__':
    data = {
        'id': '11',
        'ticker': "My Notification Ticker",
        # 'autoCancel': True,
        'largeIcon': "ic_launcher",
        'smallIcon': "ic_notification",
        'bigText': "جون من کار کن",
        'subText': "ما اینیم!",
        'color': "red",
        # 'vibrate': 1,
        # 'vibration': 300,
        'tag': 'ناپلئونی',
        'group': "ناپلئونی خوران",
        # 'ongoing': False,

        'title': "ناپلئونی آقای کیایی",
        'message': "پیام ما: آقای کیایی، با سلام... ناپلئونی فراموش نشود.",
        # 'playSound': False,
        'soundName': 'default',
        'number': '10',
        # 'actions': [{'id': 'Accept', 'text': 'Display Text'}, {'id': 'Deny', 'text': 'Display Text'}],
        'actions': '["Accept", "Deny"]',
        'info': {
            'car_info': {'name': 'pride', 'id': 1},
            'problem': {'grade': 'common', 'types': ['روغن', 'فیلتر هوا'], 'job_id': 5},
            'type': 'new_job_request'
        },
        'type': 'new_job_request'
    }
    reg_id_car = 'ejX7walDS4Y:APA91bElMQcZBEW8iYE0U1Ciun5z8QFiN1nKeCMRPdABLYKwh37Zy_398xmetFwYt-rA79JdxK4LLIrRg-PF_rQuPk5jBr1M-yNEMDINUVDPioa4IfhBwIcm2SwswQz-sDotpDzZioem'
    # reg_id = 'e2mPT-d_PX4:APA91bHoZynEICUO8qFX78CnIQipkkOdOwuyhnZ6GSx0YWFyW2bagSsGynxCZCZDyhmOgpFmy_cglRCdHpVBaSZghExoTD-ktjZsWqbrGRfrISWaUVqyjdy6cGjoHuHMbXgn2oxkwPjd'
    # PushNotification.push([reg_id_car], data)
    FCMSend(reg_id_car, data)

    # job = Job.query.filter(Job.id == 1).first()
