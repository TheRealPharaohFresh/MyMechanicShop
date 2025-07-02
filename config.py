class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Godswill150@127.0.0.1:3306/MyMechanicShop_db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300  # Cache timeout in seconds

class TestingConfig:
    pass

class ProductionConfig:
    pass