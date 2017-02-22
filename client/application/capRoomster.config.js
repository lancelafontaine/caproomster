(function(angular) {
	'use strict';
	angular.module('capRoomster').config([
		'$stateProvider',
		'$urlRouterProvider',
		function($stateProvider, $urlRouterProvider) {
			$stateProvider.state('home', {
				url: '/',
				views: {
					'main@': {
						templateUrl: 'templates/home.html'
					}
				}
			});
			$urlRouterProvider.otherwise('/');
		}
	]);
})(angular);
