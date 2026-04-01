from uconv import convert_display, format_number_localized, get_error_messages, get_unit_display_name, get_unit_display_name_for_category


class TestConvertDisplay:
    def test_display_in_french(self):
        assert convert_display(10, 'km', 'm', 'fr') == '10000 mètre'
        assert convert_display(2, 'kg', 'g', 'fr') == '2000 gramme'

    def test_display_in_english(self):
        assert convert_display(10, 'km', 'm', 'en') == '10000 meter'
        assert convert_display(2, 'kg', 'g', 'en') == '2000 gram'

    def test_display_area(self):
        assert convert_display(1, 'km2', 'm2', 'fr') == '1000000 mètre carré'
        assert convert_display(1, 'km2', 'm2', 'en') == '1000000 square meter'


class TestLocalizedFormatting:
    def test_number_format(self):
        assert format_number_localized(12.34567, 'fr') == '12,34567'
        assert format_number_localized(12.34567, 'en') == '12.34567'

    def test_display_localized_format(self):
        assert convert_display(12345.67, 'm', 'km', 'fr') == '12,34567 kilomètre'
        assert convert_display(12345.67, 'm', 'km', 'en') == '12.34567 kilometer'
        assert convert_display(1234.56, 'm', 'km', 'fr_FR') == '1,23456 kilomètre'
        assert convert_display(1234.56, 'm', 'km', 'en_US') == '1.23456 kilometer'


class TestI18nHelpers:
    def test_unit_display_name(self):
        assert get_unit_display_name('km', 'fr') == 'kilomètre'
        assert get_unit_display_name('kg', 'en') == 'kilogram'

    def test_unit_display_aliases(self):
        assert get_unit_display_name('squaremeter', 'en') == 'square meter'
        assert get_unit_display_name('squarefoot', 'fr') == 'pied carré'
        assert get_unit_display_name('kilometre', 'en') == 'kilometre'
        assert get_unit_display_name('litre', 'en') == 'litre'
        assert get_unit_display_name('°c', 'fr') == 'degré Celsius'
        assert get_unit_display_name('horsepower', 'fr') == 'cheval-vapeur'

    def test_error_messages(self):
        fr_errors = get_error_messages('fr')
        en_errors = get_error_messages('en')
        assert fr_errors['unknownUnit']('xyz') == 'Unité inconnue : xyz'
        assert en_errors['invalidInput']('bad') == 'Invalid input format: bad'

    def test_category_aware_unit_display_name(self):
        assert get_unit_display_name_for_category('ms', 'time', 'fr') == 'ms'
        assert get_unit_display_name_for_category('ms', 'speed', 'fr') == 'mètre par seconde'