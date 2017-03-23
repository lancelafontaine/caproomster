(function(angular) {

  'use strict';

  angular.module('caproomster.api').service('caproomster.api.ApiService', ApiService);

  ApiService.$inject = ['caproomster.api.ApiFactory'];

  function ApiService(ApiFactory) {

    var svc = this;
    svc.account = account;

    function account(action, payload) {
      if (action === '') {
        return ApiFactory.a().post({}, payload).$promise;
      }
      return undefined;
    }

  }
})(angular);
