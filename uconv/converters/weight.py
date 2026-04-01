from ..units import get_conversion_factor
from ..utils import factor_convert


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    """Convert weight: to base (g) then to target."""
    from_factor = get_conversion_factor(from_unit)
    to_factor = get_conversion_factor(to_unit)
    
    if from_factor is None or to_factor is None:
        raise ValueError('Invalid weight unit')
    
    return factor_convert(value, from_factor, to_factor)

