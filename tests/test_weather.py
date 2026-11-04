"""Starter tests for the weather module.
"""
import pytest

from weather import (
    average_temperature,
    filter_by_temperature,
    hottest_measurement,
    parse_measurement,
    parse_time,
)

def test_parse_time_returns_int():
    assert isinstance(parse_time("14:21"), int)

def test_parse_time_regular_time():
    assert parse_time("14:21") == 861
    
def test_parse_time_midnight():
    assert parse_time("00:00") == 0
    
def test_parse_time_before_midnight():
    assert parse_time("23:59") == 1439
    
def test_parse_24_hours():
    with pytest.raises(ValueError):
        parse_time("24:00")

def test_parse_time_minute_60():
    with pytest.raises(ValueError):
        parse_time("00:60")

# def test_parse_time_both():
    #with pytest.raises(ValueError):
        #parse_time("24:60")

def test_parse_time_without_leading_zeros():
    assert parse_time("9:5") == 545

def test_parse_time_missing_colon():
    with pytest.raises(ValueError):
        parse_time("1421")

def test_parse_time_too_many_colons():
    with pytest.raises(ValueError):
        parse_time("14:21:00")


def test_parse_time_hour_not_numeric():
    with pytest.raises(ValueError):
        parse_time("ab:21")

def test_parse_time_minute_not_numeric():
    with pytest.raises(ValueError):
        parse_time("14:cd")

def test_parse_time_hour_missing():
    with pytest.raises(ValueError):
        parse_time(":21")


def test_parse_time_minute_missing():
    with pytest.raises(ValueError):
        parse_time("14:")


def test_parse_time_empty_text():
    with pytest.raises(ValueError):
        parse_time("")


def test_parse_measurement_regular_line():
    assert parse_measurement("Köln;14:21;21.7") == ("Köln", 861, 21.7)
    

def test_parse_measurement_temperature_is_float():
    city, time, temperature = parse_measurement("Köln;14:21;20")
    assert temperature == 20.0
    assert isinstance(temperature, float)


def test_parse_measurement_not_a_string():
    with pytest.raises(ValueError):
        parse_measurement(42)


def test_parse_measurement_two_fields():
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21")


def test_parse_measurement_four_fields():
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21;21.7;x")


def test_parse_measurement_whitespace_around_fields():
    assert parse_measurement(" Köln ; 14:21 ; 21.7 ") == ("Köln", 861, 21.7)

def test_parse_measurement_space_inside_city_stays():
    assert parse_measurement("Bad Honnef;14:21;21.7") == ("Bad Honnef", 861, 21.7)


def test_parse_measurement_city_only_spaces():
    with pytest.raises(ValueError):
        parse_measurement("   ;14:21;21.7")


def test_parse_measurement_invalid_time():
    with pytest.raises(ValueError):
        parse_measurement("Köln;24:00;21.7")


def test_parse_measurement_time_without_leading_zeros():
    assert parse_measurement("Köln;9:5;21.7") == ("Köln", 545, 21.7)


def test_parse_measurement_temperature_not_numeric():
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21;abc")


def test_parse_measurement_negative_temperature():
    assert parse_measurement("Köln;14:21;-5.5") == ("Köln", 861, -5.5)


def test_parse_measurement_no_plausibility_check():
    assert parse_measurement("Köln;14:21;100.0") == ("Köln", 861, 100.0)
    assert parse_measurement("Köln;14:21;-90.0") == ("Köln", 861, -90.0)
    

def test_parse_measurement_none():
    with pytest.raises(ValueError):
        parse_measurement(None)


def test_parse_measurement_city_empty():
    with pytest.raises(ValueError):
        parse_measurement(";14:21;21.7")


def test_parse_measurement_temperature_missing():
    with pytest.raises(ValueError):
        parse_measurement("Köln;14:21;")



def test_filter_by_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 18.5),
        ("Bonn", 900, 25.0),
    ]

    assert filter_by_temperature(measurements, 15.0, 20.0) == [
        ("Düsseldorf", 720, 18.5)
    ]




def test_filter_boundaries_are_inclusive():
    measurements = [
        ("A", 600, 14.9),   # knapp unter lower -> raus
        ("B", 700, 15.0),   # genau lower -> drin
        ("C", 800, 20.0),
        ("D", 900, 25.0),   # genau upper -> drin
        ("E", 1000, 25.1),  # knapp über upper -> raus
    ]

    assert filter_by_temperature(measurements, 15.0, 25.0) == [
        ("B", 700, 15.0),
        ("C", 800, 20.0),
        ("D", 900, 25.0),
    ]


def test_filter_lower_equals_upper_is_allowed():
    measurements = [("A", 600, 20.0), ("B", 700, 21.0)]
    assert filter_by_temperature(measurements, 20.0, 20.0) == [("A", 600, 20.0)]


def test_filter_lower_greater_than_upper():
    with pytest.raises(ValueError):
        filter_by_temperature([("A", 600, 20.0)], 30.0, 10.0)


def test_filter_keeps_order():
    measurements = [
        ("A", 600, 22.0),
        ("B", 700, 30.0),
        ("C", 800, 18.0),
        ("D", 900, 20.0),
    ]
    assert filter_by_temperature(measurements, 15.0, 25.0) == [
        ("A", 600, 22.0),
        ("C", 800, 18.0),
        ("D", 900, 20.0),
    ]


def test_filter_keeps_duplicates():
    measurements = [
        ("Köln", 600, 20.0),
        ("Köln", 600, 20.0),
        ("Bonn", 700, 5.0),
    ]
    assert filter_by_temperature(measurements, 15.0, 25.0) == [
        ("Köln", 600, 20.0),
        ("Köln", 600, 20.0),
    ]


def test_filter_does_not_change_input():
    measurements = [
        ("Bonn", 720, 18.0),
        ("Köln", 600, 25.0),
        ("Aachen", 900, 12.0),
    ]
    copy = list(measurements)
    filter_by_temperature(measurements, 15.0, 30.0)
    assert measurements == copy


def test_filter_returns_new_list():
    measurements = [("A", 600, 20.0), ("B", 700, 21.0)]
    result = filter_by_temperature(measurements, 0.0, 30.0)
    assert result == measurements
    assert result is not measurements

def test_average_temperature_regular_values():
    measurements = [
        ("Köln", 600, 10.0),
        ("Köln", 720, 20.0),
    ]

    assert average_temperature(measurements, "Köln") == 15.0

def test_average_ignores_other_cities():
    measurements = [
        ("Köln", 600, 10.0),
        ("Bonn", 700, 100.0),
        ("Köln", 800, 20.0),
    ]
    assert average_temperature(measurements, "Köln") == pytest.approx(15.0)


def test_average_can_be_decimal():
    measurements = [("Köln", 600, 10.0), ("Köln", 700, 15.0)]
    assert average_temperature(measurements, "Köln") == pytest.approx(12.5)


def test_average_is_case_sensitive():
    measurements = [("Köln", 600, 10.0), ("köln", 700, 30.0)]
    assert average_temperature(measurements, "Köln") == pytest.approx(10.0)
    assert average_temperature(measurements, "köln") == pytest.approx(30.0)


def test_average_exact_city_name():
    measurements = [("Köln", 600, 10.0), ("Köln-Ehrenfeld", 700, 50.0)]
    assert average_temperature(measurements, "Köln") == pytest.approx(10.0)


def test_average_city_not_found():
    with pytest.raises(ValueError):
        average_temperature([("Köln", 600, 10.0)], "Berlin")


def test_average_empty_list():
    with pytest.raises(ValueError):
        average_temperature([], "Köln")


def test_average_does_not_change_input():
    measurements = [
        ("Bonn", 720, 18.0),
        ("Köln", 600, 25.0),
        ("Köln", 900, 12.0),
    ]
    copy = list(measurements)
    average_temperature(measurements, "Köln")
    assert measurements == copy


def test_hottest_measurement_with_unique_maximum():
    measurements = [
        ("Köln", 600, 10.0),
        ("Düsseldorf", 720, 25.0),
        ("Bonn", 900, 20.0),
    ]

    assert hottest_measurement(measurements) == ("Düsseldorf", 720, 25.0)
    

def test_hottest_maximum_first():
    measurements = [("A", 600, 30.0), ("B", 700, 20.0), ("C", 800, 10.0)]
    assert hottest_measurement(measurements) == ("A", 600, 30.0)


def test_hottest_maximum_last():
    measurements = [("A", 600, 10.0), ("B", 700, 20.0), ("C", 800, 30.0)]
    assert hottest_measurement(measurements) == ("C", 800, 30.0)


def test_hottest_single_measurement():
    assert hottest_measurement([("A", 600, 10.0)]) == ("A", 600, 10.0)


def test_hottest_only_negative_temperatures():
    measurements = [("A", 600, -5.0), ("B", 700, -2.0)]
    assert hottest_measurement(measurements) == ("B", 700, -2.0)


def test_hottest_tie_earliest_time_is_behind():
    measurements = [("A", 900, 25.0), ("B", 600, 25.0)]
    assert hottest_measurement(measurements) == ("B", 600, 25.0)


def test_hottest_tie_earliest_time_is_first():
    measurements = [("A", 600, 25.0), ("B", 900, 25.0)]
    assert hottest_measurement(measurements) == ("A", 600, 25.0)


def test_hottest_tie_same_time_first_wins():
    measurements = [("A", 600, 25.0), ("B", 600, 25.0)]
    assert hottest_measurement(measurements) == ("A", 600, 25.0)


def test_hottest_time_only_matters_on_tie():
    measurements = [("A", 900, 30.0), ("B", 500, 20.0)]
    assert hottest_measurement(measurements) == ("A", 900, 30.0)


def test_hottest_empty_list():
    with pytest.raises(ValueError):
        hottest_measurement([])


def test_hottest_does_not_change_input():
    measurements = [
        ("Bonn", 720, 18.0),
        ("Köln", 600, 25.0),
        ("Aachen", 900, 12.0),
    ]
    copy = list(measurements)
    hottest_measurement(measurements)
    assert measurements == copy
