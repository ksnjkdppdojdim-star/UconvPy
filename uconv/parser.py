import re


def parse_input(input_str: str):
    """Parse input string to value, unit.
    
    Examples:
        '10km' → (10.0, 'km')
        '5.5 lbs' → (5.5, 'lbs')
        '100 USD' → (100.0, 'usd')
        '-3.14m' → (-3.14, 'm')
        '1e5 Pa' → (100000.0, 'pa')
        '10 kg*m/s2' → (10.0, 'kg*m/s2')
    
    Returns None if invalid.
    """
    MAX_INPUT_LENGTH = 50
    MAX_VALUE = 1e15
    
    if not isinstance(input_str, str):
        return None
    
    clean = input_str.strip()
    if not clean or len(clean) > MAX_INPUT_LENGTH:
        return None
    
    # Regex: optional '-', digits + optional '.digits', optional 'e±digits', spaces*, unit (with *, /, ^)
    # Accept units with *, /, ^, digits (e.g. 'kg*m2/s2', 'l/min', 'm^2/s')
    match = re.match(r'^(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)\s*([a-zA-Z°µ][a-zA-Z0-9°µ\/\*\^]*)$', clean, re.IGNORECASE)
    
    if not match:
        return None
    
    value_str, unit = match.groups()
    try:
        value = float(value_str)
    except ValueError:
        return None
    
    # Check value bounds
    if not (-MAX_VALUE < value < MAX_VALUE) and value != 0:
        return None
    
    # Check if value is finite (not inf or nan)
    if not (isinstance(value, (int, float)) and (-MAX_VALUE < value < MAX_VALUE or value == 0)):
        return None
    
    return value, unit.lower()

