from flask import current_app, request, Blueprint
from flask.views import MethodView
from flask_login import login_required
from flask_login import login_required
from pet.pet_validator import PetValidator
from pet.model import Pets
from bson.json_util import dumps
from random import choice

class PetsAPIView(MethodView):

    @login_required
    def post(self):
        data = request.get_json()

        if not hasattr(current_app, 'current_user'):
            return '<h2>Cannot create pets</h2>\n'

        pet_validate = PetValidator()
        if pet_validate.can_create_pet(current_app.current_user.user):
            pets = Pets()
            role = current_app.current_user.user['role']

            petdata = data.get('data')

            if role == 'CUSTOMER':
                email = current_app.current_user.user['email']
            else:
                email = petdata.get('owner_email', current_app.current_user.user['email'])

            # Check if same record exists or not?
            available_pet = pets.get_a_pet({'name': petdata.get('name'), 'owner_email': email})
            if not available_pet:
                pets.create(data.get('data'), email)
                return '<h2>Created new pet</h2>\n', 200
            return '<h2>Pet already available</h2>\n', 401
        return '<h2>No privilege to create pet</h2>\n', 401

    @login_required
    def put(self):
        data = request.get_json()

        if not data.get('data'):
            return '<h2>Cannot update pet</h2>\n', 401
        if not hasattr(current_app, 'current_user'):
            return '<h2>Cannot update pet</h2>', 401

        pet_validate = PetValidator()
        petsdb = Pets()
        petData = petsdb.get_a_pet({'name': data.get('pet_name'), 'owner_email': data.get('owner_email')})

        try:
            print("Val = {}".format(pet_validate.can_update_pet(current_app.current_user.user, petData)))
            if pet_validate.can_update_pet(current_app.current_user.user, petData):
                petData['data'] = data.get('data')
                if ('checked_in' in petData['data']) and (not pet_validate.can_checkin_pet(current_app.current_user.user)):
                    return '<h2>Cannot update pet</h2>', 401
                petsdb.update(petData)
                return '<h2>Pet udpated successfully<h2>\n', 200
            else:
                return '<h2>Can not update the pet</h2>\n', 400
        except Exception as e:
            return '<h2>Can not update the pet</h2>\n', 400

    @login_required
    def get(self):
        petsdb = Pets()
        try:
            user = current_app.current_user.user
            if user['role'] == 'CUSTOMER':
                get_all_pets = petsdb.search(user['email'])
            else:
                get_all_pets = petsdb.search()

            if get_all_pets:
                return dumps(get_all_pets)
            return '<h2>Cannot fetch the pets</h2>\n' + '<p>' + dumps(list(get_all_pets)) + '</p\n'
        except Exception as e:
            return '<h2>Cannot fetch the pets</h2>\n'


    @login_required
    def delete(self):
        data = request.get_json()

        if not data.get('pet_name') and not data.get('owner_email'):
            return '<h2>Cannot delete pet</h2>\n', 401
        if not hasattr(current_app, 'current_user'):
            return '<h2>Cannot delete pet</h2>', 401

        pet_validate = PetValidator()

        if pet_validate.can_delete_pet(current_app.current_user.user):
            petsdb = Pets()
            try:
                petsdb.delete(data)
                return '<h2>Deleted the pet</h2>', 200
            except Exception as e:
                return '<h2>Cannot delete the pet</h2>', 401

        return '<h2>Cannot delete the pet</h2>', 401


class PetsHotelCheckin(MethodView):

    @login_required
    def put(self):
        data = request.get_json()

        if not data.get('pet_name') or not data.get('owner_email'):
            return '<h2>Cannot checkin the pet</h2>\n'

        pet_validate = PetValidator()
        petsdb = Pets()
        try:
            if pet_validate.can_checkin_pet(current_app.current_user.user):
                if data.get('room_number'):
                    room_available = petsdb.is_room_available(data.get('room_number'))
                    if not room_available: #meaning room is empty, go grab it
                        petsdb.checkin({'name': data.get('pet_name'), 'owner_email': data.get('owner_email')})
                        return '<h2>Pet checked in successfully</h2>\n', 200

                available_rooms = petsdb.available_rooms()
                print("available rooms = {}".format(available_rooms))
                if available_rooms.count() == current_app.config.get('HOTEL_ROOMS'):
                    return '<h2>No rooms available for checkin</h2>', 400

                exclude_rooms = [ int(room['room_number']) for room in available_rooms]
                allocated_room = choice([i for i in range(1, current_app.config.get('HOTEL_ROOMS') + 1) if i not in exclude_rooms])

                # if no rooms are provided for checkin then pick the one which is available
                petsdb.checkin({'name':data.get('pet_name'), 'owner_email': data.get('owner_email'), 'room_number': allocated_room})
                return '<h2>Pet checked in successfully</h2>', 200
            return '<h2>Cannot checkin the pet</h2>\n', 400
        except Exception as e:
            return '<h2>Cannot checkin the pet</h2>\n', 400


class PetsHotelCheckout(MethodView):

    @login_required
    def put(self):

        data = request.get_json()

        if not data.get('pet_name') or not data.get('owner_email'):
            return '<h2>Cannot checkout the pet</h2>\n'

        pet_validate = PetValidator()
        petsdb = Pets()
        pet_detail = petsdb.get_a_pet({'name': data.get('pet_name'), 'owner_email': data.get('owner_email')})
        if not pet_detail['room_number'] and not pet_detail['checked_in']:
            return '<h2>Pet had already checkedout </h2>\n', 400
        try:
            if pet_validate.can_checkin_pet(current_app.current_user.user):
                petsdb.checkout({'name': data.get('pet_name'), 'owner_email': data.get('owner_email')})
                return '<h2>Pet checked out successfully</h2>\n', 200
            return '<h2>Cannot checkout the pet</h2>\n', 400
        except Exception as e:
            return '<h2>Cannot checkout the pet</h2>\n', 400


pets_api = Blueprint("pets_action_api", __name__)
pets_checkin = Blueprint("pets_checkin_api", __name__)
pets_checkout = Blueprint("pets_checkout_api", __name__)


pets_api_view = PetsAPIView.as_view("pets_api_view")
pets_checkin_view = PetsHotelCheckin.as_view("pets_checkin_view")
pets_checkout_view = PetsHotelCheckout.as_view("pets_checkout_view")


# add the endpoints
pets_api.add_url_rule("/pet/create/", view_func=pets_api_view, methods=['POST',])
pets_api.add_url_rule("/pet/update/", view_func=pets_api_view, methods=['PUT',])
pets_api.add_url_rule("/pet/get/", view_func=pets_api_view, methods=['GET',])
pets_api.add_url_rule("/pet/delete/", view_func=pets_api_view, methods=['DELETE',])


pets_checkin.add_url_rule("/pet/checkin/", view_func=pets_checkin_view, methods=['PUT',])

pets_checkout.add_url_rule("/pet/checkout/", view_func=pets_checkout_view, methods=['PUT', ])