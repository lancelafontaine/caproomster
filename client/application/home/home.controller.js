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
      vm.eventClicked = eventClicked;
      vm.eventEdited = eventEdited;
      vm.eventDeleted = eventDeleted;
      vm.eventTimesChanged = eventTimesChanged;
      vm.timespanClicked = timespanClicked;
      vm.makeReservation = makeReservation;
      vm.calendarView = 'week';
      vm.viewDate = new Date();
      vm.toggleText = 'Show Room List';
      vm.roomList = [];
      vm.roomNumber = '';
      vm.cellIsOpen = true;
      vm.events = [];
      vm.myReservations = [];
      initData();
    }

    // check login and init all data for the view

    function initData() {
      ApiService.account('checkLogin').then(function(loggedInUser) {
        vm.authenticated = true;
        ApiService.booking('getRoomList').then(function(roomList) {
          vm.roomList = roomList.rooms;
          vm.roomNumber = vm.roomList[0];
          getRoomInfo();
        });
        ApiService.booking('getMyReservation', {
          userId: loggedInUser.success.username
        }).then(function(myReservations) {
          vm.myReservations = myReservations.reservations;
        });
      }, function() {
        $state.go('login');
      });
    }

    // parse return data into calendar event object

    function createEvent(reservation, type) {
      var dateString = reservation.timeslot.date.replace('GMT', 'EST');
      var start = new Date(dateString);
      start.setHours(reservation.timeslot.startTime);
      var end = new Date(dateString);
      end.setHours(reservation.timeslot.endTime);
      var event = {};
      event.title = reservation.description;
      event.startsAt = start;
      event.endsAt = end;
      event.color = type;
      return event;
    }

    // get reservation, waitingList, and equipment of a room

    function getRoomInfo() {
      vm.events = [];
      console.log(2312312)
      ApiService.booking('getAllReservation', {
        roomId: vm.roomNumber
      }).then(function(res){
        var reservations = res.reservations;
        for (var i = 0; i < reservations.length; i++) {
          vm.events.push(createEvent(reservations[i], calendarConfig.colorTypes.info));
        }
      });
      // TODO: get equipment list
    }

    /*
    UI Actions
    */

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

    function makeReservation(calendarRangeStartDate, calendarRangeEndDate) {
      console.log(calendarRangeStartDate);
      console.log(calendarRangeEndDate);
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

    // change room and fetch room data

    function changeRoom(room) {
      vm.roomNumber = room;
      getRoomInfo();
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

  }

})(angular);
