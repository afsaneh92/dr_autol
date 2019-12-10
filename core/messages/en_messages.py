from core.messages.base_messages import FailMessagesBase, SuccessMessagesBase


class EnFailMessages(FailMessagesBase):
    password_is_empty = "Your password can not be empty"
    name_is_empty = "Your name can not be empty"
    phone_number_is_empty = "Your phone number can not be empty"

    def __init__(self):
        pass


class EnSuccessMessages(SuccessMessagesBase):
    car_owner_has_been_registered = "You registered successfully"

    def __init__(self):
        pass

