from flask_login import login_user

from app import db, bcrypt
from .models import UserController


class AuthService:
    """Manager for handling user login and profile actions."""
    def __init__(self, username):
        self.user_controller = UserController()
        self.user = self.user_controller.getLogin(username=username)

    def login(self, password: str) -> None:
        """Login user."""
        self.user.authenticated = True
        db.session.commit()
        login_user(self.user)
                
    def validatePassword(self, password: str) -> bool:
        """Check if entered passowrd matches the corret one."""
        if self.user:
            is_valid = bcrypt.check_password_hash(self.user.password, password)
            return is_valid
        
        return False
    
    def changeEmail(self, old_email: str, new_email: str) -> bool:
        """Check if old email mathes, if so - update user email with new one."""
        if self.user:
            if self.user.email == old_email:
                self.user_controller.patch({
                    "id": self.user.id,
                    "email": new_email
                })
                return True
            
        return False

    def changePassword(self, old_password: str, new_password: str, confirm_password: str) -> bool:
        """Check if old password mathes, if so - update user password with new one."""
        if self.user:
            is_valid = bcrypt.check_password_hash(self.user.password, old_password)
            if is_valid and new_password == confirm_password:
                self.user_controller.patch({
                    "id": self.user.id,
                    "password": bcrypt.generate_password_hash(new_password).decode('utf-8')
                })

                return True

        return False