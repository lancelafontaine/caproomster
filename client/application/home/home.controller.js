(function(angular){

  'use strict';

  angular.module('caproomster').controller('caproomster.home.HomeController', HomeController);

  HomeController.$inject = ['$state', 'moment', 'calendarConfig', 'caproomster.api.ApiService'];

  function HomeController($state, moment, calendarConfig, ApiService) {

    var vm = this;
    vm.$onInit = init;

    // Init function

    function init() {
      vm.toggleMenu = toggleMenu;
      vm.changeRoom = changeRoom;
      vm.addEvent = addEvent;
      vm.eventClicked = eventClicked;
      vm.eventEdited = eventEdited;
      vm.eventDeleted = eventDeleted;
      vm.eventTimesChanged = eventTimesChanged;
      vm.timespanClicked = timespanClicked;
      vm.calendarView = 'week';
      vm.viewDate = new Date();
      vm.toggleText = 'Show Room List';
      vm.roomList = [];
      vm.roomNumber = '';
      vm.cellIsOpen = true;
      vm.events = [];
      checkLogin();
    }

    // Check login

    function checkLogin() {
      ApiService.account('checkLogin').then(function() {
        vm.authenticated = true;
        fetchEvents();
        fetchRoomList();
      }, function() {
        $state.go('login');
      });
    }

    // Fetch room list

    function fetchRoomList() {
      ApiService.booking('getRoomList').then(function(res) {
        vm.roomList = res.rooms;
        vm.roomNumber = vm.roomList[0];
      });
    }

    // Toggle Menu

    function toggleMenu() {
      if (!vm.isToggled) {
        vm.isToggled = true;
        vm.toggleText = 'Hide Room List';
      } else {
        vm.isToggled = false;
        vm.toggleText = 'Show Room List';
      }
    }

    // Change room number and fetch room data

    function changeRoom(room) {
      vm.roomNumber = room;
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
      ApiService.booking('getAllReservation').then(function(res){
        console.log(res);
      });
      // mock data
      vm.events = [
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
      vm.events.push({
        title: 'New event',
        startsAt: moment().startOf('day').toDate(),
        endsAt: moment().endOf('day').toDate(),
        color: calendarConfig.colorTypes.important,
        draggable: true,
        resizable: true
      });
    }

    function timespanClicked(date, cell) {
      if (vm.calendarView === 'month') {
        if ((vm.cellIsOpen && moment(date).startOf('day').isSame(moment(vm.viewDate).startOf('day'))) || cell.events.length === 0 || !cell.inMonth) {
          vm.cellIsOpen = false;
        } else {
          vm.cellIsOpen = true;
          vm.viewDate = date;
        }
      } else if (vm.calendarView === 'year') {
        if ((vm.cellIsOpen && moment(date).startOf('month').isSame(moment(vm.viewDate).startOf('month'))) || cell.events.length === 0) {
          vm.cellIsOpen = false;
        } else {
          vm.cellIsOpen = true;
          vm.viewDate = date;
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
