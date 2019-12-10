class IWSSearchParameters:

    def __init__(self, service_category=None, service_grade=None, service_types=None, region=None, start_schedule=None,
                 name="", business_owner_type=None):
        if service_types is None:
            service_types = []
        if region is None:
            region = []
        self.service_grade = service_grade
        self.service_types = service_types
        self.service_category = service_category
        self.region = region
        self.name = name
        self.start_schedule = start_schedule
        self.business_owner_type=business_owner_type
