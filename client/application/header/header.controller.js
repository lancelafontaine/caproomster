(function(angular) {

  'use strict';

  angular.module('caproomster.header').controller('caproomster.header.HeaderController', HeaderController);
  HeaderController.$inject = ['$state', 'caproomster.api.ApiService'];

  function HeaderController($state, ApiService) {

    var vm = this;
    vm.$onInit = init;

    function init() {
      vm.logout = logout;
    }

    function logout() {
      ApiService.account('logout').then(function() {
        $state.go('login');
      });
    }

  }

})(angular);
