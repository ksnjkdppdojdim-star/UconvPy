"""Pressure converter."""

from ..units import get_conversion_factor
from ..utils import factor_convert


def convert_pressure(value: float, from_unit: str, to_unit: str) -> float:
    """Convert pressure units.
    
    Args:
        value: Pressure value
        from_unit: Source unit (pa, bar, atm, psi, torr, etc.)
        to_unit: Target unit
    
    Returns:
        Converted pressure
    
    Raises:
        ValueError: If invalid units
    """
    from_factor = get_conversion_factor(from_unit)
    to_factor = get_conversion_factor(to_unit)
    
    if from_factor is None:
        raise ValueError(f'Invalid pressure unit: {from_unit}')
    if to_factor is None:
        raise ValueError(f'Invalid pressure unit: {to_unit}')
    
    return factor_convert(value, from_factor, to_factor)
