--BookMe
--PostgreSql compatible
-- -----------------------------------------------------||||

-- Drop all tables before running scripts
DROP TABLE IF EXISTS reservationTable cascade;
DROP TABLE IF EXISTS waitingTable cascade;
DROP TABLE IF EXISTS userTable cascade;
DROP TABLE IF EXISTS roomTable cascade;
DROP TABLE IF EXISTS timeslotTable cascade;
DROP TABLE IF EXISTS equipmentTable cascade;

-- /////////////////////////////////////////////////////////

-- ---------------------------------
-- Table: user
-- Desc: represents users of the system
-- ---------------------------------

CREATE TABLE IF NOT EXISTS userTable (
	username VARCHAR(30) NOT NULL,
	password VARCHAR(30) NOT NULL,
  capstone BOOLEAN NOT NULL,
	PRIMARY KEY (username)
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
	timeId VARCHAR(128) NOT NULL,
	startTime integer NOT NULL,
	endTime integer NOT NULL,
	date DATE NOT NULL,
	block integer NOT NULL,
	username VARCHAR(30) NOT NULL,
	FOREIGN KEY (username) REFERENCES userTable (username),
	PRIMARY KEY (timeId)
);

-- ---------------------------------
-- Table: equipment
-- Desc: represents equipment for a reservation
-- ---------------------------------

CREATE TABLE IF NOT EXISTS equipmentTable (
	equipmentId VARCHAR(128) NOT NULL,
	laptops integer DEFAULT 0,
	projectors integer DEFAULT 0,
	whiteboards integer DEFAULT 0,
	PRIMARY KEY (equipmentId)
);

-- ---------------------------------
-- Table: waiting
-- Desc: captures a reservation that is on a waiting list
-- ---------------------------------

CREATE TABLE IF NOT EXISTS waitingTable (
	waitingId VARCHAR(128) NOT NULL,
	room integer,
	reservee VARCHAR(30),
	description VARCHAR(100),
	timeslot VARCHAR(128),
	equipment VARCHAR(128),
	PRIMARY KEY (waitingId),
	FOREIGN KEY (room) REFERENCES roomTable (roomId),
	FOREIGN KEY (reservee) REFERENCES userTable (username),
	FOREIGN KEY (timeslot) REFERENCES timeslotTable (timeId),
	FOREIGN KEY (equipment) REFERENCES equipmentTable (equipmentId)
);


-- ---------------------------------
-- Table: reservation
-- Desc: represents reservations made by users
-- ---------------------------------

CREATE TABLE IF NOT EXISTS reservationTable (
	reservationId VARCHAR(128) NOT NULL,
	room integer,
	description VARCHAR(100),
	holder VARCHAR(30),
	timeslot VARCHAR(128),
	equipment VARCHAR(128),
	PRIMARY KEY (reservationId),
	FOREIGN KEY (room) REFERENCES roomTable (roomId),
	FOREIGN KEY (holder) REFERENCES userTable (username),
	FOREIGN KEY (timeslot) REFERENCES timeslotTable (timeId),
	FOREIGN KEY (equipment) REFERENCES equipmentTable (equipmentId)
);


-- ///////////// INSERT STATMENTS //////////////////////

INSERT INTO userTable(username, password, capstone) VALUES
        ('iscapstone','soen344', TRUE),
        ('nocapstone','soen344', FALSE),
        ('1','pass', FALSE),
        ('2','pass', TRUE);

INSERT INTO roomTable(roomId) VALUES (1), (2), (3), (4), (5);

