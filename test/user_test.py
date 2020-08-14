"""
Test for user api
"""
import re
import json
from base64 import b64encode
import unittest
import pytest
from flask_mail import Mail
from wsgi import app

class UserAPITest(unittest.TestCase):
    """
    Test for user API
    """

    @pytest.fixture(autouse=True)
    def initapp(self):
        """
        Initialize the app and delete the db after the tests
        """
        yield True
        if hasattr(app, "userdb"):
            app.userdb.db.user.drop()


    def test_create_user(self):
        """
        Test creating an user
        """
        client = app.test_client()
        mail = Mail(app)
        with mail.record_messages() as outbox:
            response = client.post(
                "/user/signup/",
                data=json.dumps(
                    dict(
                        username="user1",
                        password="passwd1",
                        email="user1@test.com",
                        role="STAFF",
                    )
                ),
                content_type="application/json",
            )

            assert "To signup, kindly click on the link" in outbox[0].body
            assert "/user/signup/" in outbox[0].body
            assert response.status_code == 200
            assert (
                response.get_data().decode("utf-8")
                == "<h2>Created user successfully.</h2>"
            )

            # Now try to create same user again and test the output
            response1 = client.post(
                "/user/signup/",
                data=json.dumps(
                    dict(
                        username="user1",
                        password="passwd1",
                        email="user1@test.com",
                        role="STAFF",
                    )
                ),
                content_type="application/json",
            )

            assert response1.status_code == 401
            assert response1.get_data().decode("utf-8") == "User already exists."

    def test_update_user(self):
        """
        Test updating an user
        """

        client = app.test_client()

        response = client.post(
            "/user/signup/",
            data=json.dumps(
                dict(
                    username="admin",
                    password="admin",
                    email="admin@test.com",
                    role="MANAGER",
                )
            ),
            content_type="application/json",
        )

        assert response.status_code == 200

        response = client.post(
            "/user/signup/",
            data=json.dumps(
                dict(
                    username="user1",
                    password="passwd1",
                    email="user1@test.com",
                    role="CUSTOMER",
                )
            ),
            content_type="application/json",
        )

        assert response.status_code == 200

        # The manager should be able to update the CUSTOMER
        headers = {
            "Authorization": "Basic %s"
                             % b64encode(b"admin@test.com:admin").decode("ascii")
        }
        response_update = client.put(
            "/user/update/",
            data=json.dumps(dict(email="user1@test.com", data={"role": "STAFF"})),
            headers=headers,
            content_type="application/json",
        )

        assert response_update.status_code == 200
        assert response_update.get_data().decode("utf-8") == "<h2>updated the data</h2>"


    def test_user_remove(self):
        """
        Test removal of users created
        """

        client = app.test_client()

        mail = Mail(app)
        with mail.record_messages() as outbox:
            response = client.post(
                "/user/signup/",
                data=json.dumps(
                    dict(
                        username="admin",
                        password="admin",
                        email="admin@test.com",
                        role="MANAGER",
                    )
                ),
                content_type="application/json",
            )

            assert response.status_code == 200
            url_allow_login = re.search(r'(\/user\/signup\/.*)', outbox[0].body).group()

            allow_login_response = client.get(url_allow_login, content_type="application/json")

            assert allow_login_response.status_code == 200

        response = client.post(
            "/user/signup/",
            data=json.dumps(
                dict(
                    username="user1",
                    password="passwd1",
                    email="user1@test.com",
                    role="CUSTOMER",
                )
            ),
            content_type="application/json",
        )

        assert response.status_code == 200


        headers = {
            "Authorization": "Basic %s"
                             % b64encode(b"admin@test.com:admin").decode("ascii")
        }
        delete_response = client.delete(
            "/user/remove/",
            data=json.dumps(dict(email="user1@test.com")),
            headers=headers,
            content_type="application/json",
        )

        assert delete_response.status_code == 200
        assert delete_response.get_data().decode("utf-8") == "<h2>Deleted the user</h2>"


    def test_login_and_logout_user(self):
        client = app.test_client()

        mail = Mail(app)
        with mail.record_messages() as outbox:
            response = client.post(
                "/user/signup/",
                data=json.dumps(
                    dict(
                        username="admin",
                        password="admin",
                        email="admin@test.com",
                        role="MANAGER",
                    )
                ),
                content_type="application/json",
            )

            assert response.status_code == 200
            url_allow_login = re.search(r'(\/user\/signup\/.*)', outbox[0].body).group()

            allow_login_response = client.get(url_allow_login, content_type="application/json")

            assert allow_login_response.status_code == 200

        headers = {
            "Authorization": "Basic %s"
                             % b64encode(b"admin@test.com:admin").decode("ascii")
        }
        login_response = client.post(
            "/login/",
            headers=headers,
            content_type="application/json",
        )

        assert login_response.status_code == 200
        assert login_response.get_data().decode("utf-8") == "<h2>logged in successfully...</h2>\n"


        logout_response = client.get(
            "/logout/",
            headers=headers,
            content_type="application/json",
        )

        assert logout_response.status_code == 200
        assert logout_response.get_data().decode("utf-8") == "<h2>User logged out successfully</h2>"
