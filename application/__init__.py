from flask import Flask, current_app, request
from flask_pymongo import PyMongo
from flask_login import LoginManager
from user.user_views import user_api, user_auth_api, UserAuthentication
from pet.pet_views import pets_api, pets_checkin, pets_checkout
from config import ProductionConfig, DevelopmentConfig, TestingConfig

def create_app(env=None):

    app = Flask(__name__)

    with app.app_context():
        if env == 'production':
            app.config.from_object(__name__ + '.ProductionConfig')
        elif env == 'development':
            app.config.from_object('config.DevelopmentConfig')
        else:
            app.config.from_object('config.TestingConfig')

        login_manager = LoginManager()
        login_manager.init_app(app)

        userdb = PyMongo(app)
        petsdb = PyMongo(app)

        current_app.userdb = userdb
        current_app.petsdb = petsdb
        current_app.login_manager = login_manager

        app.register_blueprint(user_api)
        app.register_blueprint(user_auth_api)

        app.register_blueprint(pets_api)
        app.register_blueprint(pets_checkin)
        app.register_blueprint(pets_checkout)


        # Personally I didn't liked the solution to have auth inside this app
        # The reason I kept it here is: I couldn't find an elagent way to use
        # the same inside user view :( In case anyone has got a better idea,
        # then it would be nice.

        # Login required
        @login_manager.request_loader
        def load_user_from_request(request):

            user_auth = UserAuthentication()
            return_val = user_auth.post()
            if return_val[1] == 401:
                return None
            if hasattr(current_app, 'current_user'):
                return current_app.current_user
            return None

    return app


