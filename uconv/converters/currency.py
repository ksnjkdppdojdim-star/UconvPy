import json
from urllib.error import URLError
from urllib.request import urlopen

from ..units import get_conversion_factor
from ..utils import factor_convert


def convert_currency(value: float, from_unit: str, to_unit: str) -> float:
    """Convert currency: to base (USD) then to target.
    Note: Hardcoded rates; use API in prod.
    """
    from_factor = get_conversion_factor(from_unit)
    to_factor = get_conversion_factor(to_unit)
    
    if from_factor is None or to_factor is None:
        raise ValueError('Invalid currency')
    
    in_usd = value * from_factor
    return in_usd * to_factor


def convert_currency_live(value: float, from_unit: str, to_unit: str, timeout: float = 10.0) -> float:
    from_code = from_unit.upper()
    to_code = to_unit.upper()
    url = f'https://api.frankfurter.app/latest?from={from_code}&to={to_code}'

    try:
        with urlopen(url, timeout=timeout) as response:
            payload = json.loads(response.read().decode('utf-8'))
    except URLError as exc:
        raise ValueError('Failed to fetch live rates') from exc

    rates = payload.get('rates', {})
    rate = rates.get(to_code)
    if rate is None:
        raise ValueError(f'Unknown currency: {to_code}')
    return value * rate

