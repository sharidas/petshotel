import bcrypt
from flask_login import UserMixin
from email_validator import validate_email, EmailNotValidError
from flask import Blueprint, current_app

class User(UserMixin):
    
    ROLES = ('MANAGER', 'STAFF', 'CUSTOMER', 'ADMIN')

    def create_user(self, username=None, password=None, email=None, role=None):
        if not username:
            raise ValueError("Invalid username")
        if not password:
            raise ValueError("Invalid password")
        if not email:
            raise ValueError("Invalid email")
        if not role:
            role = "CUSTOMER"
        
        userdb = current_app.userdb

        # check if the user is already available in the db
        user = userdb.db.user.find_one({'email': email})
        if user:
            raise ValueError("The user is already present. Check the Username, Password or Email again.")

        if type(role) == str:
            if role not in self.ROLES:
                raise ValueError("Invalid role provided. Kindly check the docs.\nBelow are the accepted values:\nMANAGER, STAFF and CUSTOMER")
        else:
            raise ValueError("Invalid role provided. Kindly provide one of the details below:\nMANAGER, STAFF and CUSTOMER")

        # hash the password
        salt = bcrypt.gensalt()
        new_passwd = bcrypt.hashpw(bytes(password, 'utf-8'), salt)
        userdb.db.user.insert(
            {
                'username': username,
                'password': new_passwd,
                'email': email,
                'role': role,
                'allow_login': ''
            }
        )

    def update_user(self, email=None, data=None):
        if not email:
            raise ValueError("Invalid email")
        if not data:
            raise ValueError("Provide the details to update")

        # The list needs to be updated if we add new fields
        userupdate = {key:value for key, value in data.items() if key in ['username', 'password', 'email', 'role', 'allow_login']}
        for key in userupdate:
            if key == 'email':
                try:
                    valid = validate_email(userupdate[key])
                    userupdate[key] = valid.email
                except EmailNotValidError as e:
                    print(e)
                    return
            if key == 'role':
                if userupdate[key] not in ['MANAGER', 'STAFF', 'CUSTOMER']:
                    raise ValueError("Invalid role provided. Kindly provide one of the details below:\nMANAGER, STAFF and CUSTOMER")
            if key == 'password':
                # hash the password
                salt = bcrypt.gensalt()
                new_passwd = bcrypt.hashpw(bytes(userupdate[key], 'utf-8'), salt)
                userupdate[key] = new_passwd
                
        if len(userupdate) > 0:
            # time to persist data
            userdb = current_app.userdb
            userupdate = {"$set": userupdate}
            userdb.db.user.update_one({"email": email}, userupdate)

    def delete_user(self, email=None):
        if not email:
            raise ValueError("Invalid email")

        userdb = current_app.userdb
        user = userdb.db.user.find_one({'email': email})

        if not user:
            raise ValueError("No user exist with the data provided.")

        try:
            userdb.db.user.delete_one({'email': email})
        except Exception as e:
            print(e)

    def get_user(self, email=None):
        if not email:
            return 'Can not get the user'
        
        userdb = current_app.userdb
        return userdb.db.user.find_one({'email': email}, {'_id': 0})

    def set_allow_login(self, user=None):
        if not user:
            return 'Cannot allow login'
        
        userdb = current_app.userdb
        userdb.db.user.update_one({'email': user.get('email')}, {"$set": {'allow_login': 1}})

    def allow_login(self, email=None, password=None):
        if not email or not password:
            raise Exception("Invalid username or password")

        userdb = current_app.userdb
        user = userdb.db.user.find_one({'email': email})

        if not user:
            raise ValueError("No user found with the email provided.")

        if not user.get('allow_login'):
            raise ValueError("Can not login")

        if bcrypt.checkpw(bytes(password, 'utf-8'), user['password']):
            user['is_authenticated'] = True
            user['is_active'] = True
            user['is_anonymous'] = False
            self.user = user
            return self
        return False

    def get_id(self):
        return self.user['email']


user_model = Blueprint("user_model", __name__)



