import UnitOfWork

from app.TDG import EquipmentTDG
from app.core.equipment import Equipment


def makeNew(laptops, projectors, whiteboards, equipmentId):
    equipment = Equipment(equipmentId,laptops=laptops, projectors=projectors, whiteboards=whiteboards)
    UnitOfWork.registerNew(equipment)
    return equipment


def find(equipmentId):
    result = EquipmentTDG.find(equipmentId)
    if not result:
        return
    else:
        return Equipment(result[0][0], result[0][1], result[0][2],result[0][3])

def set(equipmentId):
    equipment = find(equipmentId)
    UnitOfWork.registerDirty(equipment)


def done():
    UnitOfWork.commit()


# remove timeslot instance from unit of work
def delete(equipmentId):
    UnitOfWork.registerDeleted(Equipment(equipmentId, 0, 0, 0))


def save(equipment):
    EquipmentTDG.insert(equipment.getId(),equipment.equipment['laptops'],equipment.equipment['projectors'],equipment.equipment['whitboards'])


# remove waiting instance from database

def erase(timeslotId):
    TimeslotTDG.delete(timeslotId)
