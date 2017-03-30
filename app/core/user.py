# User object
class User:

    # Constructor
    def __init__(self):
        pass

    def __init__(self, userId, name, password, capstone=False):
        self.name = name
        self.password = password
        self.userId = userId
        self.capstone = capstone

    # Accessors and Mutators
    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getPassword(self):
        return self.password

    def setPassword(self, password):
        self.password = password

    def getId(self):
        return self.userId

    def setId(self, userId):
        self.userId = userId

    def setCapstone(self, capstone=True):
        self.capstone = capstone

    def isCapstone(self):
        return self.capstone

    def __str__(self):
        return '<Id: ' + str(self.userId) + ', Name:' + str(self.name) + '>'
