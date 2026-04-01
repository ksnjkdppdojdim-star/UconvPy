# Mahounou UConv (Python)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

Python implementation of the Mahounou UConv family.

Naming convention across ecosystems:
- NPM: @mahounou/uconv
- PyPI: mahounou-uconv
- Composer: mahounou/uconv

Import name in Python remains:
- from uconv import convert

## Installation

### From PyPI
```bash
pip install mahounou-uconv
```

### From Source
```bash
git clone https://github.com/ksnjkdppdojdim-star/UconvPy.git
cd UconvPy
pip install -e .
```

## CLI (Important)

This project installs these Python commands:
- uconvpy

Examples:
```bash
uconvpy 10 km m
uconvpy 60 l/min m3/h
uconvpy list --lang fr
uconvpy categories
```

Why not install a Python command named uconv by default?
- Because many machines already have the Node global command uconv from npm install -g @mahounou/uconv.
- Keeping Python command as uconvpy avoids command conflicts in PATH.

## Quick Start (Library)

```python
from uconv import convert

convert('10km', 'm')
convert('0c', 'f')
convert('100km/h', 'm/s')
convert('1kwh', 'j')
```

## API Highlights

```python
from uconv import (
		convert,
		convert_display,
		convert_currency_live,
		parse_input,
		register_unit,
)
```

## Supported Categories

- distance
- weight
- time
- currency
- temperature
- speed
- area
- volume
- energy
- pressure
- power
- data

## Project Structure (Scalable, Node-like)

```text
UconvPy/
	uconv/
		__init__.py
		cli.py
		parser.py
		converters/
			area.py
			currency.py
			data.py
			distance.py
			energy.py
			power.py
			pressure.py
			speed.py
			temperature.py
			time.py
			volume.py
			weight.py
		i18n/
			en_US/LC_MESSAGES/
			fr_FR/LC_MESSAGES/
		units/
			area.py
			currency.py
			data.py
			distance.py
			energy.py
			power.py
			pressure.py
			speed.py
			temperature.py
			time.py
			volume.py
			weight.py
			__init__.py
		utils/
			convert.py
	tests/
		test_cli.py
		test_convert.py
		test_currency_live.py
		test_i18n_display.py
	.github/workflows/
		ci.yml
		package-check.yml
```

## Development

```bash
git clone https://github.com/ksnjkdppdojdim-star/UconvPy.git
cd UconvPy
pip install -e ".[dev]"
pytest tests -v
```

## License

MIT License - see LICENSE file for details.

