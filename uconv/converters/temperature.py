"""Temperature converter.

Temperature is special because it's not a simple factor conversion.
We convert to Kelvin (base) then to target unit.
"""


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Convert temperature between units (K, C, F).
    
    Args:
        value: Temperature value
        from_unit: Source unit (k, c, f, kelvin, celsius, fahrenheit)
        to_unit: Target unit
    
    Returns:
        Converted temperature
    
    Raises:
        ValueError: If invalid units
    """
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    # Normalize unit names
    unit_map = {
        'k': 'kelvin',
        'c': 'celsius',
        '°c': 'celsius',
        'f': 'fahrenheit',
        '°f': 'fahrenheit',
    }
    
    from_unit = unit_map.get(from_unit, from_unit)
    to_unit = unit_map.get(to_unit, to_unit)
    
    valid_units = {'kelvin', 'celsius', 'fahrenheit'}
    
    if from_unit not in valid_units:
        raise ValueError(f'Invalid temperature unit: {from_unit}')
    if to_unit not in valid_units:
        raise ValueError(f'Invalid temperature unit: {to_unit}')
    
    # Step 1: Convert from source to Kelvin (base unit)
    kelvin_value = _to_kelvin(value, from_unit)
    
    # Step 2: Convert from Kelvin to target unit
    result = _from_kelvin(kelvin_value, to_unit)
    
    return result


def _to_kelvin(value: float, unit: str) -> float:
    """Convert temperature to Kelvin."""
    unit = unit.lower()
    
    if unit in ('k', 'kelvin'):
        return value
    elif unit in ('c', 'celsius'):
        return value + 273.15
    elif unit in ('f', 'fahrenheit'):
        return (value - 32) * 5/9 + 273.15
    else:
        raise ValueError(f'Unknown temperature unit: {unit}')


def _from_kelvin(value: float, unit: str) -> float:
    """Convert from Kelvin to target temperature unit."""
    unit = unit.lower()
    
    if unit in ('k', 'kelvin'):
        return value
    elif unit in ('c', 'celsius'):
        return value - 273.15
    elif unit in ('f', 'fahrenheit'):
        return (value - 273.15) * 9/5 + 32
    else:
        raise ValueError(f'Unknown temperature unit: {unit}')
