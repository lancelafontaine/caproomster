(function(angular) {

  'use strict';

  angular.module('caproomster.api').factory('caproomster.api.ApiFactory', ApiFactory);

  ApiFactory.$inject = ['$resource', 'caproomster.AppConstant'];

  function ApiFactory($resource, AppConstant) {

    var baseUrl = AppConstant.server_base_url;

    return {
      login: login,
      logout: logout,
      getRoomList: getRoomList,
      reserveSlot: reserveSlot,
      getAllReservation: getAllReservation
    };

    /* login factory */

    function login() {
      var url = '/login';
      return $resource(baseUrl + url, {}, {
        login: {
          method: 'POST',
          withCredentials: true
        },
        check: {
          method: 'GET',
          withCredentials: true
        }
      });
    }

    /* logout factory */

    function logout() {
      var url = '/logout';
      return $resource(baseUrl + url, {}, {
        logout: {
          method: 'GET',
          withCredentials: true
        }
      });
    }

    /* getRoom factory */

    function getRoomList() {
      var url = '/rooms/all';
      return $resource(baseUrl + url, {}, {
        get: {
          method: 'GET',
          withCredentials: true
        }
      });
    }

    /* creaeReservation factory */

    function reserveSlot() {
      var url = '/reservations/create';
      return $resource(baseUrl + url, {}, {
        reserve: {
          method: 'POST',
          withCredentials: true
        }
      });
    }

    /* getAllReservation factory */

    function getAllReservation() {
      var url = '/reservations/all';
      return $resource(baseUrl + url, {}, {
        get: {
          method: 'GET',
          withCredentials: true
        }
      });
    }

  }

})(angular);
