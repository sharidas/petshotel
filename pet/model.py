from flask import current_app

class Pets():
    def create(self, petdata=None, email=None):
        if not petdata or not email:
            print("Cannot create pet")
            return None
        
        petsdb = current_app.petsdb
        petsdb.db.pets.insert(
            {
                'name': petdata.get('name'),
                'room_number': petdata.get('room_number'),
                'checked_in': petdata.get('checked_in'),
                'owner_email': email,
            }
        )

    def update(self, petdata=None):
        if not petdata:
            return '<h2>Nothing to update for the pet</h2>'

        if petdata.get('name') and petdata.get('owner_email') and (petdata.get('data') != None):
            petname, owner_email, update_data = petdata.get('name'), petdata.get('owner_email'), petdata.get('data')
            update_data = {"$set": update_data}
            petsdb = current_app.petsdb
            petsdb.db.pets.update_one(petsdb.db.pets.find_one({'name': petname, 'owner_email': owner_email}), update_data)

    def delete(self, petdata=None):
        if not petdata:
            print("Cannot delete pet")
            return None

        petsdb = current_app.petsdb
        try:
            print("email = {}, name = {}".format(petdata['owner_email'], petdata['pet_name']))
            petsdb.db.pets.delete_one({'owner_email': petdata['owner_email'], 'name': petdata['pet_name']})
        except Exception as e:
            print(e)

    def checkin(self, petdata=None):
        if not petdata:
            return '<h2>Cannot checkin the pet</h2>'

        if petdata.get('name') and petdata.get('owner_email') and petdata.get('room_number'):
            petsdb = current_app.petsdb
            getpet = petsdb.db.pets.find_one({'name': petdata.get('name'), 'owner_email': petdata.get('owner_email')})
            petsdb.db.pets.update_one(getpet, {"$set": {'checked_in': 1, 'room_number': petdata.get('room_number')}})

    def checkout(self, petdata=None):
        if not petdata:
            return '<h2>Cannot checkin the pet</h2>'
        
        if petdata.get('name') and petdata.get('owner_email'):
            petsdb = current_app.petsdb
            getpet = petsdb.db.pets.find_one({'name': petdata.get('name'), 'owner_email': petdata.get('owner_email')})
            petsdb.db.pets.update_one(getpet, {"$set": {'checked_in': '', 'room_number': ''}})

    def is_room_available(self, room_number=None):
        if not room_number:
            return 'Can not find the room'
        
        petsdb = current_app.petsdb
        return petsdb.db.pets.find_one({'room_number': room_number})
    
    def available_rooms(self):
        petsdb = current_app.petsdb
        return petsdb.db.pets.find({"room_number": {"$ne": ""}})

    def search(self, email=None):
        petsdb = current_app.petsdb
        search_query = {} if not email else {'owner_email': email}
        return petsdb.db.pets.find(search_query, {'_id': 0})

    def get_a_pet(self, petdata=None):
        if not petdata:
            print("Cannot get the data for the pet")
            return None

        try:
            petsdb = current_app.petsdb
            pet = petsdb.db.pets.find_one(petdata)
            return pet
        except Exception as e:
            return None