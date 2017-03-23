(function(angular) {

  'use strict';

  angular.module('caproomster.api').factory('caproomster.api.ApiFactory', ApiFactory);

  ApiFactory.$inject = ['$resource', 'caproomster.AppConstant'];

  function ApiFactory($resource, AppConstant) {

    var baseUrl = AppConstant.server_base_url;

    return {
      a: a,
      b: b
    };

        // Register

        // Update

    function a() {
      var url = '/a';
      return $resource(baseUrl + url, {}, {
        post: {
          method: 'POST',
          withCredentials: true
        }
      });
    }

        // get user skill profile

    function b() {
      var url = '/b';
      return $resource(baseUrl + url, {
        email: '@email'
      }, {
        get: {
          method: 'GET'
        }
      });
    }

  }

})(angular);
