# CapRoomster

[![CircleCI](https://img.shields.io/circleci/project/github/lancelafontaine/caproomster.svg)](https://circleci.com/gh/lancelafontaine/caproomster) [![CodeCov](https://img.shields.io/codecov/c/github/lancelafontaine/caproomster.svg)](https://codecov.io/gh/lancelafontaine/caproomster)

This is a project done within the context of the SOEN 343 and SOEN 344 courses at Concordia University.

This repository was received from another team and ultimately refactored, maintained, and added to.

CapRoomster is a web application that allows Concordia students to reserve a CAPSTONE room for their projects.

# Documentation

TBD

# Installation and Development

## Client

See [client-side README](https://github.com/lancelafontaine/caproomster/tree/master/client) for further instructions.

## Server

### Installation
- Make sure you have Python 2.7 installed.
- Setup a [virtualenv](https://virtualenv.pypa.io/en/stable/) if you don't want to install packages globally on your system.
- `pip2 install -r requirements.txt`

### Development
- `python2 -B run.py`

### Running automated tests
- `pytest`

## Database
- Install `postgresql`.
  - If on Linux, more instructions [here](https://wiki.archlinux.org/index.php/PostgreSQL).
- Start your `postgresql` server.
- Create a database called `development`.
- Initialize the database with the `bookMeDB.sql` script.
- **IMPORTANT**: Before running the application, run `export postgres_password={your postgres password here}`

# Additional Information

## Login Credentials
- UserId: `1`, Username: `John`, Password: `pass`
- UserId: `2`, Username: `Emily`, Password: `pass`
- UserId: `3`, Username: `Rudy`, Password: `pass`
- UserId: `4`, Username: `Jackie`, Password: `pass`

## Assumptions and Constraints

TBD


# Team Members

## SOEN 344 Team Members
Zhipeng Cai - [choitwao](https://github.com/choitwao) <br/>
Adrianna Diaz - [adriannadiaz](https://github.com/adriannadiaz) <br/>
Lance Lafontaine - [lancelafontaine](https://github.com/lancelafontaine) <br/>
Arek Manoukian - [arekmano](https://github.com/arekmano) <br/>
Taimoor Rana - [Taimoorrana1](https://github.com/Taimoorrana1) <br/>
Lenz Petion - [MonsieurPetion](https://github.com/MonsieurPetion) <br/>


## SOEN 343 Team Members

Ahmad Hyjaz Loudin - @PuzzlePuzzling <br/>
Emir Bozer @emrbzr <br/>
Leo Yu @yleo <br/>
Nikolas De vigne Blanchet @ndvb <br/>
Mary Psaroudis @mary86
