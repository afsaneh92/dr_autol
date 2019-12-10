from abc import ABCMeta, abstractmethod

from core.business_logics.users import user_logic


class UserService:
    __metaclass__ = ABCMeta

    @abstractmethod
    def register_user(self, http_request):
        pass


class CarOwnerService(UserService):

    def register_user(self, http_request):
        return user_logic.run_car_owner_registration_logic(http_request)
