import pytest
import json
import xmltodict as x2d
from collections import OrderedDict
from api_report.config import Configuration as Config

param_list_without_nulls = [
    ("SVF", {"abbreviation": "SVF",
             "driver_name": "Sebastian Vettel",
             "team_name": "FERRARI",
             "start_time": "2018-05-24 12:02:58.917000",
             "end_time": "2018-05-24 12:04:03.332000",
             "result_time": "00:01:04.415000"}),
    ("SPF", {"abbreviation": "SPF",
             "driver_name": "Sergio Perez",
             "team_name": "FORCE INDIA MERCEDES",
             "start_time": "2018-05-24 12:12:01.035000",
             "end_time": "2018-05-24 12:13:13.883000",
             "result_time": "00:01:12.848000"}),
    ("KMH", {"abbreviation": "KMH",
             "driver_name": "Kevin Magnussen",
             "team_name": "HAAS FERRARI",
             "start_time": "2018-05-24 12:02:51.003000",
             "end_time": "2018-05-24 12:04:04.396000",
             "result_time": "00:01:13.393000"})
]

param_list_with_nulls = [
    ('DRR', {'abbreviation': 'DRR',
             'driver_name': 'Daniel Ricciardo',
             'team_name': 'RED BULL RACING TAG HEUER',
             'start_time': '2018-05-24 12:14:12.054000',
             'end_time': '2018-05-24 12:11:24.067000',
             'result_time': None}),
    ('EOF', {'abbreviation': 'EOF',
             'driver_name': 'Esteban Ocon',
             'team_name': 'FORCE INDIA MERCEDES',
             'start_time': '2018-05-24 12:17:58.810000',
             'end_time': '2018-05-24 12:12:11.838000',
             'result_time': None})
]


@pytest.mark.parametrize('abbr, result', [param_list_without_nulls[0]])
class TestRaceReportDefault:
    # default
    def test_get_default_report(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(abbr) == result

    # default order is ascending
    def test_default_order(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert list(OrderedDict(json.loads(response.data)))[0] == abbr


class TestRaceReportExceptions:
    # Exceptions
    # order
    def test_get_wrong_order_default(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?order=wrong_order')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "order": "invalid value for 'order' parameter, select 'acs' or 'desc'"
        }

    def test_get_wrong_order_json(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?order=wrong_order&format=json')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "order": "invalid value for 'order' parameter, select 'acs' or 'desc'"
        }

    def test_get_wrong_order_xml(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?order=wrong_order&format=xml')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "order": "invalid value for 'order' parameter, select 'acs' or 'desc'"
        }

    # limit
    def test_get_wrong_limit_type_default(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?limit=abc')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "limit": "invalid literal for int() with base 10: 'abc'"
        }

    def test_get_wrong_limit_type_json(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=json&limit=abc')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "limit": "invalid literal for int() with base 10: 'abc'"
        }

    def test_get_wrong_limit_type_xml(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=xml&limit=abc')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "limit": "invalid literal for int() with base 10: 'abc'"
        }

    # offset
    def test_get_wrong_offset_type_default(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?offset=abc')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "offset": "invalid literal for int() with base 10: 'abc'"
        }

    def test_get_wrong_offset_type_json(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=json&offset=abc')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "offset": "invalid literal for int() with base 10: 'abc'"
        }

    def test_get_wrong_offset_type_xml(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=xml&offset=abc')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "offset": "invalid literal for int() with base 10: 'abc'"
        }

    # nulls
    def test_get_wrong_nulls_type_default(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?nulls=5')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "nulls": "invalid value for 'nulls' parameter, select 'yes' or 'no'"
        }

    def test_get_wrong_nulls_type_json(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?nulls=5&format=json')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "nulls": "invalid value for 'nulls' parameter, select 'yes' or 'no'"
        }

    def test_get_wrong_nulls_type_xml(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?nulls=5&format=xml')
        assert response.status_code == 400
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == {
            "nulls": "invalid value for 'nulls' parameter, select 'yes' or 'no'"
        }

    # format
    def test_get_wrong_format(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=bla_bla_bla')
        assert response.status_code == 404
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == "'bla_bla_bla' format is not supported"
        assert dict(json.loads(response.data)).get('status') == 404


@pytest.mark.parametrize("abbr, result", [param_list_without_nulls[0]])
class TestDriverInfoDefault:  # scope db connect = 'class'
    # default
    def test_get_driver_default(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/{abbr}/')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(abbr) == result


class TestDriverInfoExceptions:
    # Exceptions
    # wrong abbreviation
    def test_get_wrong_abbr_default(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/Unknown/')
        assert response.status_code == 404
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == "abbreviation 'Unknown' not found"

    def test_get_wrong_abbr_json(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/Unknown/?format=json')
        assert response.status_code == 404
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == "abbreviation 'Unknown' not found"

    def test_get_wrong_abbr_xml(self, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/Unknown/?format=xml')
        assert response.status_code == 404
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == "abbreviation 'Unknown' not found"

    # wrong format
    @pytest.mark.parametrize("abbr, result", [param_list_without_nulls[0]])
    def test_get_wrong_format(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/{abbr}/?format=bla_bla_bla')
        assert response.status_code == 404
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == "'bla_bla_bla' format is not supported"
        assert dict(json.loads(response.data)).get('status') == 404


@pytest.mark.parametrize('abbr, result', [param_list_without_nulls[1]])
class TestRaceReportJson:  # scope db connect = 'class'
    # json
    def test_get_json_report(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=json')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(abbr) == result

    # order
    def test_set_asc_order(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?order=asc')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert list(OrderedDict(json.loads(response.data)))[6] == abbr

    def test_set_desc_order(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?order=desc')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert list(OrderedDict(json.loads(response.data)))[8] == abbr

    # limit
    def test_set_limit(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?limit=7')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(abbr) == result

    def test_set_zero_limit(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?limit=0')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)) == {}

    def test_set_wrong_limit(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?limit=1000')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(abbr) == result

    # offset
    def test_set_offset(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?offset=2')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(abbr) == result

    def test_set_zero_offset(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?offset=0')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(abbr) == result

    def test_set_wrong_offset(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?offset=1000')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)) == {}

    # nulls
    @pytest.mark.parametrize('new_abbr, new_result', [param_list_with_nulls[0]])
    def test_allow_nulls(self, new_abbr, new_result, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?nulls=yes')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(new_abbr) == new_result

    def test_delete_nulls(self, abbr, result, client, connect_test_db):
        new_abbr = 'DRR'  # This is driver has not result_time
        response = client.get(f'{Config.API_URL}/drivers/?nulls=no')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(new_abbr) is None


@pytest.mark.parametrize('abbr, result', [param_list_without_nulls[2]])
class TestRaceReportXml:  # scope db connect = 'class'
    # xml
    def test_get_xml_report(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=xml')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('drivers_report').get(abbr) == result

    # order
    def test_set_asc_order(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?order=asc&format=xml')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert list(OrderedDict(x2d.parse(response.data)).get('drivers_report'))[14] == abbr

    def test_set_desc_order(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=xml&order=desc')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert list(OrderedDict(x2d.parse(response.data)).get('drivers_report'))[0] == abbr

    # limit
    def test_set_limit(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=xml&limit=15')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('drivers_report').get(abbr) == result

    def test_set_zero_limit(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=xml&limit=0')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)) == {'drivers_report': None}

    def test_set_wrong_limit(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=xml&limit=1000')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('drivers_report').get(abbr) == result

    # offset
    def test_set_offset(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=xml&offset=3')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('drivers_report').get(abbr) == result

    def test_set_zero_offset(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=xml&offset=0')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('drivers_report').get(abbr) == result

    def test_set_wrong_offset(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?format=xml&offset=1000')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)) == {'drivers_report': None}

    # nulls
    @pytest.mark.parametrize('new_abbr, new_result', [param_list_with_nulls[1]])
    def test_allow_nulls(self, new_abbr, new_result, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/?nulls=yes&format=xml')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('drivers_report').get(new_abbr) == new_result

    def test_delete_nulls(self, abbr, result, client, connect_test_db):
        new_abbr = 'EOF'  # This is driver has not result_time
        response = client.get(f'{Config.API_URL}/drivers/?nulls=no&format=xml')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('drivers_report').get(new_abbr) is None


@pytest.mark.parametrize("abbr, result", [param_list_without_nulls[0]])
class TestDriverInfoJson:  # scope db connect = 'class'
    # json
    def test_get_driver_json(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/{abbr}/?format=json')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(abbr) == result


@pytest.mark.parametrize("abbr, result", [param_list_without_nulls[1]])
class TestDriverInfoXml:
    def test_get_driver_xml(self, abbr, result, client, connect_test_db):
        response = client.get(f'{Config.API_URL}/drivers/{abbr}/?format=xml')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('driver').get(abbr) == result
