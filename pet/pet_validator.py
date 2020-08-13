"""
This is a validator class which helps the user know
if they can create/update-or-edit/delete the pet(s).
It also helps user to see if they can checkin the
pet to the hotel or not.
"""


class PetValidator:
    """
    There are 4 roles against which the checking is made.
    Here the user is validated to check if:
    - can create a pet
    - can delete a pet
    - can checkin a pet
    - can move a pet
    """

    allowed_roles = ("MANAGER", "STAFF", "CUSTOMER")

    def can_create_pet(self, user):
        """
        Check if the user can create a pet
        """
        if user["role"] in self.allowed_roles:
            return True
        return False

    @classmethod
    def can_update_pet(cls, user, pet):
        """
        Check if user can update the pet
        """
        if not pet["checked_in"]:
            return True
        if user["role"] == "CUSTOMER":
            return False
        return True

    @classmethod
    def can_checkin_pet(cls, user):
        """
        check if the user can checkin a pet
        """
        if user["role"] == "CUSTOMER":
            return False
        return True

    @classmethod
    def can_see_pet(cls, user):
        """
        check if the user can see a pet
        """
        if user["role"] == "CUSTOMER":
            return False
        return True

    @classmethod
    def can_move_pet(cls, user):
        """
        Check if the user can move a pet
        """
        if user["role"] == "MANAGER":
            return True
        return False

    @classmethod
    def can_delete_pet(cls, user):
        """
        Check if user can delete a pet
        """
        return user["role"] == "MANAGER"
        # return True if user["role"] == "MANAGER" else False
