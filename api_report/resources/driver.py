from flask_restful import Resource
from api_report.models import Driver
from .utils import create_response
from .handlers import handle_404_error_api
from .query_string_parser import QueryString


def get_driver_info(abbr: str) -> dict or None:
    """
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
