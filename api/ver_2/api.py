from application import create_app
from db.create_db import create_db
from db.models import db, Driver, Team, RaceInfo

app = create_app(test_config=True)
new_db = db(app=app)
database_tables = [Driver, Team, RaceInfo]

if __name__ == "__main__":
    create_db(new_db, database_tables)
    app.run()