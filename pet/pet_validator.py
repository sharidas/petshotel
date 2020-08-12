class PetValidator():
    allowed_roles = ('MANAGER', 'STAFF', 'CUSTOMER')
    def can_create_pet(self, user):
        '''
        Check if the user can create a pet
        '''
        if user['role'] in self.allowed_roles:
            return True
        return False

    def can_update_pet(self, user, pet):
        if not pet['checked_in']:
            return True
        else:
            if user['role'] == 'CUSTOMER':
                return False
            return True

    def can_checkin_pet(self, user):
        if user['role'] == 'CUSTOMER':
            return False
        return True

    def can_see_pet(self, user):
        if user['role'] == 'CUSTOMER':
            return False
        return True

    def can_move_pet(self, user):
        if user['role'] == 'MANAGER':
            return True
        return False

    def can_delete_pet(self, user):
        return True if user['role'] == 'MANAGER' else False

