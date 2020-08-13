"""
This is the configuration used by the flask app 
for production, development and testing
"""


class Config:
    """
    The parent class which gets populated with the attributes
    based on the environment sourced
    """

    pass


class ProductionConfig(Config):
    """
    This configuration is used for the production
    """

    DEBUG = True
    TESTING = False
    SESSION_TYPE = "filesystem"
    SECRET_KEY = "Thisisasecretkey"  # modify this to a different value
    TOKEN_LIFE = 3600  # 1 hour
    MAIL_SENDER = "test@foo.com"
    MAIL_SERVER = "0.0.0.0"
    MAIL_PORT = 1025
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    HOTEL_ROOMS = 200
    MONGO_URI = "mongodb://localhost:27017/pet-hotel"


class DevelopmentConfig(Config):
    """
    This configuration is used for the development
    """

    DEBUG = True
    TESTING = True
    SESSION_TYPE = "filesystem"
    SECRET_KEY = "Thisisasecretkey"  # modify this to a different value
    TOKEN_LIFE = 3600  # 1 hour
    MAIL_SENDER = "test@foo.com"
    MAIL_SERVER = "0.0.0.0"
    MAIL_PORT = 1025
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    HOTEL_ROOMS = 200
    MONGO_URI = "mongodb://localhost:27017/pet-hotel"


class TestingConfig(Config):
    """
    This configuration is used for the testing
    """

    DEBUG = False
    TESTING = True
    MONGO_URI = "mongodb://localhost:27017/testdb"
    SESSION_TYPE = "filesystem"
    SECRET_KEY = "Thisisasecretkey"  # modify this to a different value
    TOKEN_LIFE = 3600  # 1 hour
    MAIL_SENDER = "test@foo.com"
    MAIL_SERVER = "0.0.0.0"
    MAIL_PORT = 1025
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    HOTEL_ROOMS = 200
