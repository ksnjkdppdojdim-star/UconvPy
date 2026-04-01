"""Power converter."""

from ..units import get_conversion_factor
from ..utils import factor_convert


def convert_power(value: float, from_unit: str, to_unit: str) -> float:
    """Convert power units.
    
    Args:
        value: Power value
        from_unit: Source unit (w, kw, mw, hp, ps, etc.)
        to_unit: Target unit
    
    Returns:
        Converted power
    
    Raises:
        ValueError: If invalid units
    """
    from_factor = get_conversion_factor(from_unit)
    to_factor = get_conversion_factor(to_unit)
    
    if from_factor is None:
        raise ValueError(f'Invalid power unit: {from_unit}')
    if to_factor is None:
        raise ValueError(f'Invalid power unit: {to_unit}')
    
    return factor_convert(value, from_factor, to_factor)
