"""Data storage converter (bits and bytes)."""

from ..units import get_conversion_factor
from ..utils import factor_convert


def convert_data(value: float, from_unit: str, to_unit: str) -> float:
    """Convert data storage units.
    
    Args:
        value: Data value
        from_unit: Source unit (b, byte, kb, kib, mb, mib, gb, gib, etc.)
        to_unit: Target unit
    
    Returns:
        Converted data size
    
    Raises:
        ValueError: If invalid units
    """
    from_factor = get_conversion_factor(from_unit)
    to_factor = get_conversion_factor(to_unit)
    
    if from_factor is None:
        raise ValueError(f'Invalid data unit: {from_unit}')
    if to_factor is None:
        raise ValueError(f'Invalid data unit: {to_unit}')
    
    return factor_convert(value, from_factor, to_factor)
