from uconv.cli import main


def test_cli_help(capsys):
    exit_code = main(['--help'])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert 'Usage: uconv <value> <from_unit> <to_unit>' in captured.out


def test_cli_version(capsys):
    exit_code = main(['--version'])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert 'uconv version ' in captured.out


def test_cli_categories(capsys):
    exit_code = main(['categories'])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert 'Available categories:' in captured.out
    assert 'distance' in captured.out
    assert 'temperature' in captured.out


def test_cli_list(capsys):
    exit_code = main(['list', '--lang', 'fr'])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert 'Supported units:' in captured.out
    assert '[distance]' in captured.out
    assert 'km (kilomètre)' in captured.out


def test_cli_convert_simple(capsys):
    exit_code = main(['10', 'km', 'm'])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert '10.0 km = 10000.0 m' in captured.out


def test_cli_convert_composed(capsys):
    exit_code = main(['60', 'l/min', 'm3/h'])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert '60.0 l/min = 3.6 m3/h' in captured.out


def test_cli_invalid_value(capsys):
    exit_code = main(['abc', 'km', 'm'])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert 'Invalid value: abc' in captured.err


def test_cli_unknown_unit(capsys):
    exit_code = main(['10', 'xyz', 'm'])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert 'Unknown or invalid unit(s).' in captured.err