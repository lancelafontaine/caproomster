(function(angular) {

  'use strict';

  angular.module('caproomster.api').service('caproomster.restApi.ApiService', ApiService);

  ApiService.$inject = ['caproomster.api.ApiFactory'];

  function ApiService(ApiFactory) {

    var svc = this;
    svc.account = account;

    function account(action, payload) {
      if (action === 'login') {
        return ApiFactory.login().login({}, payload).$promise;
      }
      if (action === 'checkLogin') {
        return ApiFactory.login().check({}).$promise;
      }
      if (action === 'logout') {
        return ApiFactory.logout().check({}).$promise;
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
      return undefined;
    }

  }
})(angular);
