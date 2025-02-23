import os
from .development import DevelopmentConfig
from .production import ProductionConfig

def get_config():
    env = os.getenv('ENV', 'development')
    
    if env == 'production':
        return ProductionConfig
    
    return DevelopmentConfig

config = get_config()
