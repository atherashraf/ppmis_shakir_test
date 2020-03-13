
CONNECTION_KEY_TESTS = {
    # 'SPATIAL_ADMIN': {
    #     'DB_KEY': 'ferrp_admin',
    #     'APPS': ['spatial_admin'],
    #     'MODELS': [],
    #     'TABLES': []
    # },
    # 'SPATIAL_DS': {
    #     'DB_KEY': 'spatialds',
    #     'APPS': ['spatial_ds'],
    #     'MODELS': [],
    #     'TABLES': []
    # },
    'FOCUS': {
        'DB_KEY': 'focus',
        'APPS': ['akah'],
        'MODELS': [],
        'TABLES': []
    },
    'DEFAULT': {
        'DB_KEY': 'default',
        'APPS': ['default'],
        'MODELS': [],
        'TABLES': []
    }
}

MODEL_FIELD_TYPES = {
    "spatial": ['GeometryField', 'PointField', 'LineStringField', 'PolygonField',
                'MultiPointField', 'MultiLineStringField', 'MultiPolygonField',
                'GeometryCollectionField', 'RasterField'],
    "number": ['AutoField', 'BigAutoField', 'BigIntegerField', 'DecimalField', 'DurationField', 'FloatField',
               'IntegerField', 'PositiveIntegerField', 'PositiveSmallIntegerField', 'SmallIntegerField'],
    "date": ['DateField', 'DateTimeField', 'TimeField'],
    "string": ['CharField', 'EmailField', 'FilePathField', 'TextField'],
    "others": ['BinaryField', 'BooleanField', 'FileField', 'FileField and FieldFile',
               'ImageField', 'GenericIPAddressField', 'NullBooleanField', 'SlugField', 'URLField', 'UUIDField']
}