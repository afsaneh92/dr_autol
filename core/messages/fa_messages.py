from core.messages.base_messages import SuccessMessagesBase, FailMessagesBase


class FaFailMessages(FailMessagesBase):
    password_is_empty = "رمز عبور نمی تواند خالی باشد."
    name_is_empty = "نام نمی تواند خالی باشد."
    phone_number_is_empty = "شماره تلفن نمی تواند خالی باشد."
    BAD_RANGE_RATE = "بازه ی امتیازدهی درست نیست."

    def __init__(self):
        pass


class FaSuccessMessages(SuccessMessagesBase):
    car_owner_has_been_registered = "ثبت نام موفقیت آمیز بود."

    def __init__(self):
        pass

