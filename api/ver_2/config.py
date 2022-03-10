class Configuration:
    DATABASE = {
        'name': 'race_info.db',
        'engine': 'peewee.SqliteDatabase',
    }
    SWAGGER = {
        'doc_dir': './api/docs/ver_2',
        "specs_route": "/api/v2"
    }
    DEBUG = True
    TESTING = False
