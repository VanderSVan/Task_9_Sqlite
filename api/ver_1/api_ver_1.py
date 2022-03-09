import os
import json
import xmltodict as x2d
from flask import Blueprint, make_response, jsonify
from flask_restful import Resource, reqparse
from marshmallow import Schema, fields
from datetime import datetime
from collections import OrderedDict as ODict
from reporting.report import create_drivers_dict
from reporting.report import sort_drivers_dict
from reporting.report import Driver

api_report = Blueprint('api', __name__)

# data initialization
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
folder_path = os.path.join(project_path, 'data_files')
try:
    drivers = create_drivers_dict(folder_path)
except Exception as err:
    print(' * !!!ATTENTION!!! * \n * [ERROR =', err, '] * ')
    drivers = {}

datetime_format = "%Y-%m-%d %I:%M:%S.%f"
order_parser = reqparse.RequestParser()
cutting_parser = reqparse.RequestParser()
format_parser = reqparse.RequestParser()
params_parser = reqparse.RequestParser()
order_parser.add_argument('order', type=str, default='asc', help='it is impossible to establish this order')
cutting_parser.add_argument('limit', type=int, default=None, help='it is impossible to set a limit')
cutting_parser.add_argument('offset', type=int, default=0, help='it is impossible to set a offset')
format_parser.add_argument('format', type=str, default='json', help='this format is not supported')
params_parser.add_argument('params', type=str, default=None, help='it is impossible to set a params')


def handle_404_error_api(error):
    if error:
        return make_response(jsonify({'status': 404, 'message': str(error)}), 404)
    return make_response(jsonify({'status': 404, 'message': 'Not found'}), 404)


class DriverEncoder(json.JSONEncoder):
    """Encode datetime to json string correctly."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime(datetime_format)
        return json.JSONEncoder.default(self, obj)


def set_limit_and_offset(report: dict, limit: int, offset: int) -> ODict:
    """
    Truncates the dictionary by two parameters: limit and offset.
    :param report: Driver dict.
    :param limit: amount drivers.
    :param offset: where to start.
    :return: ordered dict.
    """
    if limit:
        limit = offset + limit
    return ODict(list(report.items())[offset:limit])


class DriverSchema(Schema):
    abbr = fields.Str()
    name = fields.Str()
    team = fields.Str()
    start = fields.DateTime(datetime_format)
    end = fields.DateTime(datetime_format)
    time = fields.Function(lambda obj: str(obj.time))

    class Meta:
        ordered = True


def get_driver_params(driver: Driver, params=None) -> ODict:
    """
    Converts an instance of the 'Driver' class into a dictionary.
    :param driver: instance of the 'Driver' class.
    :param params: parameters which to should add. If 'None', all parameters will be added.
    :return: ordered dictionary with driver parameters.
    """
    if params:
        params = params.lower()
        params_list = params.split(',')
        clean_params_list = [param.strip() for param in params_list if hasattr(driver, param.strip())]
        driver_schema = DriverSchema(only=clean_params_list)
    else:
        driver_schema = DriverSchema()
    return driver_schema.dump(driver)


def data_process(data, abbr=None) -> dict:
    """
    Main function.
    Processing input data with the required parameters.
    :param data: driver info or report of drivers.
    :param abbr: driver abbreviation.
    :return: processed report.
    """
    format_args = format_parser.parse_args()
    params_args = params_parser.parse_args()
    if abbr:
        processed_data = get_driver_params(data, params_args.params)
        if format_args.format.lower() == 'xml':
            processed_data = {abbr: processed_data}
    else:
        cutting_args = cutting_parser.parse_args()
        if cutting_args.limit or cutting_args.offset:
            data = set_limit_and_offset(data, cutting_args.limit, cutting_args.offset)
        processed_data = {abbr: get_driver_params(driver, params_args.params) for abbr, driver in
                          data.items()}
        if format_args.format.lower() == 'xml':
            processed_data = {'drivers_report': processed_data}
    return processed_data


def create_response(report: dict):
    """
    Create response as xml or json format.
    :param report: driver report or drivers report.
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


class Drivers(Resource):
    def get(self):
        """
        file: docs/Drivers/get.yml
        """
        order_args = order_parser.parse_args()
        drivers_report = sort_drivers_dict(drivers, desc=order_args.order.lower() == 'desc')
        sorted_drivers_report = data_process(drivers_report)
        return create_response(sorted_drivers_report)


class DriverStats(Resource):
    def get(self, abbreviation: str):
        """
        file: docs/DriverStats/get.yml
        """
        abbr = abbreviation.upper()
        driver = drivers.get(abbr)
        if not driver:
            error = f"Abbreviation '{abbr}' not found"
            return handle_404_error_api(error)
        driver_info = data_process(driver, abbreviation)
        return create_response(driver_info)
