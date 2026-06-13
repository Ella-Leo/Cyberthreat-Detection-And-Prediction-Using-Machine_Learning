import re

class AuthValidator:

    @staticmethod
    def validate_password(password):

        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$'

        return re.match(
            pattern,
            password
        )