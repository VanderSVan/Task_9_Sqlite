from peewee import Model
from api.ver_2.exceptions import ImproperlyConfigured
from api.ver_2.utils import load_engine_sql


class Database:
    def __init__(self, database_config, app=None, database=None, database_class=None):
        self.app = app
        self.database = database
        self.database_config = dict(database_config)
        self.database_class = database_class
        if not self.database:
            self.load_database()
        self.Model = self.get_model_class()

    def load_database(self):
        try:
            database_name = self.database_config.pop('name')
            database_engine = self.database_config.pop('engine')
        except KeyError:
            raise ImproperlyConfigured('Please specify a "name" and "engine" for your database')
        self.database_class = load_engine_sql(database_engine)
        self.database = self.database_class(database_name, **self.database_config)

    def get_model_class(self):
        class BaseModel(Model):
            class Meta:
                database = self.database
        return BaseModel

    def connect_db(self):
        if self.database.is_closed():
            self.database.connect()

    def close_db(self):
        if not self.database.is_closed():
            self.database.close()

    def register_handlers(self):
        self.app.before_request(self.connect_db())
        self.app.after_request(self.close_db())