(function(angular){

  'use strict';

  angular.module('caproomster').controller('LoginController', LoginController);

  LoginController.$inject = ['$scope', '$state'];

  function LoginController($scope, $state) {

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
        console.log("here");
        $scope.loginError = true;
        // do something here
        //$state.go('home');
      }
    }

  }

})(angular);
