from app import db, global_logger
from core.validation.helpers import db_error_message

logger = global_logger


class CarProblem(db.Model):
    __tablename__ = 'car_problems'
    # each car problem should have a filed for persist brand product name eg: 10w40
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    job_id = db.Column(db.Integer, db.ForeignKey('auto_service_job.id'))
    job_ = db.relationship('AutoServiceJob')

    services_definition_id = db.Column(db.Integer, db.ForeignKey('services_definition.id'))
    services_definition = db.relationship("ServicesDefinition")

    consumable_item_id = db.Column(db.Integer, db.ForeignKey('consumable_items.id'))
    consumable_item = db.relationship("ConsumableItem")

    def __repr__(self):
        return '<CarProblem %r>' % self.id

    @staticmethod
    def find_job_problems(job):
        result = None
        try:
            result = True, CarProblem.query.filter(CarProblem.job_id == job.id).all()
        except:
            False, db_error_message(logger)
        return result
