from urllib.error import URLError

import pytest

from uconv import convert_currency_live


class _MockResponse:
    def __init__(self, payload: bytes):
        self._payload = payload

    def read(self) -> bytes:
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_convert_currency_live_success(monkeypatch):
    def fake_urlopen(url, timeout=10.0):
        assert 'from=USD' in url
        assert 'to=EUR' in url
        return _MockResponse(b'{"rates":{"EUR":0.92}}')

    monkeypatch.setattr('uconv.converters.currency.urlopen', fake_urlopen)

    assert convert_currency_live(100, 'usd', 'eur') == pytest.approx(92.0)


def test_convert_currency_live_unknown_currency(monkeypatch):
    def fake_urlopen(url, timeout=10.0):
        return _MockResponse(b'{"rates":{}}')

    monkeypatch.setattr('uconv.converters.currency.urlopen', fake_urlopen)

    with pytest.raises(ValueError, match='Unknown currency: EUR'):
        convert_currency_live(100, 'usd', 'eur')


def test_convert_currency_live_request_failure(monkeypatch):
    def fake_urlopen(url, timeout=10.0):
        raise URLError('network down')

    monkeypatch.setattr('uconv.converters.currency.urlopen', fake_urlopen)

    with pytest.raises(ValueError, match='Failed to fetch live rates'):
        convert_currency_live(100, 'usd', 'eur')