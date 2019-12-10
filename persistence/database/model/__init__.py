


def create_db():
    from persistence.database.entity.car_owner import CarOwners
    from persistence.database.entity.car import Car
    from persistence.database.entity.admin import Administrator
    from persistence.database.entity.auto_type import AutoType
    # from persistence.database.entity.business_owner import BusinessOwners
    from persistence.database.entity.service_grade import ServiceGrade
    from persistence.database.entity.service_type import ServiceType
    from persistence.database.entity.services import ServiceGradeType
    from persistence.database.entity.business_owner_task import BusinessOwnerTask
    from persistence.database.entity.service_grade import ServiceGrade
    from persistence.database.entity.service_type import ServiceType
    from persistence.database.entity.stauts import Status
    from persistence.database.entity.payment_type import PaymentType
    from persistence.database.entity.payment_.payment import Payment
    from persistence.database.entity.payment_.full import FullPayment
    from persistence.database.entity.payment_.installments import Installment
    from persistence.database.entity.job_.job import Job
    from persistence.database.entity.job_.insurance_job import InsuranceJob
    from persistence.database.entity.job_.autoservice_job import AutoServiceJob
    from persistence.database.entity.consumable_item import ConsumableItem
    from persistence.database.entity.question import Question
    from persistence.database.entity.question_set import QuestionSet
    from persistence.database.entity.service_type import ServiceType
    from persistence.database.entity.stauts import Status
    from persistence.database.entity.payment_type import PaymentType
    from persistence.database.entity.user.auto_service import AutoServiceBusinessOwner
    from persistence.database.entity.user.insurance import InsuranceBusinessOwner
    from persistence.database.entity.comany.insurance_company import Company, InsuranceCompany
    from persistence.database.entity.payment_.installment import InstallPayment
    from persistence.database.entity.payment_.installments import Installment

    from persistence.database.entity.auto_types_products import AutoTypeProduct
    from persistence.database.entity.service_definition import ServicesDefinition
    from app import db

    db.create_all()


def drop_db():
    from app import db

    db.reflect()
    db.drop_all()


if __name__ == "__main__":
    # drop_db()
    create_db()
