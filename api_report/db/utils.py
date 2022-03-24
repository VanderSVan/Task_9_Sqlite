import os
import sys
from datetime import datetime as dt
from .exceptions import ImproperlyConfigured


def load_engine_sql(engine_name: str):
    module_name, sql_name = engine_name.rsplit('.', 1)
    __import__(module_name)
    all_imported_modules = sys.modules
    module = all_imported_modules[module_name]
    return getattr(module, sql_name)


def load_database(database_config: dict):
    try:
        database_name = database_config.pop('name')
        database_engine = database_config.pop('engine')
        database_path = os.path.join(database_config.pop('folder_path'), database_name)
    except KeyError:
        raise ImproperlyConfigured('Please specify a "name" and "engine" for your database')
    database_class = load_engine_sql(database_engine)
    return database_class(database_path, **database_config)


def timeit(func):
    """Timekeeper's decorator"""

    def wrapper(*args, **kwargs):
        start = dt.now()
        result = func(*args, **kwargs)
        print(dt.now() - start)
        return result

    return wrapper

