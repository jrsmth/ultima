class Config(object):
    ENV = "local"
    APP_URL = "http://localhost:8080"
    REDIS_URL = "redis://@localhost:6379/0"
    USERNAME = "noah"
    PASSWORD = "ark"
    # Note :: Security risk - ideally would store creds as env-var in some sort of trust store and inject at runtime


class DevConfig(Config):
    ENV = "dev"
    APP_URL = "http://localhost:8080"
    REDIS_URL = "rediss://red-cklv99jj89us738u33i0:c1vXNdmZhDpXxxOTrkEsaBM9m9Kgk67z@frankfurt-redis.render.com:6379"


class ProductionConfig(Config):
    ENV = "prod"
    APP_URL = "https://www.ultima.jrsmth.io/"
    REDIS_URL = 'redis://red-cklv99jj89us738u33i0:6379'
