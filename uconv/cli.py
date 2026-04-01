import sys
from importlib.metadata import PackageNotFoundError, version

from . import convert
from .i18n import get_unit_display_name_for_category
from .units import UNITS, get_composed_unit_factor, get_conversion_factor


def _package_version() -> str:
    for distribution_name in ('mahounou-uconv', 'uconv'):
        try:
            return version(distribution_name)
        except PackageNotFoundError:
            continue
    return 'dev'


def print_usage() -> None:
    print('Uconv - Universal Unit Converter')
    print('Usage: uconv <value> <from_unit> <to_unit> [--lang xx]')
    print('       uconv list [--lang xx]')
    print('       uconv categories')
    print('       uconv --version')
    print('       uconv --help')
    print('Examples:')
    print('  uconv 10 km m')
    print('  uconv 100 USD EUR')
    print('  uconv list --lang fr')
    print('  uconv categories')


def print_version() -> None:
    print(f'uconv version {_package_version()}')


def print_categories() -> None:
    print('Available categories:')
    for category in UNITS:
        print(f' - {category}')


def print_units(lang: str = 'en') -> None:
    print('Supported units:')
    for category, units in UNITS.items():
        print(f'\n[{category}]')
        for unit in sorted(units):
            display_name = get_unit_display_name_for_category(unit, category, lang)
            suffix = f' ({display_name})' if display_name != unit else ''
            print(f'  {unit}{suffix}')


def _get_factor(unit: str) -> float | None:
    factor = get_conversion_factor(unit)
    if factor is not None:
        return factor
    try:
        return get_composed_unit_factor(unit)
    except ValueError:
        return None


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if not args or '--help' in args or '-h' in args:
        print_usage()
        return 0

    if '--version' in args or '-v' in args:
        print_version()
        return 0

    lang = 'en'
    if '--lang' in args:
        lang_index = args.index('--lang')
        if lang_index + 1 >= len(args):
            print('Missing language after --lang', file=sys.stderr)
            return 1
        lang = args[lang_index + 1]
        del args[lang_index:lang_index + 2]

    if args and args[0] == 'list':
        print_units(lang)
        return 0

    if args and args[0] == 'categories':
        print_categories()
        return 0

    if len(args) != 3:
        print_usage()
        return 1

    value_str, from_unit, to_unit = args
    try:
        value = float(value_str)
    except ValueError:
        print(f'Invalid value: {value_str}', file=sys.stderr)
        print_usage()
        return 1

    from_factor = _get_factor(from_unit.lower())
    to_factor = _get_factor(to_unit.lower())
    if from_factor is None or to_factor is None:
        print('Unknown or invalid unit(s).', file=sys.stderr)
        print_usage()
        return 1

    result = convert(f'{value}{from_unit}', to_unit)
    print(f'{value} {from_unit} = {result} {to_unit}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())