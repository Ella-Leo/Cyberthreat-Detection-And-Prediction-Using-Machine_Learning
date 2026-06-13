from app.models.user import User

class UserRepository:

    @staticmethod
    def get_by_email(email):

        return User.query.filter_by(
            email=email
        ).first()

    @staticmethod
    def get_by_username(username):

        return User.query.filter_by(
            username=username
        ).first()

    @staticmethod
    def create(user):

        from app import db

        db.session.add(user)
        db.session.commit()