# import os
# from flask import Flask
# from flask_restful import Api
# from flasgger import Swagger
#
# from api_report.ver_2.config import Configuration
# from api_report.ver_2.resources import api_report_2
# from api_report.ver_2.resources import DriversReport, Driver
# from api_report.ver_2.resources import handle_404_error_api
#
#
# def create_app(test_config=False, config_class=Configuration):
#     app = Flask(__name__)
#     app.config.from_object(config_class)
#     api = Api(app)
#     Swagger(
#         app,
#         template_file=os.path.join('docs', 'template.yml'),
#         parse=True
#     )
#     api_url = app.config.get('API_URL')
#     api.add_resource(DriversReport, f'{api_url}/drivers/')
#     api.add_resource(Driver, f'{api_url}/drivers/<string:abbreviation>/')
#     app.register_blueprint(api_report_2)
#     app.register_error_handler(404, handle_404_error_api)
#     if test_config:
#         app.config['TESTING'] = True
#     return app


# import os
# from flask import Flask
# from flask_restful import Api
# from flasgger import Swagger
# from api_report.resources.driver import DriverInfo
# from api_report.resources.race import RaceReport
# from api_report.resources.handlers import handle_404_error_api
# # from config import Configuration
# from api_report.models import db_class, Driver, Team, RaceInfo
# from api_report.create_db import create_db
#
#
# def create_app(test_config=False):
#     """Create and configure an instance of the Flask application."""
#     app = Flask(__name__)
#     app.config.from_object("config.Configuration")
#     api_report = Api(app)
#     Swagger(
#         app,
#         template_file=os.path.join('resources/docs', 'template.yml'),
#         parse=True
#     )
#     api_report.add_resource(RaceReport, '/api_report/drivers/')
#     api_report.add_resource(DriverInfo, '/api_report/drivers/<string:abbreviation>/')
#     app.register_error_handler(404, handle_404_error_api)
#     if test_config:
#         app.config['TESTING'] = True
#     return app
#
#
# if __name__ == '__main__':
#     database_tables = [Driver, Team, RaceInfo]
#     create_db(db_class.database, database_tables)
#     app1 = create_app()
#     app1.run()
