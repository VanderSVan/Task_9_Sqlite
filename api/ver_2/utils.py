import sys
from pprint import pprint


def load_engine_sql(engine_name: str):
    module_name, sql_name = engine_name.rsplit('.', 1)
    __import__(module_name)
    all_imported_modules = sys.modules
    module = all_imported_modules[module_name]
    return getattr(module, sql_name)


# d = {
#         'name': 'race_info.db',
#         'engine': 'peewee.SqliteDatabase',
#     }
# hui = load_engine_sql('peewee.SqliteDatabase')
# print(hui)
# new_hui = hui('race_info.db', **d)
# print(new_hui)
# # print(new_hui.name)





# # pprint(new_hui.__dict__)
# for key, value in new_hui.__dict__.items():
#     if value == "race_info.db" or key == 'race_info.db':
#         print('k =', key, 'v =', value)
#     if value == "SqliteDatabase" or key == 'SqliteDatabase':
#         print('k =', key, 'v =', value)
#
# pprint(new_hui.connect_params)