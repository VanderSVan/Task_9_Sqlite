from flask_restful import Resource
from api_report.db.models import Driver
from .utils import create_response
from .handlers import handle_404_error_api
from .query_string_parser import QueryString


def get_driver_info(abbr: str) -> dict or None:
    """
    Main function.
    Uses function 'get_driver_info' from Driver's Model.
    This function creates db query to get driver's info.
    Driver's info contains the following schema as example:
    {'SVF': {'abbreviation': 'SVF',
             'driver_name': 'Sebastian Vettel',
             'team_name': 'FERRARI',
             'start_time': datetime.datetime(2018, 5, 24, 12, 2, 58, 917000),
             'end_time': datetime.datetime(2018, 5, 24, 12, 4, 3, 332000),
             'result_time': datetime.time(0, 1, 4, 415000)}, ...
    }
    :return: driver's info as dictionary, prepared to be converted to json or xml
             or will return None if abbreviation is not exists.
    """
    driver_info_dict = Driver.get_driver_info(abbr.upper())
    if driver_info_dict:
        result_driver_info = {driver_info_dict.get('abbreviation'): driver_info_dict}
        result = {'driver': result_driver_info} if QueryString.get_format() == 'xml' else result_driver_info
    else:
        result = None
    return result


class DriverInfo(Resource):
    def get(self, abbreviation: str):
        """
        file: docs/Driver/get.yml
        """
        driver_info = get_driver_info(abbreviation)
        if driver_info:
            return create_response(driver_info, QueryString.get_format())
        error = f"abbreviation '{abbreviation}' not found"
        return handle_404_error_api(error)
