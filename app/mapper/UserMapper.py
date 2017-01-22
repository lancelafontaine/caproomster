import UserIdMap
import UnitOfWork

from app.TDG import UserTDG

from app.core.user import User



def __init__():
    pass


def makeNew(name, password):
    user = User(name, password)
    UserIdMap.addTo(user)
    UnitOfWork.registerNew(user)
    return user


def find(userId):
    user = UserIdMap.find(userId)

    result = []
    if user is None:
        result = UserTDG.find(userId)
        if not result:
            return
        else:
            user = User(result[0][0], result[0][1], result[0][2])
            UserIdMap.addTo(user)
    return user

def getUser(userId):
    user = UserIdMap.find(userId)
    return user

def setUser(userId):
    user = find(userId)
    user.setName(userId.getName())
    UnitOfWork.registerDirty(user)


def delete(userId):
    user = UserIdMap.find(userId)
    if user is not None:
        UserIdMap.removeFrom(user)
    UnitOfWork.registerDeleted(user)

def done():
    UnitOfWork.commit()

def save(user):
    UserTDG.insert(user)

def update(user):
    UserTDG.update(user)

def erase(userId):
    UserTDG.delete(userId)
