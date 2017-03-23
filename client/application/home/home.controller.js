(function(angular){

  'use strict';

  angular.module('caproomster').controller('caproomster.home.HomeController', HomeController);

  HomeController.$inject = ['$scope', 'moment', 'calendarConfig', 'caproomster.api.ApiService'];

  function HomeController($scope, moment, calendarConfig, ApiService) {

    // Init controller and variables
    init();
    $scope.toggleMenu = toggleMenu;
    $scope.changeRoom = changeRoom;
    $scope.addEvent = addEvent;
    $scope.eventClicked = eventClicked;
    $scope.eventEdited = eventEdited;
    $scope.eventDeleted = eventDeleted;
    $scope.eventTimesChanged = eventTimesChanged;
    $scope.timespanClicked = timespanClicked;

    // Init function

    function init() {
      $scope.calendarView = 'week';
      $scope.viewDate = new Date();
      $scope.toggleText = 'Show Room List';
      $scope.roomNumber = 'H921';
      $scope.cellIsOpen = true;
      $scope.events = [];
      checkLogin();
    }

    // Check login

    function checkLogin() {
      ApiService.account('checkLogin').then(function() {
        fetchEvents();
      }, function() {
        $state.go('login');
      });
    }

    // Toggle Menu

    function toggleMenu() {
      if (!$scope.isToggled) {
        $scope.isToggled = true;
        $scope.toggleText = 'Hide Room List';
      } else {
        $scope.isToggled = false;
        $scope.toggleText = 'Show Room List';
      }
    }

    // Change room number and fetch room data

    function changeRoom(room) {
      $scope.roomNumber = room;
      // TODO: change view, get data etc.
    }

    // Fetch reservations from backend

    function fetchEvents() {
      // TODO: integrate rest api and fecth real date, for now just mocking
      var actions = [{
        label: '<i class=\'glyphicon glyphicon-pencil\'></i>',
        onClick: function(args) {
          console.log('Edited');
        }
      }, {
        label: '<i class=\'glyphicon glyphicon-remove\'></i>',
        onClick: function(args) {
          console.log('Deleted');
        }
      }];
      // mock data
      $scope.events = [
        {
          title: 'Bruce - Reservation',
          color: calendarConfig.colorTypes.info,
          startsAt: moment().startOf('day').add(10, 'hours').toDate(),
          endsAt: moment().startOf('day').add(11, 'hours').toDate(),
          draggable: true,
          actions: actions
        }, {
          title: 'Bruce - Reservation',
          color: calendarConfig.colorTypes.info,
          startsAt: moment().startOf('day').add(11, 'hours').toDate(),
          endsAt: moment().startOf('day').add(12, 'hours').toDate(),
          draggable: true,
          actions: actions
        }, {
          title: 'Lance - Waiting',
          color: calendarConfig.colorTypes.important,
          startsAt: moment().startOf('day').add(11, 'hours').toDate(),
          endsAt: moment().startOf('day').add(12, 'hours').toDate(),
          draggable: true,
          actions: actions
        }, {
          title: 'Arek - Reservation',
          color: calendarConfig.colorTypes.info,
          startsAt: moment().startOf('day').subtract(2, 'days').add(14, 'hours').toDate(),
          endsAt: moment().startOf('day').subtract(2, 'days').add(15, 'hours').toDate(),
          draggable: true,
          actions: actions
        }, {
          title: 'Adrianna - Waiting',
          color: calendarConfig.colorTypes.important,
          startsAt: moment().startOf('day').subtract(2, 'days').add(14, 'hours').toDate(),
          endsAt: moment().startOf('day').subtract(2, 'days').add(15, 'hours').toDate(),
          draggable: true,
          actions: actions
        }
      ];
    }

    // add a reservation to calendar view

    function addEvent() {
      // TODO: mocking for now
      $scope.events.push({
        title: 'New event',
        startsAt: moment().startOf('day').toDate(),
        endsAt: moment().endOf('day').toDate(),
        color: calendarConfig.colorTypes.important,
        draggable: true,
        resizable: true
      });
    }

    function timespanClicked(date, cell) {
      if ($scope.calendarView === 'month') {
        if (($scope.cellIsOpen && moment(date).startOf('day').isSame(moment($scope.viewDate).startOf('day'))) || cell.events.length === 0 || !cell.inMonth) {
          $scope.cellIsOpen = false;
        } else {
          $scope.cellIsOpen = true;
          $scope.viewDate = date;
        }
      } else if ($scope.calendarView === 'year') {
        if (($scope.cellIsOpen && moment(date).startOf('month').isSame(moment($scope.viewDate).startOf('month'))) || cell.events.length === 0) {
          $scope.cellIsOpen = false;
        } else {
          $scope.cellIsOpen = true;
          $scope.viewDate = date;
        }
      }
    }

    function eventClicked() {
      //TODO
      console.log('Clicked');
    }

    function eventEdited() {
      //TODO
      console.log('Edited');
    }

    function eventDeleted() {
      //TODO
      console.log('Deleted');
    }

    function eventTimesChanged() {
      //TODO
      console.log('Dropped or resized');
    }

  }

})(angular);
