import os

# Project path initialization.
project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
current_folder = os.path.dirname(os.path.realpath(__file__))


class Configuration:
    DATABASE = {
        'folder_path': current_folder,
        'name': 'race_info.db',
        'engine': 'peewee.SqliteDatabase',
    }
    SWAGGER = {
        'doc_dir': 'api_report/resources/docs/',
        "specs_route": "/api_report"
    }
    DATA = {
        'folder_path': os.path.join(project_path, 'data_files')
    }
    DEBUG = True
    TESTING = False
    API_URL = "/api_report"
