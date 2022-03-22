# from marshmallow import Schema, fields
# from reporting.report import create_drivers_dict
# from config import Configuration
#
# # Data path initialization.
# folder_data_path = Configuration.DATA['folder_path']
#
# # datetime format initialization
# datetime_format = "%Y-%m-%d %H:%M:%S.%f"
# time_format = "%H:%M:%S.%f"
#
#
# def validate_name(value):
#
#
# class TeamSchema(Schema):
#
#
#     team_id = fields.Integer(dump_only=True)
#     team = fields.Str(validate=[])
#
#
# class RaceInfoSchema(Schema):
#     abbr = fields.Str()
#     name = fields.Str()
#     team = fields.Nested(TeamSchema)
#     start = fields.DateTime(datetime_format)
#     end = fields.DateTime(datetime_format)
#     time = fields.Function(lambda obj: str(obj.time))
#
#
#
#
# def probably_testt():
#     race_info_dict = create_drivers_dict(folder_data_path)
#     # print(list(**race_info_dict))
#     team_schema = TeamSchema(many=True)
#     # race_info_schema = RaceInfoSchema(many=True, team=team_schema)
#     # print(race_info_dict)
#     return team_schema.dump(race_info_dict.values())
#     # return race_info_schema.dump(race_info_dict.values())
#
#
# print(probably_testt())
