class Endpoints(object):
    server = "localhost"
    SERVICES_SERVICE_GRADES = '/services/service_grades'
    SERVICES_SERVICE_TYPES = '/services/service_types'
    CAR_OWNER_SET_APPOINTMENT = '/car_owner/set_appointment'
    CANCEL_JOB_BY_CAR_OWNER = '/car_owner/job/cancel'
    BUSINESS_OWNER_JOB_REQUEST = '/business_owner/job_request'
    FORGET_PASSWORD = '/forget_password'
    BUSINESS_OWNER_JOBS = '/business_owner/jobs'
    VARIABLE_BUSINESS_OWNER = '/<business_owner_id>'
    BUSINESS_OWNER_JOB = '/business_owner/job'
    ACTIVATE_BUSINESS_OWNER = '/business_owner_activate'
    CHANGE_PASSWORD = '/change_password'
    LIST_UNFINISHED_JOB = '/list_unfinished_job'
    RATE_BUSINESS_OWNER_BY_CAR_OWNER = '/rating_by_car_owner'
    DELETE_FROM_CALENDAR = '/business_owner/calendar'
    BUSINESS_OWNER_UPDATE_LOCATION = '/business_owner/location'
    INSERT_IN_CALENDAR = '/business_owner/calendar'
    LIST_IWS_BY_SEARCH = '/car_owner/iws'
    CAR_OWNER_PAYMENTS = '/car_owner/payments'
    LOGIN_IWS = '/login/iws'
    REGISTER_IWS = '/register/iws'
    LAST_EVENT = '/last_event'
    PAYABLE_LIST = '/payable_list'
    AUTO_TYPE_CONSUMABLE_ITEMS = '/auto_type_consumable_items'
    LIST_JOBS_FOR_BUSINESS_OWNER = '/business_owner/jobs'
    ADD_NEW_CAR = '/car_owner/cars'
    LIST_AUTO_TYPE = '/auto_types'
    ADD_NEW_PRODUCT = '/products'
    EDIT_PRODUCT_INFO = '/products'
    VARIABLE_PRODUCTS = '/<product_id>'
    DELETE_PRODUCT_INFO = '/products'
    GET_PRODUCT_LIST = '/products'
    SEARCH_FOR_PRODUCT = '/search_products'
    GET_SOLD_PRODUCT_LIST = '/sold_products'
    SUPPLIER_DAILY_PURCHASE_LIST = '/supplier_daily_purchase_list'
    REGISTER_SUPPLIER = '/register_supplier'
    FORCE_UPDATE = '/update'
    GET_BUSINESS_OWNER_REST_OF_ALLOWED_CREDIT = '/allowed_credit'
    BUSINESS_OWNER_ID = '/<business_owner_id>'
    LOGIN = '/login'
    SUPPLIER_CHANGE_ORDER_STATUS = '/supplier_change_order_status'
