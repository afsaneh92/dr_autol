from sqlalchemy import Column, Integer

from app import db
from persistence.database.entity.base import BaseMixin
from persistence.database.entity.service_definition import ServicesDefinition



#TODO delete, no usage
class ServicesDefinitionBrands(BaseMixin, db.Model):
    __tablename__ = 'service_definition_brands'
    # service_definition_id = db.Column(db.Integer, db.ForeignKey('services_definition.id'))
    # brand_id = db.Column(Integer, db.ForeignKey('consumable_items.id'))
    # service_definition = db.relationship(ServicesDefinition, backref="service_brands")
    # brand = db.relationship("ConsumableItem")

    def __init__(self, brand=None, service_definition=None):
        self.brand = brand
        self.service_definition = service_definition

