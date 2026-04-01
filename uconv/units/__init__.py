from .distance import UNITS as DISTANCE_UNITS
from .weight import UNITS as WEIGHT_UNITS
from .time import UNITS as TIME_UNITS
from .currency import UNITS as CURRENCY_UNITS
from .temperature import UNITS as TEMPERATURE_UNITS
from .speed import UNITS as SPEED_UNITS
from .area import UNITS as AREA_UNITS
from .volume import UNITS as VOLUME_UNITS
from .energy import UNITS as ENERGY_UNITS
from .pressure import UNITS as PRESSURE_UNITS
from .power import UNITS as POWER_UNITS
from .data import UNITS as DATA_UNITS

UNITS = {
    'distance': DISTANCE_UNITS,
    'weight': WEIGHT_UNITS,
    'time': TIME_UNITS,
    'currency': CURRENCY_UNITS,
    'temperature': TEMPERATURE_UNITS,
    'speed': SPEED_UNITS,
    'area': AREA_UNITS,
    'volume': VOLUME_UNITS,
    'energy': ENERGY_UNITS,
    'pressure': PRESSURE_UNITS,
    'power': POWER_UNITS,
    'data': DATA_UNITS,
}

BASE_UNITS = {
    'distance': 'm',
    'weight': 'g',
    'time': 's',
    'currency': 'usd',
    'temperature': 'c',
    'speed': 'm/s',
    'area': 'm2',
    'volume': 'm3',
    'energy': 'j',
    'pressure': 'pa',
    'power': 'w',
    'data': 'b',
}

SI_PREFIXES = [
    ('Y', 1e24),
    ('Z', 1e21),
    ('E', 1e18),
    ('P', 1e15),
    ('T', 1e12),
    ('G', 1e9),
    ('M', 1e6),
    ('k', 1e3),
    ('h', 1e2),
    ('da', 1e1),
    ('d', 1e-1),
    ('c', 1e-2),
    ('m', 1e-3),
    ('u', 1e-6),
    ('n', 1e-9),
    ('p', 1e-12),
    ('f', 1e-15),
    ('a', 1e-18),
    ('z', 1e-21),
    ('y', 1e-24),
]

BINARY_PREFIXES = [
    ('ki', 1024),
    ('mi', 1024 ** 2),
    ('gi', 1024 ** 3),
    ('ti', 1024 ** 4),
    ('pi', 1024 ** 5),
    ('ei', 1024 ** 6),
    ('zi', 1024 ** 7),
    ('yi', 1024 ** 8),
]

COMPOSED_EQUIVALENTS = {
    'n*m': 'j',
    'j/s': 'w',
    'w*s': 'j',
    'pa*m3': 'j',
    'v*a': 'w',
    'c*v': 'j',
}


def _add_si_prefixes(category: str, base_unit: str) -> None:
    for symbol, factor in SI_PREFIXES:
        prefixed = (symbol + base_unit).lower()
        if prefixed == base_unit.lower():
            continue
        if prefixed not in UNITS[category] and base_unit in UNITS[category]:
            UNITS[category][prefixed] = factor * UNITS[category][base_unit]


def _add_binary_prefixes() -> None:
    for symbol, factor in BINARY_PREFIXES:
        key = f'{symbol}b'
        if key not in UNITS['data']:
            UNITS['data'][key] = factor


def register_unit(name: str, factor: float, category: str) -> None:
    if not isinstance(name, str) or not name.strip():
        raise ValueError('Unit name must be a non-empty string')
    if category not in UNITS:
        raise ValueError(f'Unknown category: {category}')
    if not isinstance(factor, (int, float)) or not factor:
        raise ValueError('Invalid factor')
    UNITS[category][name.strip().lower()] = float(factor)


def get_unit_category(unit: str) -> str | None:
    normalized = unit.lower()
    for category, units in UNITS.items():
        if normalized in units:
            return category
    return None


def is_valid_unit(unit: str) -> bool:
    return get_unit_category(unit) is not None


def get_conversion_factor(unit: str) -> float | None:
    category = get_unit_category(unit)
    if not category:
        return None
    return UNITS[category][unit.lower()]


def parse_composed_unit(unit_str: str) -> tuple[list[tuple[str, int]], list[tuple[str, int]]]:
    num, *den = unit_str.split('/')
    den_part = den[0] if den else ''

    def parse_side(part: str) -> list[tuple[str, int]]:
        if not part:
            return []
        result = []
        for raw in part.split('*'):
            token = raw.strip()
            if not token:
                continue
            power = 1
            if '^' in token:
                base, exponent = token.split('^', 1)
                token = base
                power = int(exponent)
            else:
                index = len(token)
                while index > 0 and token[index - 1].isdigit():
                    index -= 1
                if index < len(token) and index > 0:
                    token, exponent = token[:index], token[index:]
                    power = int(exponent)
            result.append((token.lower(), power))
        return result

    return parse_side(num), parse_side(den_part)


def get_composed_unit_factor(unit_str: str) -> float:
    normalized = unit_str.replace(' ', '').lower()
    if normalized in COMPOSED_EQUIVALENTS:
        factor = get_conversion_factor(COMPOSED_EQUIVALENTS[normalized])
        if factor is None:
            raise ValueError(f'Unknown equivalent unit: {normalized}')
        return factor

    numerator, denominator = parse_composed_unit(normalized)
    factor = 1.0
    for unit, power in numerator:
        current = get_conversion_factor(unit)
        if current is None:
            raise ValueError(f'Unknown unit: {unit}')
        factor *= current ** power
    for unit, power in denominator:
        current = get_conversion_factor(unit)
        if current is None:
            raise ValueError(f'Unknown unit: {unit}')
        factor /= current ** power
    return factor


_add_si_prefixes('distance', 'm')
_add_si_prefixes('weight', 'g')
_add_si_prefixes('area', 'm2')
_add_si_prefixes('volume', 'm3')
_add_si_prefixes('volume', 'l')
_add_binary_prefixes()

__all__ = [
    'BASE_UNITS',
    'UNITS',
    'register_unit',
    'get_unit_category',
    'is_valid_unit',
    'get_conversion_factor',
    'parse_composed_unit',
    'get_composed_unit_factor',
]