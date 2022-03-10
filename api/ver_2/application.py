import os
from flask import Flask
from flask_restful import Api
from flasgger import Swagger
from api_ver_2 import api_report_2
from api_ver_2 import DriversReport, DriverStats
from api_ver_2 import handle_404_error_api


def create_app(test_config=False):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    app.config.from_object('config.Configuration')
    api = Api(app)
    Swagger(
        app,
        template_file=os.path.join('ver_2', 'docs', 'template.yml'),
        parse=True
    )
    api.add_resource(DriversReport, '/api/v2/drivers/')
    api.add_resource(DriverStats, '/api/v2/drivers/<string:abbreviation>/')
    app.register_blueprint(api_report_2)
    app.register_error_handler(404, handle_404_error_api)
    if test_config:
        app.config['TESTING'] = True
    return app


if __name__ == "__main__":
    application = create_app()
    application.run()
