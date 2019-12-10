from persistence.database.entity.job_.insurance_job import InsuranceJob
from app import db, global_logger


class Body(InsuranceJob):
    non_fabric_accessories_values = db.Column(db.String(30))
    extra_coverages = db.Column(db.String(30))

    __mapper_args__ = {
        'polymorphic_identity':'Body',
    }