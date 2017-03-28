import UnitOfWork

from app.TDG import UserTDG
from app.core.user import User


def __init__():
    pass


def makeNew(userId, name, password, capstone):
    user = User(userId, name, password, capstone)
    UnitOfWork.registerNew(user)
    return user


def find(userId):
    result = UserTDG.find(userId)
    if not result:
        return
    else:
        return User(result[0][0], result[0][1], result[0][2], result[0][3])


def setUser(userId):
    user = find(userId)
    user.setName(user.getName())
    UnitOfWork.registerDirty(user)


def delete(userId):
    UnitOfWork.registerDeleted( User(userId,None,None,None) )


def done():
    UnitOfWork.commit()


def save(user):
    UserTDG.insert(
        user.getName(),
        user.getPassword(),
        user.isCapstone()
    )


def update(user):
    UserTDG.update(
        user.getId(),
        user.getName(),
        user.getPassword(),
        user.isCapstone()
    )


def erase(user):
    UserTDG.delete(user.getId())
