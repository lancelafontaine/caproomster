import pytest

from app.core.user import  User


def test_change_capstone_status(monkeypatch):
	#Initialization
	user1 = User("arek","secretArekPassword")
	user2 = User("bruce","secretBrucePassword",False)
	user3 = User("cc","secretCCPassword",True)

	#By default, users are not capstone students,
	# so making sure this is correctly enforced
	assert user1.isCapstone() == False
	assert user2.isCapstone() == False
	assert user3.isCapstone() == True

	#Forcing capstone attribute to False
	user1.setCapstone(False)
	user2.setCapstone(False)
	user3.setCapstone(False)

	#Student should now be a regular student
	assert user1.isCapstone() == False
	assert user2.isCapstone() == False
	assert user3.isCapstone() == False

	#Granting student capstone status
	user1.setCapstone(True)
	user2.setCapstone(True)

	#By default, this method can
	# be called with no arguments...
	user3.setCapstone()

	#Checking user3
	assert user3.isCapstone() == True

	#Student now is a capstone student
	assert user1.isCapstone() == True

	#Taking off capstone status, returning to regular student status
	user1.setCapstone(False)

	#Making sure student is really a regular student
	assert user1.isCapstone() == False

def test_setting_password(monkeypatch):
	#Initialization
	user = User("taimoor","secretTaimoorPassword")

	#The password is not really secret
	assert user.getPassword() == "secretTaimoorPassword"

	#Checking for comparison between different passwords
	assert not user.getPassword() == "someOtherString"

	#Checking that internally automagically the
	# string case is not being ignored...
	assert not user.getPassword() == "secrettaimoorpassword"
