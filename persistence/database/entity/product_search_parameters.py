class ProductsSearchParameters:

    def __init__(self, code="", supplier_id=None, brand_id=None, company_id=None, sub_category_id=None, min_price=None,
                 max_price=None,
                 minimum_order=None, accepted_number=None, requested_number=None, supplier_status_id=None):
        self.code = code
        self.supplier_id = supplier_id
        self.brand_id = brand_id
        self.company_id = company_id
        self.sub_category_id = sub_category_id
        self.minimum_order = minimum_order
        self.max_price = max_price
        self.min_price = min_price
        self.accepted_number = accepted_number
        self.requested_number = requested_number
        self.supplier_status_id = supplier_status_id
