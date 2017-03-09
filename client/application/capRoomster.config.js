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
						templateUrl: 'login/login.template.html',
						controller: 'LoginController'
					}
				}
			});

			$stateProvider.state('home', {
				url: '/home',
				views: {
					'main': {
						templateUrl: 'home/home.template.html'
					}
				}
			})
			
			$urlRouterProvider.otherwise('/');

		}

	]);

})(angular);
