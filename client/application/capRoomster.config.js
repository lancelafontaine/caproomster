(function(angular) {

	'use strict';

	angular.module('caproomster').config([
		
		'$stateProvider',
		'$urlRouterProvider',

		function($stateProvider, $urlRouterProvider) {

			$stateProvider.state('home', {
				url: '/',
				views: {
					'header@': {
						templateUrl: 'login/login.template.html',
						controller: 'LoginController'
					}
				}
			});
			
			$urlRouterProvider.otherwise('/');

		}

	]);

})(angular);
