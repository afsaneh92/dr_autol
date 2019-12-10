from app import db, global_logger
from persistence.database.entity.base import BaseMixin

logger = global_logger


class BusinessOwnerTask(BaseMixin, db.Model):
    __tablename__ = 'business_owner_tasks'
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    business_owner_id = db.Column(db.Integer, db.ForeignKey('auto_service_business_owners.id'))
    business_owner_ = db.relationship('AutoServiceBusinessOwner')
    service_definition_id = db.Column(db.Integer, db.ForeignKey('services_definition.id'))
    service_definition = db.relationship("ServicesDefinition")

    def __repr__(self):
        return '<BusinessOwnerTask %r>' % self.id


class BusinessOwnerTaskCarWash(BaseMixin, db.Model):
    __tablename__ = 'business_owner_tasks_car_wash'
    id = db.Column(db.Integer, primary_key=True)
    deleted = db.Column(db.Boolean, default=False)
    business_owner_id = db.Column(db.Integer, db.ForeignKey('car_wash_business_owner_owners.id'))
    business_owner_ = db.relationship('CarWashBusinessOwner')
    service_definition_id = db.Column(db.Integer, db.ForeignKey('services_definition.id'))
    service_definition = db.relationship("ServicesDefinition")

    def __repr__(self):
        return '<BusinessOwnerTask %r>' % self.id
