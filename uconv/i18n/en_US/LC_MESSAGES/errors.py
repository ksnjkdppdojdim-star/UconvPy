ERROR_MESSAGES = {
    'unknownUnit': lambda unit: f'Unknown unit: {unit}',
    'invalidInput': lambda value: f'Invalid input format: {value}',
    'incompatibleUnits': lambda src, dst: f'Cannot convert from {src} to {dst}: incompatible unit types',
    'conversionFailed': lambda message: f'Conversion failed: {message}',
}