class UserAlreadyExistsError(Exception):
    """When trying to save a user that alreadys exists in the database"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UserDoesNotExistsError(Exception):
    """When the user does not in the database"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class IncorrectCredentialsToLoginError(Exception):
    """When used the incorrect credentials to log in the site"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class IncorrectUserDataError(Exception):
    """When used the incorrect user data"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DuplicateRegisterError(Exception):
    """When the database have two registers with the same email"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class AuthenticationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

