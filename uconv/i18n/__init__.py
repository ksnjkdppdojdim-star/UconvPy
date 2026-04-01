from .en_US.LC_MESSAGES.errors import ERROR_MESSAGES as ERRORS_EN
from .en_US.LC_MESSAGES.units import UNIT_NAMES as UNITS_EN
from .fr_FR.LC_MESSAGES.errors import ERROR_MESSAGES as ERRORS_FR
from .fr_FR.LC_MESSAGES.units import UNIT_NAMES as UNITS_FR

UNIT_I18N_MAP = {
    'fr': UNITS_FR,
    'fr_FR': UNITS_FR,
    'en': UNITS_EN,
    'en_US': UNITS_EN,
}

ERROR_I18N_MAP = {
    'fr': ERRORS_FR,
    'fr_FR': ERRORS_FR,
    'en': ERRORS_EN,
    'en_US': ERRORS_EN,
}


def get_unit_display_name(unit: str, lang: str = 'en') -> str:
    normalized = unit.lower()
    dictionary = UNIT_I18N_MAP.get(lang, UNIT_I18N_MAP['en'])
    for category in dictionary.values():
        if normalized in category:
            return category[normalized]
    return normalized


def get_unit_display_name_for_category(unit: str, category: str, lang: str = 'en') -> str:
    normalized = unit.lower()
    dictionary = UNIT_I18N_MAP.get(lang, UNIT_I18N_MAP['en'])
    localized_category = dictionary.get(category, {})
    return localized_category.get(normalized, normalized)


def get_error_messages(lang: str = 'en') -> dict:
    return ERROR_I18N_MAP.get(lang, ERROR_I18N_MAP['en'])


__all__ = ['get_unit_display_name', 'get_unit_display_name_for_category', 'get_error_messages']