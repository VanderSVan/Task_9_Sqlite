from flask_restful import Resource
from api_report.models import RaceInfo
from .utils import create_response
from .query_string_parser import QueryString


def get_race_info() -> dict:
    """
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
