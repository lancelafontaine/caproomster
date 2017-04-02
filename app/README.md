# REST API DOCUMENTATION

## General Information

Some resources require a user that is *logged in* in order to be accessed. They'll be marked with :warning: throughout this documentation.

If an unauthenticated user attempts to access one of these resources without being logged in, the response will be:

**401 - UNAUTHORIZED**
```
{
  "unauthorized": "Not logged in. You must login."
}
```

<hr/>

## Resource - `/login`

### `GET`

Checks if the current user is logged in or not.

#### Possible Responses

**200 - OK**
```
{
	"data": {
		"username": "iscapstone"
	},
	"login success": "Successfully logged in"
}
```

**401 - UNAUTHORIZED**
```
{
  "unauthorized": "Not logged in. You must login."
}
```


### `POST`

Login attempt. Returns a session token.

#### Expected Request Payload

John is a regular student.
```
{
	"username":"John",
	"password":"pass"
}
```

Other valid `username` are Emily (regular), Hans (capstone), Jackie (regular), Mary (capstone) and Rudy (regular)
All have `pass as the password.

#### Success Response

**200 - OK**
```
{
	"data": {
		"username": "John"
	},
	"login success": "Successfully logged in"
}
```

<hr/>

## Resource - `/logout`

### `GET`

Allows the current user to log out.

#### Success Response

**200 - OK**
```
{
  "logout success": "Successfully logged out."
}
```

<hr/>

## Resource  - `/rooms/all` - :warning:

### `GET`

Retrieves all CAPSTONE rooms in the system.


#### Success Response

**200 - OK**
```
{
	"rooms": [
		1,
		2,
		3,
		4,
		5
	]
}
```

<hr/>

## Resource - `reservations/create` - :warning:

### `POST`

Creates a new reservation for a specific timeslot, user an room.

#### Expected Request Payload

```
{
  "roomId":"2",
  "username":"John",
  "timeslot":{
    "startTime":"16",
    "endTime":"18",
    "date":"2017/04/02",
    "block":"2",
    "userId":"John",
    "timeId":"timeslotID_taimlkmlkm"
  },
  "description":"John 2 meeting",
  "equipment":{
    "laptop":"0",
    "projector":"0",
    "board":"0"
  }
}
```

Be careful, as there is some inconsistency for the time being between the username and userId...

#### Success Response

```
{
	"makeNewReservation": "successfully created the reservation",
	"reservationId": "94b12553-4fd1-4097-b1ec-0b9050ad45d3"
}
```

## Resource - `reservations/user/:userId`

### `GET`

Gets all the reservations of a specific user

#### Success Response

```
{
	"reservations": [
		{
			"description": "cool meeting",
			"reservationId": "94b12553-4fd1-4097-b1ec-0b9050ad45d3",
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "Thu, 19 Mar 2020 00:00:00 GMT",
				"endTime": 5,
				"startTime": 4,
				"timeId": "9470839d-8fbf-4d19-ae51-101b2616c780"
			},
			"user": {
				"username": "iscapstone"
			}
		}
	],
	"username": "iscapstone",
	"waitings": []
}
```

## Resource - `reservations/room/:roomId`

### `GET`

Gets all the reservations within a particular room.

#### Success Response

```
{
	"reservations": [
		{
			"description": "cool meeting",
			"reservationId": "94b12553-4fd1-4097-b1ec-0b9050ad45d3",
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "Thu, 19 Mar 2020 00:00:00 GMT",
				"endTime": 5,
				"startTime": 4,
				"timeId": "9470839d-8fbf-4d19-ae51-101b2616c780"
			},
			"user": {
				"username": "iscapstone"
			}
		}
	],
	"roomId": "1",
	"waitings": []
}
```

## Resource - `reservations/all`

### `GET`

Gets all the reservations in the system

#### Success Response

```
{
	"reservations": [
		{
			"description": "cool meeting",
			"reservationId": "94b12553-4fd1-4097-b1ec-0b9050ad45d3",
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "Thu, 19 Mar 2020 00:00:00 GMT",
				"endTime": 5,
				"startTime": 4,
				"timeId": "9470839d-8fbf-4d19-ae51-101b2616c780"
			},
			"user": {
				"username": "iscapstone"
			}
		}
	],
	"waitings": []
}
```

## Resource - `reservations/:reservationId`

### `DELETE`

Deletes a reservation based on the specified ID. Returns 404 if no reservation is found with that ID.

#### Success Response
```
{
	"reservationId": "b29615b7-2895-4929-955a-ea0491e283de",
	"success": "reservation successfully deleted"
}
```



