import os

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Godswill150@127.0.0.1:3306/MyMechanicShop_db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://testuser:testpass@127.0.0.1:3306/mechanicshop_test'
    TESTING = True
    DEBUG = False
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 1  # Usually shorter timeout for tests
class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds