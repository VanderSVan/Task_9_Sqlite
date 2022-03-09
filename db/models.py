from peewee import *
from api.ver_2.init_database import Database
from api.ver_2.config import Configuration

db = Database(Configuration.DATABASE)


class Driver(db.Model):
    driver_id = PrimaryKeyField()
    first_name = CharField()
    last_name = CharField()

    @staticmethod
    def get_driver_info(abbr) -> dict or None:
        abbreviation = (fn.Substr(Driver.first_name, 1, 1)
                        .concat(fn.Substr(Driver.last_name, 1, 1))
                        .concat(fn.Substr(Team.team_name, 1, 1))
                        .alias('abbreviation'))
        driver_name = (Driver.first_name
                       .concat(" " + Driver.last_name)
                       .alias('driver_name'))
        try:
            with db:
                driver_query = (Driver
                                .select(abbreviation, driver_name, Team.team_name,
                                        RaceInfo.start_time, RaceInfo.end_time, RaceInfo.result_time)
                                .join(RaceInfo, on=(Driver.driver_id == RaceInfo.driver_id))
                                .join(Team, on=(Team.team_id == RaceInfo.team_id))
                                .where(abbreviation == str(abbr))
                                )
                return driver_query.dicts().get()
        except Driver.DoesNotExist:
            return None

    class Meta:
        db_table = 'drivers'


class Team(db.Model):
    team_id = PrimaryKeyField()
    team_name = TextField(unique=True)

    class Meta:
        db_table = 'teams'


class RaceInfo(db.Model):
    race_result_id = PrimaryKeyField()
    driver_id = ForeignKeyField(Driver, to_field='driver_id', lazy_load=False)
    team_id = ForeignKeyField(Team, to_field='team_id', lazy_load=False)
    start_time = DateTimeField()
    end_time = DateTimeField()
    result_time = TimeField(null=True)

    @staticmethod
    def get_race_info(order='asc', limit=None, offset=0, nulls=True) -> dict:
        abbreviation = (fn.Substr(Driver.first_name, 1, 1)
                        .concat(fn.Substr(Driver.last_name, 1, 1))
                        .concat(fn.Substr(Team.team_name, 1, 1))
                        .alias('abbreviation'))
        driver_name = (Driver.first_name
                       .concat(" " + Driver.last_name)
                       .alias('driver_name'))
        with db:
            race_info_query = (RaceInfo
                               .select(abbreviation, driver_name, Team.team_name,
                                       RaceInfo.start_time, RaceInfo.end_time, RaceInfo.result_time)
                               .join(Driver, on=(Driver.driver_id == RaceInfo.driver_id))
                               .join(Team, on=(Team.team_id == RaceInfo.team_id))
                               .where(RaceInfo.result_time.is_null(nulls) if not nulls else None)
                               .order_by(RaceInfo.result_time.desc(nulls='LAST') if order == 'desc'
                                         else RaceInfo.result_time.asc(nulls='LAST'))
                               .limit(limit)
                               .offset(offset)
                               ).dicts()
            return race_info_query.dicts()

    class Meta:
        db_table = 'races_info'
