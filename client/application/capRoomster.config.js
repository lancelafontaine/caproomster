(function(angular) {
  'use strict';
  angular.module('capRoomster').config([
    '$stateProvider',
    '$urlRouterProvider',
    function($stateProvider, $urlRouterProvider) {
      $stateProvider.state('tab', {
        url: '/',
        template: '<h1>hello</h1>'
      });
      $urlRouterProvider.otherwise('/');
    }
  ]);
})(angular);
