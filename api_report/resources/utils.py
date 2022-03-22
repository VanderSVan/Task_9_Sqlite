import json
import xmltodict as x2d
from flask import make_response
from datetime import datetime, time
from .handlers import handle_404_error_api

# datetime format initialization
datetime_format = "%Y-%m-%d %H:%M:%S.%f"
time_format = "%H:%M:%S.%f"


class DriverEncoder(json.JSONEncoder):
    """Encode datetime and time to json string correctly."""

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime(datetime_format)
        elif isinstance(obj, time):
            return obj.strftime(time_format)
        return json.JSONEncoder.default(self, obj)


def create_response(report: dict, output_format):
    """
    """
    if output_format == 'xml':
        xml_format = x2d.unparse(report, encoding='UTF-8', pretty=True)
        response = make_response(xml_format, 200)
        response.mimetype = "application/xml"
    elif output_format == 'json':
        json_format = json.dumps(report, cls=DriverEncoder,
                                 indent='\t', ensure_ascii=False)
        response = make_response(json_format, 200)
        response.mimetype = "application/json"
    else:
        error = f"'{output_format}' format is not supported"
        return handle_404_error_api(error)
    return response
