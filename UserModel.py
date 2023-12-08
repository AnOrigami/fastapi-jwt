class User:
    def __init__(self, username, hash_password, sex, email, active, role):
        self.username = username
        self.hash_password = hash_password
        self.sex = sex
        self.email = email
        self.active = active
        self.role = role