import pytest
from peewee import SqliteDatabase
from src.api_report.app import create_app
from src.api_report.db import Driver, Team, RaceInfo
from src.api_report.db.insert_records import db_data_prepare

MODELS = [Driver, Team, RaceInfo]
test_db = SqliteDatabase(':memory:')
data_list = db_data_prepare()


@pytest.fixture
def app():
    return create_app(test_config=True)


@pytest.fixture
def client(app):
    app.config['DEBUG'] = False
    return app.test_client()


@pytest.fixture(scope='class')
def connect_test_db():
    """Fixture to connect and disconnect database for each test class"""
    test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
    with test_db:
        # setup
        test_db.drop_tables(MODELS)
        test_db.create_tables(MODELS)
        for table, data in zip(MODELS, data_list):
            data_insert_query = table.insert_many(data)  # insert data to db
            data_insert_query.execute()
        yield
        # teardown
