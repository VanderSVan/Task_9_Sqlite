import pytest
from unittest.mock import patch
from datetime import datetime as dt
from datetime import timedelta as td
from src.api_report.db.insert_records import db_data_prepare
from reporting.report import Driver

input_params = {'SVF': Driver(abbr='SVF',
                              name='Sebastian Vettel',
                              team='FERRARI',
                              start=dt(2018, 5, 24, 12, 2, 58, 917000),
                              end=dt(2018, 5, 24, 12, 4, 3, 332000)),
                'VBM': Driver(abbr='VBM',
                              name='Valtteri Bottas',
                              team='MERCEDES',
                              start=dt(2018, 5, 24, 12, 0),
                              end=dt(2018, 5, 24, 12, 1, 12, 434000)),
                'KRF': Driver(abbr='KRF',
                              name='Kimi Räikkönen',
                              team='FERRARI',
                              start=dt(2018, 5, 24, 12, 3, 1, 250000),
                              end=dt(2018, 5, 24, 12, 4, 13, 889000))
                }

output_list_for_normal_mode = [[{'driver_id': 1, 'first_name': 'Sebastian', 'last_name': 'Vettel'},
                                {'driver_id': 2, 'first_name': 'Valtteri', 'last_name': 'Bottas'},
                                {'driver_id': 3, 'first_name': 'Kimi', 'last_name': 'Räikkönen'}],
                               [{'team_id': 1, 'team_name': 'FERRARI'},
                                {'team_id': 2, 'team_name': 'MERCEDES'}],
                               [{'race_result_id': 1,
                                 'driver_id': 1,
                                 'team_id': 1,
                                 'start_time': dt(2018, 5, 24, 12, 2, 58, 917000),
                                 'end_time': dt(2018, 5, 24, 12, 4, 3, 332000),
                                 'result_time': td(seconds=64, microseconds=415000)},
                                {'race_result_id': 2,
                                 'driver_id': 2,
                                 'team_id': 2,
                                 'start_time': dt(2018, 5, 24, 12, 0),
                                 'end_time': dt(2018, 5, 24, 12, 1, 12, 434000),
                                 'result_time': td(seconds=72, microseconds=434000)},
                                {'race_result_id': 3,
                                 'driver_id': 3,
                                 'team_id': 1,
                                 'start_time': dt(2018, 5, 24, 12, 3, 1, 250000),
                                 'end_time': dt(2018, 5, 24, 12, 4, 13, 889000),
                                 'result_time': td(seconds=72, microseconds=639000)}
                                ]]

output_list_for_cut_mode = [[{'driver_id': 1, 'first_name': 'Valtteri', 'last_name': 'Bottas'}],
                             [{'team_id': 1, 'team_name': 'MERCEDES'}],
                             [{'race_result_id': 1,
                               'driver_id': 1,
                               'team_id': 1,
                               'start_time': dt(2018, 5, 24, 12, 0),
                               'end_time': dt(2018, 5, 24, 12, 1, 12, 434000),
                               'result_time': td(seconds=72, microseconds=434000)}
                              ]]


@pytest.mark.parametrize('params, normal_mode_result, cut_mode_result',
                         [(input_params, output_list_for_normal_mode, output_list_for_cut_mode)])
@patch("api_report.db.insert_records.create_drivers_dict")
class TestDbDataPrepare:
    def test_correct_work(self, mock_drivers_dict, params, normal_mode_result, cut_mode_result):
        mock_drivers_dict.return_value = params
        assert db_data_prepare() == normal_mode_result

    def test_cut_mode(self, mock_drivers_dict, params, normal_mode_result, cut_mode_result):
        mock_drivers_dict.return_value = params
        assert db_data_prepare(limit=1, offset=1) == cut_mode_result
