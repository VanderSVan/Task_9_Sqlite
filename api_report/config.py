import os

# Project path initialization.
current_folder = os.path.dirname(os.path.realpath(__file__))


class Configuration:
    DATABASE = {
        'folder_path': current_folder,
        'name': 'race_info.db',
        'engine': 'peewee.SqliteDatabase',
    }
    DATA = {
        'folder_path': os.path.join(current_folder, 'data_files')
    }
    API_URL = "/api/v1"
    SWAGGER = {
        'doc_dir': 'api_report/resources/docs/',
        "specs_route": API_URL
    }
    DEBUG = True
    TESTING = False
