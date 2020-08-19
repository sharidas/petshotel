# Pets Hotel

The core idea behind this project is to have a hotel where humans allow pets to checkin and checkout. This is absolutely a fun project.
This is also my playground with flask. We learn all the day, so why not spread the wings and enhance our imagination. This project doesn't
have a UI "YET". The main focus is to create RESTful API's adhering to the flask patterns. 

#### Prerequisite

The prerequisite for this project is:
- Python 
- MongoDB


#### Start flask app

- Create a virtual environment as: `virtualenv --python python3 .env`

- Source activate script as `source .env/bin/activate`

- To start the flask app kindly install the prerequisite in requirements.txt as:

    ```pip install -r requirements.txt```

- Run the flask app as shown below:
    ```FLASK_APP=wsgi.py FLASK_ENV=development flask run```

- Make sure an email server configuration is made in the config.py. For the testing you can give a try with mailhog.
  But if you want to connect to a different mail server, then kindly update the configuration in config.py

- Also make sure your mongodb configurations are correct in config.py.


The humans who manage the hotel have 3 roles: "CUSTOMER", "STAFF" and "Manager".

### Roles

#### CUSTOMER

A customer is the one who can update(i.e, edit or delete) the data of pets who are not checked in. When a logged in, a customer can see the pets (of whom he/she is the owner).

#### STAFF

A staff is the one who can update the data of the pets. They can even checkin the pets. They can also checkout. They can invite the customer by email
address.

A staff can also edit, search and create pets. The staff should also be able to see who is the owner of the pet.


#### MANAGER

A manager can do all the operations what a staff can do, plus move the pets to other room and delete them.


NOTE: This is work in progress project.


### RESTful endpoint

Below are the endpoints available to user. Lets assume that flask is running in `localhost:5000`, else kindly change the url accordingly in the below
endpoints.

#### User

- CREATE user 
    - `curl -H 'Content-Type: application/json' -X POST -d '{"username":"user1", "password": "********", "email":"user1@test.com", "role": "STAFF"}' http://localhost:5000/user/signup/`
    
        The user will not be allowed to login after this. An email will be sent to the one configured in our config.py. So in our default setup it would be
        sent to mailhog. Open the email arrived in the inbox, and click the link to confirm. Once the link is clicked the user can login using the login endpoint.

- LOGIN user
    - `curl -H 'Content-Type: application/json' -X POST -d '{"password": "********", "email":"user1@test.com"}' http://localhost:5000/login/`
        
        The user can login only if the email confirmation link is clicked.

- UPDATE user
    - `curl -u "user1@test.com":"********" -H 'Content-Type: application/json' -X PUT -d '{"email":"user3@test.com", "data": {"role": "CUSTOMER"}}' http://localhost:5000/user/update/`

        The user can update the `role`, `email`, `allow_login` `username`, `password` of the user.

- DELETE user
    - `curl -u "user1@test.com":"********" -H 'Content-Type: application/json' -X DELETE -d '{"email":"user3@test.com"}' http://localhost:5000/user/remove/`

        The user can be deleted. But to delete the user, a user with privilege should be logged in.


#### Pet

- CREATE pet
    - `curl -u "user3@test.com":"********" -H 'Content-Type: application/json' -X POST -d '{"data": {"name":"Jerry", "room_number": "", "checked_in": "", "owner_email": "user3@test.com"}}' http://localhost:5000/pet/create/`
    
        This endpoint would help to create a new pet with name `Jimmy`. You can see that room number and checked in status are kept empty. The `owner_email` is the
        owner of the pet.

- UPDATE pet
    - `curl -u "user2@test.com":"********" -H 'Content-Type: application/json' -X PUT -d '{"pet_name": "Jimmy", "owner_email":"user3@test.com", "data": {"checked_in": 1, "room_number": 10}}' http://localhost:5000/pet/update/`

        This endpoint would allow the pet to checkin and specify the room number allocated. You may also update the name of the pet and change the owner of the pet.
        But remember that the login user should have the privilege to do the same.

- GET pet
    - `curl -u "user3@test.com":"********" http://localhost:5000/pet/get/`

        This endpoint will allow to get the pets owned by user3


#### Kubernetes Setup

As this setup relies on mailhog + flask, the yaml files are created by keeping the same in mind. This can be changed of-course :)

To test the same I have used minikube. I expect you to start minikube, so that you have access to `kubectl` and execute the steps shown below:

-  ```kubectl apply -f flask-app-deployment.yaml```
-  ```kubectl apply -f  mailhog-deployment.yaml```
-  ```kubectl apply -f flask-port.yaml``` 
-  ```kubectl apply -f mailhog-port.yaml```

Now we could have used CoreDNS to get the flask app pod access the mailhog pod. But instead I make it simple, edit the /etc/hosts of the flask app pod and add the ip address of mailhog :)

Not yet done, don't you wanna see the mailhog web ui in your localhost? Of-course.

So just execute the step below:

- ```kubectl port-forward <name-of-mailhog-pod> 8025```

Verified the user creation and login with this setup.

