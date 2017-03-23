(function(angular) {

  'use strict';

  angular.module('caproomster.header').component('headerComponent', {
    controller: 'caproomster.header.HeaderController',
    controllerAs: 'vm',
    templateUrl: 'header/header.template.html'
  });

})(angular);
