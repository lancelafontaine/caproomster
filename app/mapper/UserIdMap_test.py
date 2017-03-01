from app.mapper import UserMapper
from app.mapper import UserIdMap


def test_clear():
    assert(len(UserIdMap.userList) is 0)
    user = UserMapper.find(1)
    assert(len(UserIdMap.userList) is 1)
    UserIdMap.clear()
    assert(len(UserIdMap.userList) is 0)
