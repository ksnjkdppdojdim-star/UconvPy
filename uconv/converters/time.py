from ..units import get_conversion_factor
from ..utils import factor_convert


def convert_time(value: float, from_unit: str, to_unit: str) -> float:
    """Convert time: to base (s) then to target."""
    from_factor = get_conversion_factor(from_unit)
    to_factor = get_conversion_factor(to_unit)
    
    if from_factor is None or to_factor is None:
        raise ValueError('Invalid time unit')
    
    return factor_convert(value, from_factor, to_factor)

