# User object
class User:

    # Constructor
    def __init__(self):
        pass

    def __init__(self, username, password, capstone=False):
        self.username = username
        self.password = password
        self.capstone = capstone

    # Accessors and Mutators
    def getId(self):
        return self.username

    def setId(self, username):
        self.username = username

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = password

    def isCapstone(self):
        return self.capstone

    def __str__(self):
        return '<Id: ' + str(self.userId) + ', Name:' + str(self.name) + '>'
