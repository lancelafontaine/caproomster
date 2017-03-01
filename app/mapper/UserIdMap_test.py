from app.mapper import UserMapper
from app.mapper import UserIdMap


def test_clear():
    assert(len(UserIdMap.userList) is 0)
    UserIdMap.userList.append('a')
    assert(len(UserIdMap.userList) is 1)
    UserIdMap.clear()
    assert(len(UserIdMap.userList) is 0)
