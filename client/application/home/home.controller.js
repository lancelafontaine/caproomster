(function(angular){

  'use strict';

  angular.module('caproomster').controller('caproomster.home.HomeController', HomeController);

  HomeController.$inject = [
    '$state',
    'moment',
    'calendarConfig',
    'caproomster.api.ApiService',
    'caproomster.home.HomeService'];

  function HomeController($state, moment, calendarConfig, ApiService, HomeService) {

    var vm = this;
    var currentUser = null;
    vm.$onInit = init;

    // Init function

    function init() {
      vm.toggleMenu = toggleMenu;
      vm.changeRoom = changeRoom;
      vm.makeReservation = makeReservation;
      vm.dateToNumber = HomeService.dateToNumber;
      vm.calendarView = 'week';
      vm.viewDate = new Date();
      vm.toggleText = 'Show Room List';
      vm.message = 'Select a timeslot to start reservation';
      vm.roomList = [];
      vm.roomNumber = '';
      vm.cellIsOpen = true;
      vm.events = [];
      vm.myReservations = [];
      vm.myWaitingList = [];
      vm.newReservationCache = {
        equipment: {
          laptop: 0,
          projector: 0,
          board: 0
        },
        length: 1,
        start: undefined,
        date: undefined
      };
      vm.inAction = null;
      initData();
    }

    // check login and init all data for the view

    function initData() {
      ApiService.account('checkLogin').then(function(loggedInUser) {
        currentUser = loggedInUser.success.username;
        vm.authenticated = true;
        ApiService.booking('getRoomList').then(function(roomList) {
          vm.roomList = roomList.rooms;
          vm.roomNumber = vm.roomList[0];
          getRoomInfo();
          getMyInfo();
        });
      }, function() {
        $state.go('login');
      });
    }

    // get ROOM reservations and waitings

    function getRoomInfo() {
      vm.events = [];
      ApiService.booking('getAllReservation', {
        roomId: vm.roomNumber
      }).then(function(res){
        var reservations = res.reservations || [];
        var waitingList = res.waitingList || [];
        for (var i = 0; i < reservations.length; i++) {
          vm.events.push(HomeService.createEvent(reservations[i], calendarConfig.colorTypes.info));
        }
        for (var j = 0; j < waitingList.length; j++) {
          vm.events.push(HomeService.createEvent(reservations[i], calendarConfig.colorTypes.warning));
        }
      });
    }

    // get USER reservations and waitings

    function getMyInfo() {
      ApiService.booking('getMyReservation', {
        userId: currentUser
      }).then(function(myReservations) {
        vm.myReservations = myReservations.reservations;
        vm.myWaitingList = myReservations.waitings;
      });
    }

    // Make one reservation

    function makeReservation() {
      var payload = {
        roomId: vm.roomNumber,
        username: currentUser,
        timeslot: {
          startTime: vm.newReservationCache.start,
          endTime: parseInt(vm.newReservationCache.start) + parseInt(vm.newReservationCache.length),
          date: vm.newReservationCache.date
        },
        equipment: vm.newReservationCache.equipment,
        description: currentUser + '\'s Reservation'
      };
      console.log(payload);
      ApiService.booking('reserve', payload).then(function() {
        showMessage('Successfully reserved.');
        vm.inAction = null;
        getRoomInfo();
        getMyInfo();
      }, function() {
        showMessage('Fail to reserve, please try again.');
        vm.inAction = null;
      });
    }

    /*
    Helper Functions
    */

    function showMessage(msg) {
      vm.message = msg;
      vm.newReservationCache = {
        equipment: {
          laptop: 0,
          projector: 0,
          board: 0
        },
        length: 1,
        start: undefined,
        date: undefined
      };
      setTimeout(function(){
        vm.message = 'Select a timeslot to start reservation!';
      }, 600);
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
