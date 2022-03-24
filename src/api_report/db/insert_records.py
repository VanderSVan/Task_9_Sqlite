from reporting.report import create_drivers_dict
from src.api_report.db.utils import timeit
from src.api_report.config import Configuration


# Data path initialization.
folder_data_path = Configuration.DATA['folder_path']


@timeit
def create_tables(db, tables: list):
    """Drops existing tables and creates new tables"""
    with db:
        db.drop_tables(tables)
        db.create_tables(tables)
    print('Tables has been created in')


def db_data_prepare(limit=None, offset=0) -> [list, list, list]:
    """
    Gets data from files and prepares it for insertion into db.
    If you want to insert a limited amount of data into the db,
    you can set 'limit' and 'offset' options.
    :param limit: limits the amount of data.
    :param offset: skips data according to offset.
    :return: list of lists.
    """
    # convert data files to dict, where the key is the driver's abbreviation
    race_info_dict = create_drivers_dict(folder_data_path)
    if limit or offset:
        # Entering to cut mode
        race_list = list(race_info_dict.values())
        # truncate race_list using slicing method
        race_report = race_list[offset:(limit if limit is None else limit + offset)]
    else:
        race_report = race_info_dict.values()
    drivers_list = []
    teams_dict = {}
    race_result_list = []
    team_id = 1
    for counter, driver_info in enumerate(race_report, start=1):
        full_name = driver_info.name.split()
        drivers_list.append({'driver_id': counter, 'first_name': full_name[0], 'last_name': full_name[1]})
        if driver_info.team not in teams_dict:
            teams_dict[driver_info.team] = team_id
            team_id += 1
        race_result_list.append({'race_result_id': counter, 'driver_id': counter,
                                 'team_id': teams_dict[driver_info.team],
                                 'start_time': driver_info.start,
                                 'end_time': driver_info.end,
                                 'result_time': driver_info.time})
    teams_list = [{'team_id': team_id, 'team_name': team_name} for team_name, team_id in teams_dict.items()]
    return [drivers_list, teams_list, race_result_list]


@timeit
def insert_records_to_db(database, tables):
    """Get prepared data and insert it into db."""
    data_list = db_data_prepare()
    create_tables(database, tables)
    with database.atomic():
        for table, data in zip(tables, data_list):
            data_insert_query = table.insert_many(data)  # insert data to db
            data_insert_query.execute()
    print('Records has been added in')


if __name__ == '__main__':
    from pprint import pp
    pp(db_data_prepare(limit=5, offset=5), indent=2)
