from flask import Blueprint, request, url_for, current_app
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from user.model import User

class UserAPIView(MethodView):

    def create_and_send_mail(self):
        urlsafetime = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        role = data.get('role')

        user = User()

        # check if the user already exists
        if not user.get_user(email=email):
            user.create_user(username=username, password=password, email=email, role=role)
            token = urlsafetime.dumps(email, salt='email-confirm')
            msg = Message('Confirm Email', recipients=[email], sender=current_app.config.get('MAIL_SENDER'))
            #link = url_for('email_confirm_view.email_api_view', token=token, _external=True)
            link = url_for('user_action_view.user_api_view', token=token, _method='GET', _external=True)
            msg.body = 'To signup, kindly click on the link {}'.format(link)
            mail = Mail(current_app._get_current_object())
            mail.send(msg)
        else:
            raise ValueError("User already exists.")

    
    def post(self):
        try:
            self.create_and_send_mail()
            return '<h2>Created user successfully.</h2>', 200
        except ValueError as e:
            return f'{e}', 401

    def put(self):
        data = request.get_json()
        if hasattr(current_app, 'current_user'):
            if current_app.current_user.user['role'] == 'CUSTOMER':
                return '<h2>Do not have privilege to update the user</h2>'

        user = User()
        try:
            user.update_user(data.get('email'), data.get('data'))
        except ValueError as e:
            print(e)
    
        return '<h2>updated the data</h2>'

    def get(self, token):
        try:

            urlsafetime = URLSafeTimedSerializer(current_app.config.get('SECRET_KEY'))
            email = urlsafetime.loads(token, salt='email-confirm', max_age=current_app.config['TOKEN_LIFE'])
            
            user = User()
            user_obj = user.get_user(email=email)
            user.set_allow_login(user_obj)

            return '<h1>Now user can login</h1>', 200
        except SignatureExpired as e:
            return '<h2>The token is expired</h2>', 401

    
    @login_required
    def delete(self):
        data = request.get_json()
        if hasattr(current_app, 'current_user'):
            if current_app.current_user.user['role'] == 'CUSTOMER':
                return '<h2>Cannot delete the user</h2>'
        
            if current_app.current_user.user['email'] == data.get('email'):
                return '<h2>Cannot delete the user</h2>'

        user = User()
        try:
            user.delete_user(data.get('email'))
        except Exception as e:
            print(e)
            return f'{e}', 401
        return '<h2>Deleted the user</h2>', 200


class UserAuthentication(MethodView):

    def post(self):
        data = {}
        if request.data:
            data = request.get_json()
        user = User()

        if request.authorization:
            username = request.authorization['username']
        elif data.get('email'):
            username = data.get('email')
        else:
            return '<h2>Kindly provide user name to login</h2>'

        if request.authorization:
            password = request.authorization['password']
        elif data.get('password'):
            password = data.get('password')
        else:
            return '<h2>Kindly provide password to login</h2>'

        try:
            user_object = user.allow_login(username, password)
            if user_object:
                login_user(user_object, force=True)
                current_app.current_user = user_object
                return '<h2>logged in successfully...</h2>\n', 200
            return '<h2>Cannot login</h2>', 401
        except ValueError as e:
            return str(e), 401


    @login_required
    def get(self):
        logout_user()
        return '<h2>User logged out successfully</h2>'


user_api = Blueprint("user_action_view", __name__)
user_api_view = UserAPIView.as_view("user_api_view")

user_api.add_url_rule('/user/signup/', view_func=user_api_view, methods=["POST",])
user_api.add_url_rule('/user/signup/<token>', view_func=user_api_view, methods=["GET",])
user_api.add_url_rule('/user/remove/', view_func=user_api_view, methods=['DELETE',])
user_api.add_url_rule('/user/update/', view_func=user_api_view, methods=['PUT',])

#email_api = Blueprint("email_confirm_view", __name__)
#email_api_view = EmailConfirm.as_view("email_api_view")

#email_api.add_url_rule("/confirm_email/<token>", view_func=email_api_view, methods=['GET'])

user_auth_api = Blueprint("user_auth_api", __name__)
user_auth_api_view = UserAuthentication.as_view("user_auth_api_view")

user_api.add_url_rule('/login/', view_func=user_auth_api_view, methods=['POST',])
user_api.add_url_rule('/logout/', view_func=user_auth_api_view, methods=['GET',])


