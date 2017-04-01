import UnitOfWork

from app.TDG import UserTDG
from app.core.user import User


def __init__():
    pass


def makeNew(username, password, capstone):
    user = User(username, password, capstone)
    UnitOfWork.registerNew(user)
    return user


def find(username):
    result = UserTDG.find(username)
    if not result:
        return
    else:
        return User(result[0][0], result[0][1], result[0][2])


def setUser(username):
    user = find(username)
    user.setName(user.getId())
    UnitOfWork.registerDirty(user)


def delete(username):
    UnitOfWork.registerDeleted( User(username,None,None) )


def done():
    UnitOfWork.commit()


def save(user):
    UserTDG.insert(
        user.getId(),
        user.getPassword(),
        user.isCapstone()
    )


def update(user):
    UserTDG.update(
        user.getId(),
        user.getPassword(),
        user.isCapstone()
    )


def erase(user):
    UserTDG.delete(user.getId())
