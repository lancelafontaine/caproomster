(function(angular){

  'use strict';

  angular.module('caproomster.login').controller('caproomster.login.LoginController', LoginController);

  LoginController.$inject = ['$scope', '$state', 'caproomster.api.ApiService'];

  function LoginController($scope, $state, ApiService) {

    init();
    $scope.login = login;

    function init() {
      loadVideo();
      $scope.userInfo = {};
    }

    function loadVideo() {
      $scope.videos = [{
        videoId: 'JDl0AhqHF_s',
        start: 3,
        end: 30,
        loop: true
      }];
    }

    function login() {
      $scope.loginError = false;
      if (!$scope.userInfo.username || !$scope.userInfo.password) {
        $scope.loginError = true;
      }
      else {
        var payload = {
          userId: $scope.userInfo.username,
          password: $scope.userInfo.password
        };
        ApiService.account('login', payload).then(function() {
          $state.go('home');
        }, function(res) {
          $scope.loginError = true;
          console.log(res);
        });
      }
    }

  }

})(angular);
