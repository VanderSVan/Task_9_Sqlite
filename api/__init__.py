# import os
# from flask import Flask
# from flask_restful import Api
# from flasgger import Swagger
# from db.create_db import Database, create_tables, insert_records_to_db
# from api.ver_2.api_ver_2 import api_report_2
# from api.ver_2.api_ver_2 import DriversReport, DriverStats
# from api.ver_2.api_ver_2 import handle_404_error_api
# from db.models import Driver, Team, RaceInfo
# from api.ver_2.config import Configuration
#
# database_tables = [Driver, Team, RaceInfo]
#
#
# def create_db(database: Database, tables):
#     create_tables(database, tables)
#     insert_records_to_db(database, tables)
#     print('*** db has been created ***', '\n')
#
#
# def create_app(test_config=False):
#     app = Flask(__name__)
#     app.config.from_object('config.Configuration')
#     api = Api(app)
#     Swagger(
#         app,
#         template_file=os.path.join('ver_2', 'docs', 'template.yml'),
#         parse=True
#     )
#     api.add_resource(DriversReport, '/api/v2/drivers/')
#     api.add_resource(DriverStats, '/api/v2/drivers/<string:abbreviation>/')
#     app.register_blueprint(api_report_2)
#     app.register_error_handler(404, handle_404_error_api)
#     if test_config:
#         app.config['TESTING'] = True
#     return app
#
#
# application = create_app(test_config=True)
# db = Database(application, Configuration.DATABASE)
#
#
# if __name__ == "__main__":
#     create_db(db, database_tables)
#     application.run()
