import pytest
import unittest
from wsgi import app
from flask_mail import Mail
import json

class UserAPITest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def initapp(self):
        yield True
        app.userdb.db.user.drop()

    
    def test_create_user(self):
        client = app.test_client()
        mail = Mail(app)
        with mail.record_messages() as outbox:
            response = client.post('/user/signup/', 
                    data=json.dumps(dict(username="user1", password="passwd1", email="user1@test.com", role="STAFF")), 
                    content_type='application/json')
            
            assert "To signup, kindly click on the link" in outbox[0].body
            assert "/user/signup/" in outbox[0].body
            assert response.status_code == 200
            assert "<h2>Created user successfully.</h2>" == response.get_data().decode('utf-8')

            # Now try to create same user again and test the output
            response1 = client.post('/user/signup/', 
                    data=json.dumps(dict(username="user1", password="passwd1", email="user1@test.com", role="STAFF")), 
                    content_type='application/json')

            assert response1.status_code == 401
            assert "User already exists." == response1.get_data().decode('utf-8')


    def test_update_user(self):
        from base64 import b64encode
        client = app.test_client()

        response = client.post('/user/signup/', 
                    data=json.dumps(dict(username="admin", password="admin", email="admin@test.com", role="MANAGER")), 
                    content_type='application/json')

        assert response.status_code == 200

        response = client.post('/user/signup/', 
                    data=json.dumps(dict(username="user1", password="passwd1", email="user1@test.com", role="CUSTOMER")), 
                    content_type='application/json')

        assert response.status_code == 200

        # The manager should be able to update the CUSTOMER
        headers = {'Authorization': 'Basic %s' % b64encode(b"admin@test.com:admin").decode('ascii')}
        response_update = client.put('/user/update/',
                            data=json.dumps(dict(email='user1@test.com', data={'role': 'STAFF'})),
                            headers=headers, content_type='application/json')
        
        assert response_update.status_code == 200
        assert response_update.get_data().decode('utf-8') == '<h2>updated the data</h2>'






