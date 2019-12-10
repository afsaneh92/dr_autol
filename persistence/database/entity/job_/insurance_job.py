from persistence.database.entity.job_.job import Job
from app import db, global_logger


class InsuranceJob(Job):
    __tablename__ = 'insurance_job'
    id = db.Column(db.Integer, db.ForeignKey('jobs.id'), primary_key=True)
    duration = db.Column(db.Integer, nullable=False)
    car_value = db.Column(db.Numeric, nullable=False)
    type = db.Column(db.String(50))
    company = 1

    __mapper_args__ = {
        'polymorphic_identity': 'Insurance',
        'polymorphic_on': type
    }
    # car_problems = db.relationship("CarProblem", backref="car_problem_backref", lazy='dynamic',
    #                                primaryjoin="Job.id == CarProblem.job_id")
