from .default import BaseConfig

class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True
    DB_PATH = "data/dev.db"
    MAX_CONCURRENT_REQUESTS = 2
