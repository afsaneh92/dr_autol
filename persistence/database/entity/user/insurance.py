from persistence.database.entity.user.business_owner import BusinessOwner
from app import db, global_logger


class InsuranceBusinessOwner(BusinessOwner):
    __tablename__ = 'insurance_business_owners'
    id = db.Column(db.Integer, db.ForeignKey('business_owners.id'), primary_key=True)
    branch_code = db.Column(db.String(6), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    company = db.relationship("Company")


    __mapper_args__ = {
        'polymorphic_identity':'InsuranceBusinessOwner',
    }
    __table_args__ = (db.UniqueConstraint('branch_code', name='unique_branch_code'),)

    # __tablename__ = 'insurance_business_owners'
    # id = db.Column(db.Integer, db.ForeignKey('business_ownerss.id'), primary_key=True)
    # branch_code = db.Column(db.String(20), nullable=True)


    # __mapper_args__ = {
    #     'polymorphic_identity':'InsuranceBusinessOwner',
    #     # 'polymorphic_on': 'business_owner_type'
    # }

    def __repr__(self):
        return '<InsuranceBusinessOwner %r>' % self.id