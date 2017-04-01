import pytest
from app.core.equipment import Equipment

def test_equipment_with_no_arguments_is_zero_length():
	equipment = Equipment()
	assert 0 == len(equipment)

def test_equipment_getting_number_of_equipment_needed():
	equipment7 = Equipment(laptops=2,projectors=1,whiteboards=4)
	assert 7 == len(equipment7)

	equipment1 = Equipment(0,1,0)
	assert 1 == len(equipment1)

	equipment4 = Equipment(1,2,1)
	assert 4 == len(equipment4)


