"""Area converter."""

from ..units import get_conversion_factor
from ..utils import factor_convert


def convert_area(value: float, from_unit: str, to_unit: str) -> float:
    """Convert area units.
    
    Args:
        value: Area value
        from_unit: Source unit (m2, km2, hectare, acre, ft2, etc.)
        to_unit: Target unit
    
    Returns:
        Converted area
    
    Raises:
        ValueError: If invalid units
    """
    from_factor = get_conversion_factor(from_unit)
    to_factor = get_conversion_factor(to_unit)
    
    if from_factor is None:
        raise ValueError(f'Invalid area unit: {from_unit}')
    if to_factor is None:
        raise ValueError(f'Invalid area unit: {to_unit}')
    
    return factor_convert(value, from_factor, to_factor)
