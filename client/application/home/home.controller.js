(function(angular){

  'use strict';

  angular.module('caproomster').controller('caproomster.home.HomeController', HomeController);

  HomeController.$inject = [
    '$state',
    'moment',
    'calendarConfig',
    '$interval',
    'caproomster.api.ApiService',
    'caproomster.home.HomeService'];

  function HomeController($state, moment, calendarConfig, $interval, ApiService, HomeService) {

    var vm = this;
    var currentUser = null;
    vm.$onInit = init;

    function init() {
      vm.toggleMenu = toggleMenu;
      vm.changeRoom = changeRoom;
      vm.makeReservation = makeReservation;
      vm.modifyReservation = modifyReservation;
      vm.deleteReservation = deleteReservation;
      vm.resetCache = resetCache;
      vm.setCache = setCache;
      vm.dateToNumber = HomeService.dateToNumber;
      vm.calendarView = 'week';
      vm.viewDate = new Date();
      vm.toggleText = 'Show Room List';
      vm.message = 'Select a start timeslot for the reservation.';
      vm.roomList = [];
      vm.roomNumber = '';
      vm.cellIsOpen = true;
      vm.events = [];
      vm.myReservations = [];
      vm.myWaitingList = [];
      vm.parseInt = parseInt;
      initData();
      //getRoomInfo();
      $interval(getRoomInfo, 1500);
    }

    function initData() {
      vm.resetCache();
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

    function getRoomInfo() {
      var tempEvents = [];
      ApiService.booking('getAllReservation', {
        roomId: vm.roomNumber
      }).then(function(res){
        var reservations = res.reservations || [];
        var waitingList = res.waitings || [];
        for (var resIndex = 0; resIndex < reservations.length; resIndex++) {
          tempEvents.push(HomeService.createEvent(reservations[resIndex], calendarConfig.colorTypes.info));
        }
        for (var wtIndex = 0; wtIndex < waitingList.length; wtIndex++) {
          tempEvents.push(HomeService.createEvent(waitingList[wtIndex], calendarConfig.colorTypes.warning));
        }
        vm.events = tempEvents;
      });
    }

    function getMyInfo() {
      ApiService.booking('getMyReservation', {
        userId: currentUser
      }).then(function(myReservations) {
        vm.myReservations = myReservations.reservations;
        vm.myWaitingList = myReservations.waitings;
      });
    }

    function makeReservation() {
      var param = {
        repeat: vm.cache.repeat
      };
      ApiService.booking('createReservation', createPayload(), param).then(function() {
        showMessage('Successfully reserved.');
        vm.resetCache();
        getMyInfo();
      }, function() {
        vm.resetCache();
        showMessage('Failed to reserve, please try again.');
      });
    }

    function modifyReservation() {
      var param = {
        reservationId: vm.cache.reservationId
      };
      ApiService.booking('modifyReservation', createPayload(), param).then(function() {
        showMessage('Successfully modified.');
        vm.resetCache();
        getMyInfo();
      }, function() {
        vm.resetCache();
        showMessage('Failed to modify, please try again.');
      });
    }

    function deleteReservation() {
      var payload = {
        reservationId: vm.cache.reservationId
      };
      ApiService.booking('deleteMyReservation', payload).then(function() {
        if (vm.cache.inAction == 'modify') {
          showMessage('Successfully modified.');
        } else {
          showMessage('Successfully deleted.');
        }
        vm.resetCache();
        getMyInfo();
      }, function() {
        vm.resetCache();
        showMessage('Failed to reserve, please try again.');
      });
    }

    function createPayload() {
      return {
        roomId: vm.roomNumber,
        username: currentUser,
        timeslot: {
          startTime: vm.cache.start,
          endTime: parseInt(vm.cache.start) + parseInt(vm.cache.length),
          date: vm.cache.date
        },
        equipment: vm.cache.equipment,
        description: currentUser + '\'s Reservation'
      };
    }

    function showMessage(msg) {
      vm.message = msg;
      setTimeout(function(){
        vm.message = 'Select a start timeslot for the reservation.';
      }, 600);
    }

    function resetCache() {
      vm.cache = {
        equipment: {
          laptop: 0,
          projector: 0,
          board: 0
        },
        length: 1,
        start: null,
        date: null,
        inAction: null,
        reservationId: null,
        repeat: 0
      };
    }

    function setCache(res, action) {
      vm.cache = {
        equipment: {
          laptop: res.equipment.laptops,
          projector: res.equipment.projectors,
          board: res.equipment.whiteboards
        },
        length: parseInt(res.timeslot.endTime) - parseInt(res.timeslot.startTime),
        start: parseInt(res.timeslot.startTime),
        date: res.timeslot.date,
        inAction: action,
        reservationId: res.reservationId || res.waitingId,
        repeat: 0
      };
    }

    function changeRoom(room) {
      vm.roomNumber = room;
      getRoomInfo();
    }

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
