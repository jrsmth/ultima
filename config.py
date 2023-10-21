class Config(object):
    REDIS_URL = "redis://@localhost:6379/0"


class ProductionConfig(Config):
    REDIS_URL = 'redis://red-cklv99jj89us738u33i0:6379'