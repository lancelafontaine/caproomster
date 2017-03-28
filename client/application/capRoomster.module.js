(function(angular) {

  'use strict';

  angular.module('caproomster', [
    'ui.router',
    'angularVideoBg',
    'ui.bootstrap',
    'ngResource',
    'ngSanitize',
    'ngStorage',
    'ngAnimate',
    'mwl.calendar',
    'caproomster.api',
    'caproomster.login',
    'caproomster.header',
    'caproomster.home'
  ]);

})(angular);
