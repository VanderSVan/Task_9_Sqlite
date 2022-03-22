from flask_restful import reqparse

# request parsers
order_parser = reqparse.RequestParser()
truncation_parser = reqparse.RequestParser()
format_parser = reqparse.RequestParser()
params_parser = reqparse.RequestParser()

# arguments in the query-string
order_parser.add_argument('order', type=str, default='asc', choices=['asc', 'desc'],
                          help="invalid value for 'order' parameter, select 'acs' or 'desc'")
truncation_parser.add_argument('limit', type=int, default=None,
                               help='it is impossible to set a limit')
truncation_parser.add_argument('offset', type=int, default=0,
                               help='it is impossible to set a offset')
truncation_parser.add_argument('nulls', type=str, default='yes', choices=['yes', 'no'],
                               help="invalid value for 'nulls' parameter, select 'yes' or 'no'")
format_parser.add_argument('format', type=str, default='json',
                           help='this format is not supported')


class QueryString:
    @staticmethod
    def get_order():
        return order_parser.parse_args().order.lower()

    @staticmethod
    def get_format():
        return format_parser.parse_args().format.lower()

    @staticmethod
    def get_limit():
        return truncation_parser.parse_args().limit

    @staticmethod
    def get_offset():
        return truncation_parser.parse_args().offset

    @staticmethod
    def get_nulls():
        return truncation_parser.parse_args().nulls.lower()
