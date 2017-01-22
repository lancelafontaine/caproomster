--COMP 343
--BookMe
--PostgreSql compatible
-- -----------------------------------------------------||||

-- Drop all tables before running scripts
DROP TABLE IF EXISTS reservationTable cascade;
DROP TABLE IF EXISTS waitingTable cascade;
DROP TABLE IF EXISTS userTable cascade;
DROP TABLE IF EXISTS roomTable cascade;
DROP TABLE IF EXISTS timeslotTable cascade;

-- /////////////////////////////////////////////////////////

-- ---------------------------------
-- Table: user
-- Desc: represents users of the system
-- ---------------------------------

CREATE TABLE IF NOT EXISTS userTable (
	userId SERIAL NOT NULL,
	name VARCHAR(30)  NOT NULL DEFAULT ' ',
	password VARCHAR(30) NOT NULL,
	PRIMARY KEY (userId)
);


-- ---------------------------------
-- Table: room
-- Desc: represents rooms that can be reserved
-- Note: lock :: determine if room can be accessed
-- ---------------------------------

CREATE TABLE IF NOT EXISTS roomTable (
	roomId SERIAL NOT NULL,
	roomLock BOOLEAN NOT NULL DEFAULT FALSE,
	PRIMARY KEY (roomId)
);


-- ---------------------------------
-- Table: timeslot
-- Desc: represents a timeslot for a reservation
-- ---------------------------------

CREATE TABLE IF NOT EXISTS timeslotTable (
	timeId SERIAL NOT NULL,
	startTime integer NOT NULL,
	endTime integer NOT NULL,
	date DATE NOT NULL,
	block integer NOT NULL,
	userId integer NOT NULL,
	FOREIGN KEY (userId) REFERENCES userTable (userId),
	PRIMARY KEY (timeId)
);


-- ---------------------------------
-- Table: waiting
-- Desc: captures a reservation that is on a waiting list
-- ---------------------------------

CREATE TABLE IF NOT EXISTS waitingTable (
	waitingId SERIAL NOT NULL,
	room integer,
	reservee integer,
	description VARCHAR(100),
	timeslot integer,
	PRIMARY KEY (waitingId),
	FOREIGN KEY (room) REFERENCES roomTable (roomId),
	FOREIGN KEY (reservee) REFERENCES userTable (userId),
	FOREIGN KEY (timeslot) REFERENCES timeslotTable (timeId)
);


-- ---------------------------------
-- Table: reservation
-- Desc: represents reservations made by users
-- ---------------------------------

CREATE TABLE IF NOT EXISTS reservationTable (
	reservationId SERIAL NOT NULL,
	room integer,
	description VARCHAR(100),
	holder integer,
	timeslot integer,
	PRIMARY KEY (reservationId),
	FOREIGN KEY (room) REFERENCES roomTable (roomId),
	FOREIGN KEY (holder) REFERENCES userTable (userId),
	FOREIGN KEY (timeslot) REFERENCES timeslotTable (timeId)
);


-- ///////////// INSERT STATMENTS //////////////////////

INSERT INTO userTable(password, name) VALUES
	('pass','John'),
	('pass','Emily'),
	('pass','Rudy'),
	('pass','Jackie');


INSERT INTO roomTable(roomId) VALUES
	(1),
	(2),
	(3),
	(4),
	(5);

