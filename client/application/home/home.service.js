(function(angular) {

  'use strict';

  angular.module('caproomster.home').service('caproomster.home.HomeService', HomeService);

  HomeService.$inject = [];

  function HomeService() {

    var svc = this;
    svc.createEvent = createEvent;
    svc.dateToNumber = dateToNumber;

    function createEvent(reservation, type) {
      var date = reservation.timeslot.date;
      var startTime = new Date(date);
      startTime.setHours(reservation.timeslot.startTime);
      var endTime = new Date(date);
      endTime.setHours(reservation.timeslot.endTime);
      return {
        title: reservation.description,
        startsAt: startTime,
        endsAt: endTime,
        color: type
      };
    }

    function dateToNumber(dateObj) {
      var year = dateObj.getFullYear();
      var month = dateObj.getMonth() + 1;
      var date = dateObj.getDate();
      if (month < 10) {
        month = '0' + month;
      }
      if (date < 10) {
        date = '0' + date;
      }
      return year + '/' + month + '/' + date;
    }


  }
})(angular);
