from core.messages.keys import Keys


class ReflectionControllers(object):
    ACCEPT_JOB_CONTROLLER = {Keys.MODULE: 'core.controller.business_owner.job_process_statuses.accept_request',
                             Keys.KLASS: 'AcceptController'}
    DENY_JOB_CONTROLLER = {Keys.MODULE: 'core.controller.business_owner.job_process_statuses.deny_request',
                           Keys.KLASS: 'DenyJobRequestController'}
    START_JOB_CONTROLLER = {Keys.MODULE: 'core.controller.business_owner.job_process_statuses.start_request',
                            Keys.KLASS: 'StartJobRequestController'}
    FINISH_JOB_CONTROLLER = {Keys.MODULE: 'core.controller.business_owner.job_process_statuses.finish_request',
                             Keys.KLASS: 'FinishJobRequestController'}
    CANCEL_JOB_BY_BO_CONTROLLER = {Keys.MODULE: 'core.controller.business_owner.job_process_statuses.cancel_request',
                                   Keys.KLASS: 'CancelJobRequestController'}
    FULL_PAYMENT_CONTROLLER = {Keys.MODULE: 'core.controller.car_owner.payment.full',
                               Keys.KLASS: 'FullPaymentRequestController'}
    INSTALLMENT_PAYMENT_CONTROLLER = {Keys.MODULE: 'core.controller.car_owner.payment.installment',
                                      Keys.KLASS: 'InstallmentPaymentRequestController'}
    AUTO_SERVICE_JOB_CONTROLLER = {Keys.MODULE: 'core.controller.car_owner.job.auto_service',
                                   Keys.KLASS: 'AutoServiceRequestController'}
    INSURANCE_JOB_CONTROLLER = {Keys.MODULE: 'core.controller.car_owner.job.insurance',
                                Keys.KLASS: 'InsuranceRequestController'}

    ACCEPT_ORDER_CONTROLLER = {Keys.MODULE: 'core.controller.supplier.order_process_statuses.accept_order_request',
                               Keys.KLASS: 'AcceptOrderController'}
    DENY_ORDER_CONTROLLER = {Keys.MODULE: 'core.controller.supplier.order_process_statuses.deny_order_request',
                               Keys.KLASS: 'DenyOrderController'}


class ReflectionRequests(object):
    ACCEPT_JOB_REQUEST = {Keys.MODULE: 'core.request.choose_job_by_bo.accept_request', Keys.KLASS: 'AcceptRequest'}
    DENY_JOB_REQUEST = {Keys.MODULE: 'core.request.choose_job_by_bo.deny_request', Keys.KLASS: 'DenyRequest'}
    START_JOB_REQUEST = {Keys.MODULE: 'core.request.choose_job_by_bo.start_request', Keys.KLASS: 'StartJobRequest'}
    FINISH_JOB_REQUEST = {Keys.MODULE: 'core.request.choose_job_by_bo.finish_request', Keys.KLASS: 'FinishJobRequest'}
    CANCEL_JOB_BY_BO_REQUEST = {Keys.MODULE: 'core.request.choose_job_by_bo.cancel_request',
                                Keys.KLASS: 'CancelJobRequest'}
    INSTALLMENT_PAYMENT_REQUEST = {Keys.MODULE: 'core.request.car_owner.payment.installment',
                                   Keys.KLASS: 'InstallmentRequest'}
    FULL_PAYMENT_REQUEST = {Keys.MODULE: 'core.request.car_owner.payment.full', Keys.KLASS: 'FullRequest'}
    AUTO_SERVICE_JOB_REQUEST = {Keys.MODULE: 'core.request.car_owner.job.auto_service',
                                Keys.KLASS: 'AutoServiceRequest'}
    INSURANCE_JOB_REQUEST = {Keys.MODULE: 'core.request.car_owner.job.insurance', Keys.KLASS: 'InsuranceRequest'}

    ACCEPT_ORDER_REQUEST = {Keys.MODULE: 'core.request.choose_order_item_by_supplier.accept_order_request',
                            Keys.KLASS: 'AcceptOrderRequest'}
    DENY_ORDER_REQUEST = {Keys.MODULE: 'core.request.choose_order_item_by_supplier.deny_order_request',
                            Keys.KLASS: 'DenyOrderRequest'}

