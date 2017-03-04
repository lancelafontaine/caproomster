from app.core.registry import Registry
from app.core.reservationbook import ReservationBook
from app.core.directory import Directory
import pytest


def test_valid_registry_init():
    reservationList = []
    waitingList = []
    reservationBook = ReservationBook(reservationList, waitingList)

    roomList = []
    directory = Directory(roomList)

    registry = Registry(directory, reservationBook)

    assert(type(registry.directory.roomList) is list)
    assert(type(registry.reservationBook.reservationList) is list)
    assert(type(registry.reservationBook.waitingList) is list)

def test_invalid_registry_init():
    reservationList = []
    waitingList = []
    reservationBook = ReservationBook(reservationList, waitingList)

    roomList = []
    directory = Directory(roomList)

    registry = Registry(directory, reservationBook)

    with pytest.raises(AttributeError) as e:
        registry.fakeAttributeDoesntExist
