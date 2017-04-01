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
```
{
	"username":"iscapstone",
	"password":"soen344"
}
```

#### Success Response

**200 - OK**
```
{
	"data": {
		"username": "iscapstone"
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
	"rooms": [
		1,
		2,
		3,
		4,
		5
	]
}
```

#### Success Response

```
{
  "makeNewReservation": "successfully created the reservation",
  "reservationId": 221513
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
			"reservationId": 1,
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "Thu, 19 Mar 2020 00:00:00 GMT",
				"endTime": 15,
				"startTime": 14,
				"timeId": 1
			},
			"user": {
				"userId": 1,
				"username": "John"
			}
		}
	],
	"userId": "1"
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
			"reservationId": 1,
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "Thu, 19 Mar 2020 00:00:00 GMT",
				"endTime": 15,
				"startTime": 14,
				"timeId": 1
			},
			"user": {
				"userId": 1,
				"username": "John"
			}
		}
	],
	"roomId": "1"
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
			"reservationId": 1,
			"room": {
				"roomId": 1
			},
			"timeslot": {
				"date": "Thu, 19 Mar 2020 00:00:00 GMT",
				"endTime": 15,
				"startTime": 14,
				"timeId": 1
			},
			"user": {
				"userId": 1,
				"username": "John"
			}
		}
	]
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



