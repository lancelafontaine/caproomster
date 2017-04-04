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
      createReservation: createReservation,
      modifyReservation: modifyReservation,
      getAllReservation: getAllReservation,
      getMyReservation: getMyReservation,
      deleteMyReservation: deleteMyReservation
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

    function createReservation() {
      var url = '/reservations/repeat/:repeat';
      return $resource(baseUrl + url, {
        repeat: '@repeat'
      }, {
        reserve: {
          method: 'POST',
          withCredentials: true
        }
      });
    }

    /* modifyReservation factory */

    function modifyReservation() {
      var url = '/reservations/modify/:reservationId';
      return $resource(baseUrl + url, {
        reservationId: '@reservationId'
      }, {
        modify: {
          method: 'PUT',
          withCredentials: true
        }
      });
    }

    /* getAllReservation factory */

    function getAllReservation() {
      var url = '/reservations/room/:roomId';
      return $resource(baseUrl + url, {
        roomId: '@roomId'
      }, {
        get: {
          method: 'GET',
          withCredentials: true
        }
      });
    }

    /* getMyReservation factory */

    function getMyReservation() {
      var url = '/reservations/user/:userId';
      return $resource(baseUrl + url, {
        userId: '@userId'
      }, {
        get: {
          method: 'GET',
          withCredentials: true
        }
      });
    }

    /* deleteReservation factory */

    function deleteMyReservation() {
      var url = '/reservations/:reservationId';
      return $resource(baseUrl + url, {
        reservationId: '@reservationId'
      }, {
        delete: {
          method: 'DELETE',
          withCredentials: true
        }
      });
    }

  }

})(angular);
