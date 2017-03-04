import UnitOfWork

from app.TDG import UserTDG
from app.core.user import User


def __init__():
    pass


def makeNew(userId, name, password):
    user = User(userId, name, password)
    UnitOfWork.registerNew(user)
    return user


def find(userId):
    result = []
    result = UserTDG.find(userId)
    if not result:
        return
    else:
        return User(result[0][0], result[0][1], result[0][2])


def setUser(userId):
    user = find(userId)
    user.setName(user.getName())
    UnitOfWork.registerDirty(user)


def delete(userId):
    UnitOfWork.registerDeleted( User(userId,None,None) )


def done():
    UnitOfWork.commit()


def save(user):
    UserTDG.insert(
        user.getName(),
        user.getPassword()
    )


def update(user):
    UserTDG.update(
        user.getId(),
        user.getName(),
        user.getPassword()
    )


def erase(user):
    UserTDG.delete(user.getId())
