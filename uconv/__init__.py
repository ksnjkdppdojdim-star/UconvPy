from .i18n import get_error_messages, get_unit_display_name, get_unit_display_name_for_category
from .parser import parse_input
from .units import get_composed_unit_factor, get_unit_category, is_valid_unit, register_unit
from .converters.distance import convert_distance
from .converters.weight import convert_weight
from .converters.time import convert_time
from .converters.currency import convert_currency, convert_currency_live
from .converters.temperature import convert_temperature
from .converters.speed import convert_speed
from .converters.area import convert_area
from .converters.volume import convert_volume
from .converters.energy import convert_energy
from .converters.pressure import convert_pressure
from .converters.power import convert_power
from .converters.data import convert_data


class UnknownUnitError(Exception):
    """Raised when unit is unknown."""
    def __init__(self, unit):
        self.message = f'Unknown unit: {unit}'
        super().__init__(self.message)


class InvalidInputError(Exception):
    """Raised when input format is invalid."""
    def __init__(self, input_str):
        self.message = f'Invalid input format: {input_str}'
        super().__init__(self.message)


class IncompatibleUnitsError(Exception):
    """Raised when units are incompatible types."""
    def __init__(self, from_unit, to_unit):
        self.message = f'Cannot convert from {from_unit} to {to_unit}: incompatible unit types'
        super().__init__(self.message)


_converters = {
    'distance': convert_distance,
    'weight': convert_weight,
    'time': convert_time,
    'currency': convert_currency,
    'temperature': convert_temperature,
    'speed': convert_speed,
    'area': convert_area,
    'volume': convert_volume,
    'energy': convert_energy,
    'pressure': convert_pressure,
    'power': convert_power,
    'data': convert_data
}


def _is_composed_unit(unit: str) -> bool:
    return any(char in unit for char in ('/', '*', '^')) or unit[-1:].isdigit()


def format_number_localized(value: float, locale: str = 'en', maximum_fraction_digits: int = 10) -> str:
    formatted = f'{value:.{maximum_fraction_digits}f}'.rstrip('0').rstrip('.')
    if locale.lower().startswith('fr'):
        return formatted.replace('.', ',')
    return formatted


def convert_display(value: float | str, from_unit: str, to_unit: str, lang: str = 'en') -> str:
    locale = lang.replace('_', '-')
    result = convert(f'{value}{from_unit}', to_unit)
    formatted = format_number_localized(result, locale)
    category = get_unit_category(to_unit) or ''
    display_name = get_unit_display_name_for_category(to_unit, category, lang) if category else get_unit_display_name(to_unit, lang)
    return f'{formatted} {display_name}'


def convert(from_str: str, to_unit: str) -> float:
    """Convert between units.
    
    Args:
        from_str: Source value and unit (e.g., '10km')
        to_unit: Target unit (e.g., 'm')
    
    Returns:
        Converted value as float
    
    Raises:
        UnknownUnitError, InvalidInputError, IncompatibleUnitsError
    """
    try:
        # Parse input
        parsed = parse_input(from_str)
        if parsed is None:
            raise InvalidInputError(from_str)
        
        value, from_unit = parsed
        
        to_unit = to_unit.strip().lower()

        if _is_composed_unit(from_unit) or _is_composed_unit(to_unit):
            from_factor = get_composed_unit_factor(from_unit)
            to_factor = get_composed_unit_factor(to_unit)
            return (value * from_factor) / to_factor

        # Validate units
        if not is_valid_unit(from_unit):
            raise UnknownUnitError(from_unit)
        
        if not is_valid_unit(to_unit):
            raise UnknownUnitError(to_unit)
        
        # Get categories
        from_category = get_unit_category(from_unit)
        to_category = get_unit_category(to_unit)
        
        # Check compatibility
        if from_category != to_category:
            raise IncompatibleUnitsError(from_unit, to_unit)
        
        # Get converter
        converter = _converters.get(from_category)
        if converter is None:
            raise ValueError(f'No converter for category: {from_category}')
        
        # Convert
        return converter(value, from_unit, to_unit)
    
    except (UnknownUnitError, InvalidInputError, IncompatibleUnitsError) as e:
        raise e
    except Exception as e:
        raise ValueError(f'Conversion failed: {str(e)}') from e


__all__ = [
    'convert',
    'convert_display',
    'convert_currency_live',
    'format_number_localized',
    'get_error_messages',
    'get_unit_display_name',
    'get_unit_display_name_for_category',
    'parse_input',
    'register_unit',
    'get_unit_category',
    'is_valid_unit',
    'UnknownUnitError',
    'InvalidInputError',
    'IncompatibleUnitsError',
]

