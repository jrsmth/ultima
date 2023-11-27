class Config(object):
    APP_URL = "http://localhost:8080"
    REDIS_URL = "redis://@localhost:6379/0"


class DevConfig(Config):
    APP_URL = "http://localhost:8080"
    REDIS_URL = "rediss://red-cklv99jj89us738u33i0:c1vXNdmZhDpXxxOTrkEsaBM9m9Kgk67z@frankfurt-redis.render.com:6379"


class ProductionConfig(Config):
    APP_URL = "https://www.ultima.jrsmth.io/"
    REDIS_URL = 'redis://red-cklv99jj89us738u33i0:6379'
