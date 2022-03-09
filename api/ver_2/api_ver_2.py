import json
import xmltodict as x2d
from flask import Blueprint, make_response, jsonify
from flask_restful import Resource, reqparse
from datetime import datetime, time
from db.models import Driver, RaceInfo

api_report_2 = Blueprint('api_v2', __name__)

# datetime format initialization
datetime_format = "%Y-%m-%d %H:%M:%S.%f"
time_format = "%H:%M:%S.%f"

# request parsers
order_parser = reqparse.RequestParser()
truncation_parser = reqparse.RequestParser()
format_parser = reqparse.RequestParser()
params_parser = reqparse.RequestParser()

# arguments in the query-string
order_parser.add_argument('order', type=str, default='asc', choices=['asc', 'desc'],
                          help="invalid value for 'order' parameter, select 'acs' or 'desc'")
truncation_parser.add_argument('limit', type=int, default=None, help='it is impossible to set a limit')
truncation_parser.add_argument('offset', type=int, default=0, help='it is impossible to set a offset')
truncation_parser.add_argument('nulls', type=str, default='yes', choices=['yes', 'no'],
                               help="invalid value for 'nulls' parameter, select 'yes' or 'no'")
format_parser.add_argument('format', type=str, default='json', help='this format is not supported')


def handle_404_error_api(error=None):
    if error:
        return make_response(jsonify({'status': 404, 'message': str(error)}), 404)
    return make_response(jsonify({'status': 404, 'message': 'Not found'}), 404)


class DriverEncoder(json.JSONEncoder):
    """Encode datetime and time to json string correctly."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime(datetime_format)
        elif isinstance(obj, time):
            return obj.strftime(time_format)
        return json.JSONEncoder.default(self, obj)


def get_driver_info(abbr: str) -> dict or None:
    """
    """
    format_output = format_parser.parse_args().format.lower()
    driver = Driver()
    driver_info_dict = driver.get_driver_info(abbr.upper())
    if driver_info_dict:
        result_driver_info = {driver_info_dict.get('abbreviation'): driver_info_dict}
        result = {'driver': result_driver_info} if format_output == 'xml' else result_driver_info
    else:
        result = None
    return result


def get_race_info() -> dict:
    """
    """
    format_output = format_parser.parse_args().format.lower()
    order = order_parser.parse_args().order.lower()
    truncation_args = truncation_parser.parse_args()
    race = RaceInfo()
    race_info_dict = race.get_race_info(order=order, limit=truncation_args.limit,
                                        offset=truncation_args.offset,
                                        nulls=True if truncation_args.nulls.lower() == 'yes' else False)
    result_race_info = {driver_info.get('abbreviation'): driver_info for driver_info in race_info_dict}
    return {'drivers_report': result_race_info} if format_output == 'xml' else result_race_info


def create_response(report: dict):
    """
    """
    format_args = format_parser.parse_args()
    if format_args.format.lower() == 'xml':
        xml_format = x2d.unparse(report, encoding='UTF-8', pretty=True)
        response = make_response(xml_format, 200)
        response.mimetype = "application/xml"
    elif format_args.format.lower() == 'json':
        json_format = json.dumps(report, cls=DriverEncoder,
                                 indent='\t', ensure_ascii=False)
        response = make_response(json_format, 200)
        response.mimetype = "application/json"
    else:
        error = f"'{format_args.format}' format is not supported"
        return handle_404_error_api(error)
    return response


class DriversReport(Resource):
    def get(self):
        """
        file: docs/Drivers/get.yml
        """
        drivers_report = get_race_info()
        return create_response(drivers_report)


class DriverStats(Resource):
    def get(self, abbreviation: str):
        """
        file: docs/DriverStats/get.yml
        """
        driver_info = get_driver_info(abbreviation)
        if driver_info:
            return create_response(driver_info)
        error = f"abbreviation '{abbreviation}' not found"
        return handle_404_error_api(error)
