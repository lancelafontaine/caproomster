(function(angular) {

  'use strict';

  angular.module('caproomster').config([

    '$stateProvider',
    '$urlRouterProvider',

    function($stateProvider, $urlRouterProvider) {

      $stateProvider.state('login', {
        url: '/',
        views: {
          'header': {
            component: 'loginComponent'
          }
        }
      });

      $stateProvider.state('home', {
        url: '/home',
        views: {
          'header': {
            component: 'headerComponent'
          },
          'main': {
            templateUrl: 'home/home.template.html',
            controller: 'HomeController'
          }
        }
      });

      $urlRouterProvider.otherwise('/');

    }

  ]);

})(angular);
