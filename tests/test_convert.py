import pytest
from uconv import convert, parse_input, get_unit_category, is_valid_unit, register_unit
from uconv import UnknownUnitError, InvalidInputError, IncompatibleUnitsError


class TestParser:
    """Test input parser"""
    
    def test_parse_simple_value(self):
        assert parse_input('10m') == (10.0, 'm')
        assert parse_input('5.5lbs') == (5.5, 'lbs')
        assert parse_input('100usd') == (100.0, 'usd')
    
    def test_parse_with_spaces(self):
        assert parse_input('10 km') == (10.0, 'km')
        assert parse_input('5.5 lbs') == (5.5, 'lbs')
    
    def test_parse_negative_values(self):
        assert parse_input('-3.14m') == (-3.14, 'm')
        assert parse_input('-100 usd') == (-100.0, 'usd')
    
    def test_parse_scientific_notation(self):
        assert parse_input('1e5m') == (100000.0, 'm')
        assert parse_input('1.5e5 km') == (150000.0, 'km')
        assert parse_input('1e-3kg') == (0.001, 'kg')
        assert parse_input('1.23e+2 lbs') == (123.0, 'lbs')
    
    def test_parse_composed_units(self):
        assert parse_input('10kg*m/s2') == (10.0, 'kg*m/s2')
        assert parse_input('5j/s') == (5.0, 'j/s')
    
    def test_parse_invalid_input(self):
        assert parse_input('invalid') is None
        assert parse_input('') is None
        assert parse_input('nounit') is None


class TestDistance:
    """Test distance conversions"""
    
    def test_km_to_m(self):
        assert convert('10km', 'm') == 10000
    
    def test_m_to_km(self):
        assert convert('10000m', 'km') == 10
    
    def test_ft_to_m(self):
        assert abs(convert('10ft', 'm') - 3.048) < 0.001
    
    def test_mile_to_km(self):
        assert abs(convert('1mi', 'km') - 1.609344) < 0.001
    
    def test_decimal_values(self):
        assert convert('5.5km', 'm') == 5500


class TestWeight:
    """Test weight conversions"""
    
    def test_lbs_to_kg(self):
        assert abs(convert('5lbs', 'kg') - 2.26796) < 0.00001
    
    def test_oz_to_g(self):
        assert abs(convert('16oz', 'g') - 453.592) < 0.001
    
    def test_kg_to_lb(self):
        assert abs(convert('1kg', 'lb') - 2.20462) < 0.00001
    
    def test_ton_to_kg(self):
        assert convert('1t', 'kg') == 1000


class TestTime:
    """Test time conversions"""
    
    def test_hr_to_min(self):
        assert convert('1hr', 'min') == 60
    
    def test_day_to_hr(self):
        assert convert('1day', 'hr') == 24
    
    def test_min_to_s(self):
        assert convert('5min', 's') == 300
    
    def test_week_to_day(self):
        assert convert('1week', 'day') == 7


class TestTemperature:
    """Test temperature conversions (special case)"""
    
    def test_celsius_to_fahrenheit(self):
        assert abs(convert('0c', 'f') - 32.0) < 0.001
        assert abs(convert('100c', 'f') - 212.0) < 0.001
    
    def test_fahrenheit_to_celsius(self):
        assert abs(convert('32f', 'c') - 0.0) < 0.001
        assert abs(convert('212f', 'c') - 100.0) < 0.001
    
    def test_celsius_to_kelvin(self):
        assert abs(convert('0c', 'k') - 273.15) < 0.001
    
    def test_kelvin_to_celsius(self):
        assert abs(convert('273.15k', 'c') - 0.0) < 0.001


class TestSpeed:
    """Test speed conversions"""
    
    def test_kmh_to_ms(self):
        # 100 km/h * 0.277778 m/s per km/h ≈ 27.78 m/s
        result = convert('100kmh', 'm/s')
        assert abs(result - 27.7778) < 0.1
    
    def test_mph_to_kmh(self):
        # 1 mph ≈ 1.60934 km/h
        result = convert('1mph', 'kmh')
        assert abs(result - 1.60934) < 0.01

    def test_speed_aliases(self):
        assert convert('10meter/second', 'km/h') == pytest.approx(36, rel=1e-4)
        assert convert('10knots', 'm/s') == pytest.approx(5.14444, rel=1e-4)


class TestArea:
    """Test area conversions"""
    
    def test_hectare_to_m2(self):
        assert convert('1hectare', 'm2') == 10000
    
    def test_m2_to_km2(self):
        assert convert('1000000m2', 'km2') == 1

    def test_area_aliases(self):
        assert convert('1squarefoot', 'ft2') == pytest.approx(1)
        assert convert('1yd2', 'm2') == pytest.approx(0.836127)


class TestVolume:
    """Test volume conversions"""
    
    def test_liter_to_ml(self):
        # Use approximate due to floating point precision
        result = convert('1l', 'ml')
        assert abs(result - 1000) < 0.1
    
    def test_m3_to_liter(self):
        assert convert('1m3', 'l') == 1000

    def test_volume_aliases(self):
        assert convert('1quart', 'pt') == pytest.approx(2.0, rel=1e-3)
        assert convert('1cm3', 'ml') == pytest.approx(1.0)


class TestEnergy:
    """Test energy conversions"""
    
    def test_kwh_to_j(self):
        assert convert('1kwh', 'j') == 3600000
    
    def test_kj_to_j(self):
        assert convert('1kj', 'j') == 1000

    def test_energy_aliases(self):
        assert convert('3600j', 'watt-hour') == pytest.approx(1)
        assert convert('1joules', 'j') == pytest.approx(1)


class TestPressure:
    """Test pressure conversions"""
    
    def test_bar_to_pa(self):
        assert convert('1bar', 'pa') == 100000
    
    def test_atm_to_pa(self):
        assert abs(convert('1atm', 'pa') - 101325) < 1

    def test_pressure_aliases(self):
        assert convert('6894.76pa', 'pound per square inch') == pytest.approx(1)


class TestPower:
    """Test power conversions"""
    
    def test_kw_to_w(self):
        assert convert('1kw', 'w') == 1000
    
    def test_hp_to_w(self):
        assert abs(convert('1hp', 'w') - 745.7) < 0.1

    def test_power_aliases(self):
        assert convert('1watts', 'w') == pytest.approx(1)


class TestCurrency:
    """Test currency conversions"""
    
    def test_usd_to_eur(self):
        result = convert('100usd', 'eur')
        assert abs(result - 85) < 1
    
    def test_same_currency(self):
        assert convert('100usd', 'usd') == 100


class TestErrors:
    """Test error handling"""
    
    def test_unknown_from_unit(self):
        with pytest.raises(UnknownUnitError):
            convert('10xyz', 'm')
    
    def test_unknown_to_unit(self):
        with pytest.raises(UnknownUnitError):
            convert('10m', 'xyz')
    
    def test_incompatible_units(self):
        with pytest.raises(IncompatibleUnitsError):
            convert('10km', 'kg')
    
    def test_invalid_input_format(self):
        with pytest.raises(InvalidInputError):
            convert('invalid', 'm')


class TestUtilityFunctions:
    """Test utility functions"""
    
    def test_get_unit_category(self):
        assert get_unit_category('m') == 'distance'
        assert get_unit_category('kg') == 'weight'
        assert get_unit_category('s') == 'time'
        assert get_unit_category('c') == 'temperature'
        assert get_unit_category('kmh') == 'speed'
        assert get_unit_category('xyz') is None
    
    def test_is_valid_unit(self):
        assert is_valid_unit('m') is True
        assert is_valid_unit('km') is True
        assert is_valid_unit('xyz') is False

    def test_register_unit(self):
        register_unit('furlongtest', 201.168, 'distance')
        assert convert('1furlongtest', 'm') == pytest.approx(201.168)

    def test_temperature_aliases(self):
        assert convert('0°c', 'f') == pytest.approx(32)

    def test_weight_aliases(self):
        assert convert('1megagram', 'kg') == pytest.approx(1000)


class TestComposedUnits:
    def test_km2_to_m2(self):
        assert convert('2km2', 'm2') == pytest.approx(2e6)

    def test_cm3_to_m3(self):
        assert convert('1000000cm3', 'm3') == pytest.approx(1)

    def test_l_per_min_to_m3_per_h(self):
        assert convert('60l/min', 'm3/h') == pytest.approx(3.6)

    def test_m3_per_s_to_l_per_min(self):
        assert convert('0.001m3/s', 'l/min') == pytest.approx(60)

    def test_energy_equivalents(self):
        assert convert('5n*m', 'j') == pytest.approx(5)
        assert convert('42j/s', 'w') == pytest.approx(42)
        assert convert('7w*s', 'j') == pytest.approx(7)
        assert convert('3pa*m3', 'j') == pytest.approx(3)

    
    def test_invalid_input_error(self):
        with pytest.raises(InvalidInputError):
            convert('invalid', 'm')
        with pytest.raises(InvalidInputError):
            convert('', 'm')
        with pytest.raises(InvalidInputError):
            convert('10', 'm')
    
    def test_incompatible_units_error(self):
        with pytest.raises(IncompatibleUnitsError):
            convert('10km', 'kg')
        with pytest.raises(IncompatibleUnitsError):
            convert('5lbs', 'hr')
        with pytest.raises(IncompatibleUnitsError):
            convert('100usd', 'm')
    
    def test_parse_variants(self):
        assert convert('10 km', 'm') == 10000
        assert convert('10.5km', 'm') == 10500
        assert convert(' 10km ', 'm') == 10000
        assert convert('-10km', 'm') == -10000


if __name__ == '__main__':
    pytest.main([__file__])

