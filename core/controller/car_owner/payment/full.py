from app import db, global_logger
from core.controller import BaseController
from core.messages.keys import Keys
from core.messages.translator.messages_keys import MessagesKeys
from core.result import Result
from core.result.failure.Job_not_payable import JobNotPayable
from core.result.failure.invalid_state_for_job import InvalidState
from core.result.failure.job_paid_before import JobPaidBefore
from core.result.failure.not_found_job import JobNotFound
from core.result.failure.wrong_amount import WrongAmountFactor
from core.result.success.success_payment_added import SuccessPaymentAdded
from core.services.push_notifications.iws_announcement import IWSAnnouncement
from core.validation.database_helper import calculate_job_payment_price
from core.validation.helpers import db_error_message
from persistence.database.entity.car import Car
from persistence.database.entity.job_.job import Job
from persistence.database.entity.stauts import Status
from persistence.database.entity.user.user import User

logger = global_logger


class FullPaymentRequestController(BaseController):

    def __init__(self, job, payment, converter):
        self.payment = payment
        self.job = job
        self.converter = converter

    def execute(self):
        error_free, existence_job_result = self._is_job_valid()
        if not error_free:
            return existence_job_result

        self.job = existence_job_result
        error_free, result = self._is_bad_request()
        if error_free:
            dct = result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        error_free, result = self.do_payment_operation()
        if not error_free:
            dct = result.dictionary_creator()
            return self.serialize(dct, converter=self.converter)

        self._push_notification_done_payment()
        dct = result.dictionary_creator()
        return self.serialize(dct, converter=self.converter)

    def _validate_state(self):
        if self.job.status_.name == Keys.STATUS_START:
            return True,
        return False, InvalidState(status=404, message=Result.language.INVALID_STATE, params=None)

    def _load_job(self):
        return Job.load_job(self.job.id)

    def _push_notification_done_payment(self):
        loaded_car_result = Car.find(id=self.job.car_id)
        loaded_business_owner_result = User.find(id=self.job.business_owner_id)
        if not loaded_car_result[0] or not loaded_business_owner_result[0]:
            logger.warn('push notification failed')
            return
        business_owner = loaded_business_owner_result[1][0]
        car = loaded_car_result[1][0]
        IWSAnnouncement.send_payment_result_notification(car, business_owner)

    def _is_exist_job(self, job):
        result = True,
        if job is None:
            result = False, JobNotFound(status=404, message=MessagesKeys.NOT_FOUND_JOB)
        else:
            result = True, job
        return result

    def do_payment_operation(self):
        result = None
        try:
            error_free, result = self.add_payment()
            if not error_free:
                raise Exception()
            self.payment = result['payment']
            error_free, result = self.update_job_with_payment()
            if not error_free:
                raise Exception()
            db.session.commit()
            result = True, SuccessPaymentAdded(status=200, message=Result.language.PAYMENT_PAID_SUCCESSFULLY,
                                               params=None)
        except:
            db.session.rollback()
            result = db_error_message(logger)
        return result

    def update_job_with_payment(self):
        data = {'payment_id': self.payment.id}
        return self.job.update(db, data)

    def add_payment(self):
        return self.payment.add(db, self.payment)

    def is_payable(self):
        pass

    def _is_amount_enough(self):
        job_price = calculate_job_payment_price(self.job)

        if self.payment.amount == job_price:
            return True,
        else:
            return False, WrongAmountFactor(status=404, message=MessagesKeys.JOB_PRICE_IS_WRONG, params=None)

    def _is_job_payable(self):
        error_free, ids = Status.load_not_payable_statues_ids()
        if not error_free:
            return False, ids
        if self.job.status_id in ids:
            return False, JobNotPayable(status=404, message=MessagesKeys.JOB_IS_NOT_PAYABLE, params=None)
        else:
            return True,

    def _is_paid_before(self):
        if not self.job.payment_id is None:
            return False, JobPaidBefore(status=404, message=MessagesKeys.JOB_IS_PAID_BEFORE, params=None)
            pass
        else:
            return True,

    def _is_bad_request(self):
        amount_result = self._is_amount_enough()
        if not amount_result[0]:
            return True, amount_result[1]
        payable_result = self._is_job_payable()
        if not payable_result[0]:
            return True, payable_result[1]
        paid_before_result = self._is_paid_before()
        if not paid_before_result[0]:
            return True, paid_before_result[1]
        return False, None

    def _is_job_valid(self):
        error_free, loaded_job = self._load_job()
        if not error_free:
            dct = loaded_job.dictionary_creator()
            return False, self.serialize(dct, converter=self.converter)
        error_free, existence_job = self._is_exist_job(loaded_job)
        if not error_free:
            dct = existence_job.dictionary_creator()
            return False, self.serialize(dct, converter=self.converter)
        return True, existence_job
