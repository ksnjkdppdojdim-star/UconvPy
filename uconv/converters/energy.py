"""Energy converter."""

from ..units import get_conversion_factor
from ..utils import factor_convert


def convert_energy(value: float, from_unit: str, to_unit: str) -> float:
    """Convert energy units.
    
    Args:
        value: Energy value
        from_unit: Source unit (j, kj, cal, kcal, wh, kwh, btu, ev, etc.)
        to_unit: Target unit
    
    Returns:
        Converted energy
    
    Raises:
        ValueError: If invalid units
    """
    from_factor = get_conversion_factor(from_unit)
    to_factor = get_conversion_factor(to_unit)
    
    if from_factor is None:
        raise ValueError(f'Invalid energy unit: {from_unit}')
    if to_factor is None:
        raise ValueError(f'Invalid energy unit: {to_unit}')
    
    return factor_convert(value, from_factor, to_factor)
