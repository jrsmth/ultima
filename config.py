class Config(object):
    REDIS_URL = "redis://@localhost:6379/0"


class DevConfig(object):
    REDIS_URL = "rediss://red-cklv99jj89us738u33i0:c1vXNdmZhDpXxxOTrkEsaBM9m9Kgk67z@frankfurt-redis.render.com:6379"


class ProductionConfig(Config):
    REDIS_URL = 'redis://red-cklv99jj89us738u33i0:6379'
