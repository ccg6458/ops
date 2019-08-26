from .settings import Config


class DevConfig(Config):
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PASSWORD = ''
    pass
