# REST API DOCUMENTATION

## General Information

Some resources require a user that is *logged in* in order to be accessed. They'll be marked with :warning: throughout this documentation.

If an unauthenticated user attempts to access one of these resources without being logged in, the response will be:

**401 - UNAUTHORIZED**
```json
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
```json
{
  "success": {
    "userId": 1
  }
}
```

**401 - UNAUTHORIZED**
```json
{
  "unauthorized": "Not logged in. You must login."
}
```


### `POST`

Login attempt. Returns a session token.

#### Expected Request Payload
```json
{
  "userId":"1",
  "password": "pass"
}
```

#### Success Response

**200 - OK**
```json
{
  "data": {
    "userId": "1",
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
```json
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
```json
{
  "logout success": "Successfully logged out."
}
```

<hr/>

## Resource - `reservations/create` - :warning:

### `POST`

Creates a new reservation for a specific timeslot, user an room.

#### Expected Request Payload

```json
{
  	"roomId":"1",
  	"userId": "1",
	"timeslot":  {
		"startTime": "16",
		"endTime": "17",
		"date": "2020-03-19"
	},
  	"description": "cool meeting"
}
```

#### Success Response

```json
{
  "makeNewReservation": "successfully created the reservation",
  "reservationId": 221513
}
```

## Resource - `reservations/user/:userId`

### `GET`

Gets all the reservations of a specific user

#### Success Response

```json
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

## Resource - `reservation/room/:roomId`

### `GET`

Gets all the reservations within a particular room.

#### Success Response

```json
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

```json
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





