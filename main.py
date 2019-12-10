from app import app
from routers.admin import admin
from routers.authintication import authentication
from routers.business_owner import business_owner
from routers.car_owner import car_owner
from routers.choose_services import choose_service_grade
from routers.index import index_route

app.register_blueprint(index_route)
app.register_blueprint(car_owner)
app.register_blueprint(business_owner)
app.register_blueprint(authentication)
app.register_blueprint(admin)
app.register_blueprint(choose_service_grade)
# app.register_blueprint(supplier)

@app.teardown_appcontext
def shutdown_session(exception=None):
    pass


# @app.teardown_request
# def teardown_request(exception):
#     if exception:
#         db_session.session.rollback()
#     db_session.session.remove()


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    # logger = logging.getLogger('dr_autol_logger')
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')
    app.run(host="0.0.0.0")
