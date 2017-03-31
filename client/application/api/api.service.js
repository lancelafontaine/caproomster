(function(angular) {

  'use strict';

  angular.module('caproomster.api').service('caproomster.api.ApiService', ApiService);

  ApiService.$inject = ['caproomster.api.ApiFactory'];

  function ApiService(ApiFactory) {

    var svc = this;
    svc.account = account;
    svc.booking = booking;

    function account(action, payload) {
      if (action === 'login') {
        return ApiFactory.login().login({}, payload).$promise;
      }
      if (action === 'checkLogin') {
        return ApiFactory.login().check({}).$promise;
      }
      if (action === 'logout') {
        return ApiFactory.logout().logout({}).$promise;
      }
      return undefined;
    }

    function booking(action, payload) {
      if (action === 'getRoomList') {
        return ApiFactory.getRoomList().get({}).$promise;
      }
      if (action === 'reserve') {
        return ApiFactory.reserveSlot().reserve({}, payload).$promise;
      }
      if (action === 'getAllReservation') {
        return ApiFactory.getAllReservation().get(payload).$promise;
      }
      return undefined;
    }

  }
})(angular);
