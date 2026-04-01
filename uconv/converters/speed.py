"""Speed converter."""

from ..units import get_conversion_factor
from ..utils import factor_convert


def convert_speed(value: float, from_unit: str, to_unit: str) -> float:
    """Convert speed units.
    
    Args:
        value: Speed value
        from_unit: Source unit (m/s, km/h, mph, knot, ft/s, etc.)
        to_unit: Target unit
    
    Returns:
        Converted speed
    
    Raises:
        ValueError: If invalid units
    """
    # Get conversion factors to base unit (m/s)
    from_factor = get_conversion_factor(from_unit)
    to_factor = get_conversion_factor(to_unit)
    
    if from_factor is None:
        raise ValueError(f'Invalid speed unit: {from_unit}')
    if to_factor is None:
        raise ValueError(f'Invalid speed unit: {to_unit}')
    
    # Convert to base (m/s) then to target
    return factor_convert(value, from_factor, to_factor)
