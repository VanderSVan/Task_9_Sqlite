from flask_restful import Resource
from api_report.db.models import RaceInfo
from .utils import create_response
from .query_string_parser import QueryString


def get_race_info() -> dict:
    """
    Main function.
    Uses function 'get_race_info' from RaceInfo's Model.
    This function creates db query to get race report.
    Report contains the following schema as example:
    {'SVF': {'abbreviation': 'SVF',
             'driver_name': 'Sebastian Vettel',
             'team_name': 'FERRARI',
             'start_time': datetime.datetime(2018, 5, 24, 12, 2, 58, 917000),
             'end_time': datetime.datetime(2018, 5, 24, 12, 4, 3, 332000),
             'result_time': datetime.time(0, 1, 4, 415000)}, ...
    }
    Report can be modified by params:
     - order: asc(ascending), desc(descending)
     - limit: any int (truncates number of drivers by limit)
     - offset: any int (truncates number of drivers by offset)
     - nulls: 'yes' or 'no' (outputs null values or not)
    :return: race report as dictionary, prepared to be converted to json or xml
    """
    race_info_dict = RaceInfo.get_race_info(order=QueryString.get_order(),
                                            limit=QueryString.get_limit(),
                                            offset=QueryString.get_offset(),
                                            nulls=True if QueryString.get_nulls() == 'yes' else False)
    result_race_info = {driver_info.get('abbreviation'): driver_info for driver_info in race_info_dict}
    return {'drivers_report': result_race_info} if QueryString.get_format() == 'xml' else result_race_info


class RaceReport(Resource):
    def get(self):
        """
        file: docs/RaceReport/get.yml
        """
        drivers_report = get_race_info()
        return create_response(drivers_report, QueryString.get_format())
