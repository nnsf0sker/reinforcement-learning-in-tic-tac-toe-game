import pytest

from referee import Referee


@pytest.mark.parametrize(
    'field_adapter_settings,expected_possible_fields_n',
    [
        ((1, 1, 1), 1),
        ((2, 1, 1), 1),
        ((1, 2, 1), 1),
        ((2, 1, 2), 3),
        ((1, 2, 2), 3),
    ]
)
def test_all_possible_fields_method(field_adapter_settings, expected_possible_fields_n):
    field_adapter = Referee(*field_adapter_settings)
    result_possible_fields_n = sum(1 for _ in field_adapter.all_possible_fields())
    assert result_possible_fields_n == expected_possible_fields_n


@pytest.mark.parametrize(
    'field_adapter_settings,field,expected_result',
    [
        ((3, 3, 3), (0, 0, 0, 0, 0, 0, 0, 0, 0), 0),
        ((3, 3, 3), (1, 0, 0, 0, 0, 2, 1, 2, 1), 0),
        ((3, 3, 3), (1, 2, 1, 1, 2, 2, 1, 0, 0), 1),
        ((3, 3, 3), (2, 2, 1, 2, 1, 2, 1, 2, 1), 1),
        ((3, 3, 3), (2, 2, 2, 2, 1, 1, 1, 2, 1), 2),
    ],
)
def test_check_field_method(field_adapter_settings, field, expected_result):
    field_adapter = Referee(*field_adapter_settings)
    result = field_adapter.check_field(field)
    assert result == expected_result
