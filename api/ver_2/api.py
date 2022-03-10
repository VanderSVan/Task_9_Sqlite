from application import create_app
from api.ver_2.db import create_db
from api.ver_2.db import db, Driver, Team, RaceInfo

app = create_app(test_config=True)
new_db = db(app=app)
database_tables = [Driver, Team, RaceInfo]

if __name__ == "__main__":
    create_db(new_db, database_tables)
