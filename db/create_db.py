import os
from reporting.report import create_drivers_dict
from datetime import datetime as dt

# data path initialization
project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_path = os.path.join(project_path, 'data_files')


def timeit(func):
    def wrapper(*args):
        start = dt.now()
        result = func(*args)
        print(dt.now() - start)
        return result

    return wrapper


@timeit
def create_tables(db, tables: list):
    with db:
        db.drop_tables(tables)
        db.create_tables(tables)
    print('Tables has been created in')


def create_data_for_db():
    race_info_dict = create_drivers_dict(data_path)  # data from files
    drivers_list = []
    teams_dict = {}
    race_result_list = []
    team_id = 1
    for counter, driver_info in enumerate(race_info_dict.values(), start=1):
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
def insert_records_to_db(db, tables):
    data_list = create_data_for_db()
    with db.atomic():
        for table, data in zip(tables, data_list):
            query_insert_drivers = table.insert_many(data)  # insert data to db
            query_insert_drivers.execute()
    print('Records has been added in')


def create_db(database, tables):
    """Main function"""
    create_tables(database, tables)
    insert_records_to_db(database, tables)
    print('*** db has been created ***', '\n')


if __name__ == '__main__':
    create_tables()
    insert_records_to_db()