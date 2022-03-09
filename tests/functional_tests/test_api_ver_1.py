import pytest
import json
import xmltodict as x2d
from collections import OrderedDict


@pytest.mark.parametrize('abbr, result', [
    ('EOF', {'abbr': 'EOF',
             'name': 'Esteban Ocon',
             'team': 'FORCE INDIA MERCEDES',
             'start': '2018-05-24 12:17:58.810000',
             'end': '2018-05-24 01:12:11.838000',
             'time': '0:54:13.028000'})
])
class TestDriversJson:
    def test_get_report(self, abbr, result, client):
        response = client.get('/api/v1/drivers/')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(abbr) == result

    def test_default_order(self, abbr, result, client):
        response = client.get('/api/v1/drivers/')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert list(OrderedDict(json.loads(response.data)))[1] == abbr

    def test_set_order(self, abbr, result, client):
        response = client.get('api/v1/drivers/?order=desc')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert list(OrderedDict(json.loads(response.data)))[17] == abbr

    def test_set_limit(self, abbr, result, client):
        response = client.get('api/v1/drivers/?limit=2')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(abbr) == result

    def test_set_offset(self, abbr, result, client):
        response = client.get('api/v1/drivers/?offset=1')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get(abbr) == result

    @pytest.mark.parametrize("new_abbr, result2", [
        ('DRR', {'name': 'Daniel Ricciardo',
                 'team': 'RED BULL RACING TAG HEUER',
                 'time': '0:57:12.013000'})
    ])
    def test_set_params(self, new_abbr, result2, abbr, result, client):
        response = client.get('api/v1/drivers/?params=name,team,time')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert OrderedDict(json.loads(response.data)).get(new_abbr) == result2


@pytest.mark.parametrize('abbr, result', [
    ('VBM', OrderedDict({'abbr': 'VBM',
                         'name': 'Valtteri Bottas',
                         'team': 'MERCEDES',
                         'start': '2018-05-24 12:00:00.000000',
                         'end': '2018-05-24 01:01:12.434000',
                         'time': '1:01:12.434000'}))
])
class TestDriversXml:
    def test_get_report(self, abbr, result, client):
        response = client.get('/api/v1/drivers/?format=xml')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('drivers_report').get(abbr) == result

    def test_default_order(self, abbr, result, client):
        response = client.get('/api/v1/drivers/?format=xml')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert list(OrderedDict(x2d.parse(response.data)).get('drivers_report'))[5] == abbr

    def test_set_order(self, abbr, result, client):
        response = client.get('/api/v1/drivers/?format=xml&order=desc')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert list(OrderedDict(x2d.parse(response.data)).get('drivers_report'))[13] == abbr

    def test_set_limit(self, abbr, result, client):
        response = client.get('api/v1/drivers/?format=xml&limit=6')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('drivers_report').get(abbr) == result

    def test_set_offset(self, abbr, result, client):
        response = client.get('api/v1/drivers/?format=xml&offset=5')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('drivers_report').get(abbr) == result

    @pytest.mark.parametrize("new_abbr, result2", [
        ('KRF', {'name': 'Kimi Räikkönen',
                 'team': 'FERRARI',
                 'time': '1:01:12.639000'})
    ])
    def test_set_params(self, new_abbr, result2, abbr, result, client):
        response = client.get('api/v1/drivers/?format=xml&params=name,team,time')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert dict(x2d.parse(response.data)).get('drivers_report').get(new_abbr) == result2


class TestDriverStatsJson:
    @pytest.mark.parametrize("abbr, result", [
        ('CLS', {'abbr': 'CLS',
                 'end': '2018-05-24 01:10:54.750000',
                 'name': 'Charles Leclerc',
                 'start': '2018-05-24 12:09:41.921000',
                 'team': 'SAUBER FERRARI',
                 'time': '1:01:12.829000'})
    ])
    def test_get_driver(self, abbr, result, client):
        response = client.get(f'api/v1/drivers/{abbr}/')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert OrderedDict(json.loads(response.data)) == result

    @pytest.mark.parametrize("abbr, result", [
        ('RGH', {'name': 'Romain Grosjean',
                 'team': 'HAAS FERRARI',
                 'time': '1:01:12.930000'})
    ])
    def test_set_params(self, abbr, result, client):
        response = client.get(f'api/v1/drivers/{abbr}/?params=name,team,time')
        assert response.status_code == 200
        assert 'application/json' in response.headers['Content-Type']
        assert OrderedDict(json.loads(response.data)) == result

    def test_get_wrong_abbr(self, client):
        response = client.get('api/v1/drivers/Unknown/')
        assert response.status_code == 404
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == "Abbreviation 'UNKNOWN' not found"


class TestDriverStatsXml:
    @pytest.mark.parametrize("abbr, result", [
        ('CSR', OrderedDict([('abbr', 'CSR'),
                             ('name', 'Carlos Sainz'),
                             ('team', 'RENAULT'),
                             ('start', '2018-05-24 12:03:15.145000'),
                             ('end', '2018-05-24 01:04:28.095000'),
                             ('time', '1:01:12.950000')]))
    ])
    def test_get_driver(self, abbr, result, client):
        response = client.get(f'api/v1/drivers/{abbr}/?format=xml')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert OrderedDict(x2d.parse(response.data)).get(abbr) == result

    @pytest.mark.parametrize("abbr, result", [
        ('BHS', OrderedDict([('name', 'Brendon Hartley'),
                             ('team', 'SCUDERIA TORO ROSSO HONDA'),
                             ('time', '1:01:13.179000')]))
    ])
    def test_set_params(self, abbr, result, client):
        response = client.get(f'api/v1/drivers/{abbr}/?format=xml&params=name,team,time')
        assert response.status_code == 200
        assert 'application/xml' in response.headers['Content-Type']
        assert OrderedDict(x2d.parse(response.data)).get(abbr) == result

    def test_get_wrong_abbr(self, client):
        response = client.get('api/v1/drivers/Unknown/?format=xml')
        assert response.status_code == 404
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data))['message'] == "Abbreviation 'UNKNOWN' not found"


class TestGetWrongFormat:
    def test_get_wrong_format(self, client):
        response = client.get('api/v1/drivers/?format=Something')
        assert response.status_code == 404
        assert 'application/json' in response.headers['Content-Type']
        assert dict(json.loads(response.data)).get('message') == "'Something' format is not supported"
        assert dict(json.loads(response.data)).get('status') == 404