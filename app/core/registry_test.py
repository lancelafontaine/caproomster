from app.core.registry import Registry
from app.core.reservationbook import ReservationBook
import pytest


def test_valid_registry_init():
    reservationList = []
    waitingList = []
    reservationBook = ReservationBook(reservationList, waitingList)

    registry = Registry(reservationBook)

    assert(type(registry.reservationBook.reservationList) is list)
    assert(type(registry.reservationBook.waitingList) is list)

def test_invalid_registry_init():
    reservationList = []
    waitingList = []
    reservationBook = ReservationBook(reservationList, waitingList)

    registry = Registry(reservationBook)

    with pytest.raises(AttributeError) as e:
        registry.fakeAttributeDoesntExist

