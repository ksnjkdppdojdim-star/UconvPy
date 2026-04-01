ERROR_MESSAGES = {
    'unknownUnit': lambda unit: f'Unité inconnue : {unit}',
    'invalidInput': lambda value: f'Format d’entrée invalide : {value}',
    'incompatibleUnits': lambda src, dst: f'Conversion impossible de {src} vers {dst} : types incompatibles',
    'conversionFailed': lambda message: f'Échec de la conversion : {message}',
}