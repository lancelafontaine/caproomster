(function(angular) {

  'use strict';

  angular.module('caproomster.login').component('loginComponent', {
    controller: 'caproomster.login.LoginController',
    controllerAs: 'vm',
    templateUrl: 'login/login.template.html'
  });

})(angular);
