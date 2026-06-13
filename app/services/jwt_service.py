from flask_jwt_extended import (
    create_access_token
)

class JWTService:

    @staticmethod
    def generate_token(user_id):

        return create_access_token(
            identity=str(user_id)
        )