from .app import create_app
from .app import db, Driver, Team, RaceInfo
from .app import insert_records_to_db

# Create database
database_tables = [Driver, Team, RaceInfo]
insert_records_to_db(db, database_tables)
# Create app
app = create_app()
app.run()
