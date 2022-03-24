import os
from flask import Flask, g
from flask_restful import Api
from flasgger import Swagger
from src.api_report.resources.driver import DriverInfo
from src.api_report.resources.race import RaceReport
from src.api_report.resources.handlers import handle_404_error_api
from src.api_report.config import Configuration
from src.api_report.db.models import db, Driver, Team, RaceInfo
from src.api_report.db.insert_records import insert_records_to_db


def create_app(test_config=False):
    """Create and configure an instance of the Flask application."""
    application = Flask(__name__)
    application.config.from_object(Configuration)
    api_report = Api(application)
    api_url = Configuration.API_URL
    Swagger(
        application,
        template_file=os.path.join('resources/docs', 'template.yml'),
        parse=True
    )
    # Resources
    api_report.add_resource(RaceReport, f'{api_url}/drivers/')
    api_report.add_resource(DriverInfo, f'{api_url}/drivers/<string:abbreviation>/')
    # Handlers
    application.register_error_handler(404, handle_404_error_api)

    @application.before_request
    def connect_db():
        if 'db' not in g:
            g.db = db
            g.db.connect()

    @application.teardown_request
    def close_db(error):
        if 'db' in g:
            g.db.close()
            if error:
                print(str(error))

    if test_config:
        application.config['TESTING'] = True
    return application


if __name__ == '__main__':
    # Create database
    database_tables = [Driver, Team, RaceInfo]
    insert_records_to_db(db, database_tables)
    # Create app
    app = create_app()
    app.run()

