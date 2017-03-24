(function(angular) {

  'use strict';

  angular.module('caproomster.home').component('homeComponent', {
    controller: 'caproomster.home.HomeController',
    controllerAs: 'vm',
    templateUrl: 'home.template.html'
  });

})(angular);
