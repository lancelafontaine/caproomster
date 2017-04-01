from app.mapper import UserMapper
from app.mapper import IdMap
from app.core.user import User
from app.TDG import UserTDG


def teardown_module(module):
    IdMap.clear(User)


def test_find_not_found_in_id_map_not_found_in_DB(monkeypatch):
    # Mock
    def no_find(_):
        return
    def no_find2(_, __):
        return
    monkeypatch.setattr(IdMap, 'find', no_find2)
    monkeypatch.setattr(UserTDG, 'find', no_find)

    # Execute
    val = UserMapper.find(1)

    # Verify
    assert(val is None)


def test_find_not_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    expected = User('joe', 'shmoe')

    # Mock
    def no_find(_, __):
        return

    def yes_find(_):
        return [[expected.getId(), expected.getPassword(), expected.isCapstone()]]

    monkeypatch.setattr(IdMap, 'find', no_find)
    monkeypatch.setattr(UserTDG, 'find', yes_find)

    # Execute
    val = UserMapper.find(1)

    # Verify
    assert(val.getPassword() is expected.getPassword())
    assert(val.getId() is expected.getId())


def test_find_found_in_id_map_not_found_in_DB(monkeypatch):
    # Test Data
    expected = User('joel', 'shmoel', True)

    # Mock
    def id_find(_,__):
        return expected

    def no_find(_):
        return

    monkeypatch.setattr(IdMap, 'find', id_find)
    monkeypatch.setattr(UserTDG, 'find', no_find)

    # Execute
    val = UserMapper.find(1)

    # Verify
    assert(val.getPassword() is expected.getPassword())
    assert(val.getId() is expected.getId())
    assert(val.isCapstone() is expected.isCapstone())


def test_find_found_in_id_map_found_in_DB(monkeypatch):
    # Test Data
    unexpected = User('joe', 'shmoe',False)
    expected = User('joel', 'shmoel',False)

    # Mock
    def id_find(_,__):
        return expected

    def tdg_find(_):
        return [[unexpected.getId(), unexpected.getPassword()]]

    monkeypatch.setattr(IdMap, 'find', id_find)
    monkeypatch.setattr(UserTDG, 'find', tdg_find)

    # Execute
    val = UserMapper.find(1)

    # Verify
    assert(val.getPassword() is expected.getPassword())
    assert(val.getId() is expected.getId())
    assert(val.isCapstone() is expected.isCapstone())
