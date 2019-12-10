from persistence.database.entity.job_.insurance_job import InsuranceJob
from app import db, global_logger


class ThirdPart(InsuranceJob):
    max_coverage = db.Column(db.String(30))

    __mapper_args__ = {
        'polymorphic_identity':'ThirdParty',
    }