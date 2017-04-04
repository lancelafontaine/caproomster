# REST API DOCUMENTATION

## General Information

Some resources require a user that is *logged in* in order to be accessed.

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
	"success": {
		"username": "iscapstone"
	}
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
All have `pass` as the password.

#### Success Response

**200 - OK**
```
{
	"data": {
		"capstone": "True",
		"username": "Mary"
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

Creates a new reservation for a specific timeslot, user and room.

If there is a time conflict, you will be put on the waitlist.

If there is not enough equipment for you reservation, you will be put on the waitlist.

If your are trying to reserve for more than 3 hours in a given week, this call with abort. No reservations or waiting lists will be created/altered.

#### Expected Request Payload

```
{
  	"roomId":"1",
  	"username": "Mary",
	"timeslot":  {
		"startTime": "7",
		"endTime": "8",
		"date": "2020/03/19"
	},
	"equipment":  {
		"laptop": 1,
		"projector": 1,
		"board": 1
	},
  	"description": "cool meeting"
}
```

#### Success Response

```
{
	"makeNewReservation": "successfully created reservation",
	"reservation": "83e51d8f-d1d7-4a9b-aa06-ae29db717c46"
}
```

## Resource - `reservations/repeat/:repeats`

### `POST`

Creates a new reservation for a specific timeslot, user and room, every week, for `repeats` weeks in the future.

`repeats` needs to be an integer between `0` and `2`.

If there is a time conflict, you will be put on the waitlist.

If there is not enough equipment for your reservation, you will be put on the waitlist.

If your are trying to reserve for more than 3 hours in a given week, this call with abort. Your previously registered reservations/waitings won't be reverted.

#### Expected Request Payload

```
{
  	"roomId":"1",
  	"username": "Mary",
	"timeslot":  {
		"startTime": "7",
		"endTime": "8",
		"date": "2020/03/19"
	},
	"equipment":  {
		"laptop": 1,
		"projector": 1,
		"board": 1
	},
  	"description": "cool meeting"
}
```

#### Success Response

```
{
{
	"reservations": [
		{
			"description": "cool meeting",
			"equipment": {
				"equipmentId": "eb14b4d7-799f-4550-b2b1-9b4a897e34eb",
				"laptops": 1,
				"projectors": "1",
				"whiteboards": 1
			},
			"reservationId": "f8d8b8eb-8da0-4f94-b31a-9cc062170ad6",
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "2020/03/19",
				"endTime": 8,
				"startTime": 7,
				"timeId": "96285b1a-311d-4769-95b5-b24719223d27",
				"userId": "Mary"
			},
			"user": {
				"isCapstone": true,
				"username": "Mary"
			}
		}
	],
	"success": "You have successfully repeated your reservations. Results are shown below.",
	"waitings": [
		{
			"description": "cool meeting",
			"equipment": {
				"equipmentId": "84248089-54d5-41eb-8255-d98ca6e01364",
				"laptops": 1,
				"projectors": "1",
				"whiteboards": 1
			},
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "2020/03/26",
				"endTime": 8,
				"startTime": 7,
				"timeId": "1ae98160-da92-451d-8e5d-554eb271c6ad",
				"userId": "Mary"
			},
			"user": {
				"isCapstone": true,
				"username": "Mary"
			},
			"waitingId": "62fc2ad1-2278-4e24-9a9f-cf32387dea3d"
		}
	]
}
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
			"equipment": {
				"equipmentId": "c98a52ea-a1f0-4452-b77b-a172e5de12ec",
				"laptops": 1,
				"projectors": "1",
				"whiteboards": 1
			},
			"reservationId": "83e51d8f-d1d7-4a9b-aa06-ae29db717c46",
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "2020/03/19",
				"endTime": 8,
				"startTime": 7,
				"timeId": "18fc4a23-83f8-4b13-a71b-862de4e003a2",
				"userId": "Mary"
			},
			"user": {
				"isCapstone": true,
				"username": "Mary"
			}
		}
	],
	"username": "Mary",
	"waitings": [
		{
			"description": "cool meeting",
			"equipment": {
				"equipmentId": "f51e1be0-8f32-409b-9030-85ab772a9e71",
				"laptops": 1,
				"projectors": "1",
				"whiteboards": 1
			},
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "2020/03/19",
				"endTime": 8,
				"startTime": 7,
				"timeId": "034df89d-e3b3-4dfb-b1b8-8341dfd3b8bd",
				"userId": "Mary"
			},
			"user": {
				"isCapstone": true,
				"username": "Mary"
			},
			"waitingId": "9091b42d-9f8b-464f-936f-16db3f01fa5e"
		}
	]
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
			"equipment": {
				"equipmentId": "c98a52ea-a1f0-4452-b77b-a172e5de12ec",
				"laptops": 1,
				"projectors": "1",
				"whiteboards": 1
			},
			"reservationId": "83e51d8f-d1d7-4a9b-aa06-ae29db717c46",
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "2020/03/19",
				"endTime": 8,
				"startTime": 7,
				"timeId": "18fc4a23-83f8-4b13-a71b-862de4e003a2",
				"userId": "Mary"
			},
			"user": {
				"isCapstone": true,
				"username": "Mary"
			}
		}
	],
	"roomId": "1",
	"waitings": [
		{
			"description": "cool meeting",
			"equipment": {
				"equipmentId": "f51e1be0-8f32-409b-9030-85ab772a9e71",
				"laptops": 1,
				"projectors": "1",
				"whiteboards": 1
			},
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "2020/03/19",
				"endTime": 8,
				"startTime": 7,
				"timeId": "034df89d-e3b3-4dfb-b1b8-8341dfd3b8bd",
				"userId": "Mary"
			},
			"user": {
				"isCapstone": true,
				"username": "Mary"
			},
			"waitingId": "9091b42d-9f8b-464f-936f-16db3f01fa5e"
		}
	]
}
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
			"equipment": {
				"equipmentId": "c98a52ea-a1f0-4452-b77b-a172e5de12ec",
				"laptops": 1,
				"projectors": "1",
				"whiteboards": 1
			},
			"reservationId": "83e51d8f-d1d7-4a9b-aa06-ae29db717c46",
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "2020/03/19",
				"endTime": 8,
				"startTime": 7,
				"timeId": "18fc4a23-83f8-4b13-a71b-862de4e003a2",
				"userId": "Mary"
			},
			"user": {
				"isCapstone": true,
				"username": "Mary"
			}
		}
	],
	"waitings": [
		{
			"description": "cool meeting",
			"equipment": {
				"equipmentId": "f51e1be0-8f32-409b-9030-85ab772a9e71",
				"laptops": 1,
				"projectors": "1",
				"whiteboards": 1
			},
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "2020/03/19",
				"endTime": 8,
				"startTime": 7,
				"timeId": "034df89d-e3b3-4dfb-b1b8-8341dfd3b8bd",
				"userId": "Mary"
			},
			"user": {
				"isCapstone": true,
				"username": "Mary"
			},
			"waitingId": "9091b42d-9f8b-464f-936f-16db3f01fa5e"
		}
	]
}
```

## Resource - `reservations/:reservationId`

### `DELETE`

Deletes a reservation or waiting based on the specified ID. Returns `404` if no reservation or waiting is found with that ID.

#### Success Response

##### If deleting a reservation
```
{
	"reservationId": "b29615b7-2895-4929-955a-ea0491e283de",
	"success": "reservation successfully deleted"
}
```

##### If deleting a waiting
```
{
	"success": "reservation on waiting list successfully deleted",
	"waitingId": "3b0c25cf-999e-4638-b27b-d372607cfe96"
}
```



