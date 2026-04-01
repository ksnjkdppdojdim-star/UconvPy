"""Volume converter."""

from ..units import get_conversion_factor
from ..utils import factor_convert


def convert_volume(value: float, from_unit: str, to_unit: str) -> float:
    """Convert volume units.
    
    Args:
        value: Volume value
        from_unit: Source unit (m3, l, gallon, ft3, barrel, etc.)
        to_unit: Target unit
    
    Returns:
        Converted volume
    
    Raises:
        ValueError: If invalid units
    """
    from_factor = get_conversion_factor(from_unit)
    to_factor = get_conversion_factor(to_unit)
    
    if from_factor is None:
        raise ValueError(f'Invalid volume unit: {from_unit}')
    if to_factor is None:
        raise ValueError(f'Invalid volume unit: {to_unit}')
    
    return factor_convert(value, from_factor, to_factor)
