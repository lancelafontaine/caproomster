(function(angular){

  'use strict';

  angular.module('caproomster').controller('LoginController', LoginController);

  LoginController.$inject = ['$scope'];

  function LoginController($scope) {

    init();

    function init() {
      loadVideo();
    }

    function loadVideo() {
      $scope.videos = [{
        videoId: 'JDl0AhqHF_s',
        mute: true,
        start: 3
      }];
      $scope.slowShow = true;
      setTimeout(function() {
        $scope.$apply(function(){
          $scope.slowShow = false;
        });
      }, 3000);
    }
  }

})(angular);
