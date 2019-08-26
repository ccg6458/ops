import os
from .settings_dev import DevConfig
from .settings_prod import ProdConfig

if os.environ.get('USER',0) == 'mc':
    Config = DevConfig
else:
    Config = ProdConfig
