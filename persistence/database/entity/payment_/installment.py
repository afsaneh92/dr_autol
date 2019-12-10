from app import db
from persistence.database.entity.payment_.payment import Payment


class InstallPayment(Payment):
    __tablename__ = 'install_payments'
    id = db.Column(db.Integer, db.ForeignKey('payments.id'), primary_key=True)
    installments = db.relationship("Installment")

    __mapper_args__ = {
        'polymorphic_identity':'InstallPayment',
    }
    # car_problems = db.relationship("CarProblem", backref="car_problem_backref", lazy='dynamic',
    #                                primaryjoin="Job.id == CarProblem.job_id")
