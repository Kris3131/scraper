from .default import BaseConfig

class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
    DB_PATH = "data/prod.db"
    MAX_CONCURRENT_REQUESTS = 5
