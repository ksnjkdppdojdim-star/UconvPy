from ..units import get_conversion_factor
from ..utils import factor_convert


def convert_distance(value: float, from_unit: str, to_unit: str) -> float:
    """Convert distance: to base (m) then to target.

    Args:
        value: Value in from_unit
        from_unit, to_unit: Units

    Raises:
        ValueError if invalid units
    """
    from_factor = get_conversion_factor(from_unit)
    to_factor = get_conversion_factor(to_unit)
    
    if from_factor is None or to_factor is None:
        raise ValueError('Invalid distance unit')
    
    return factor_convert(value, from_factor, to_factor)

