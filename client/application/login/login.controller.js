(function(angular){

  'use strict';

  angular.module('caproomster.login').controller('caproomster.login.LoginController', LoginController);

  LoginController.$inject = ['$state', 'caproomster.api.ApiService'];

  function LoginController($state, ApiService) {

    var vm = this;
    vm.login = login;
    init();

    function init() {
      loadVideo();
      vm.userInfo = {};
    }

    function loadVideo() {
      vm.videos = [{
        videoId: 'JDl0AhqHF_s',
        start: 3,
        end: 30,
        loop: true
      }];
    }

    function login() {
      vm.loginError = false;
      if (!vm.userInfo.username || !vm.userInfo.password) {
        vm.loginError = true;
      }
      else {
        var payload = {
          userId: vm.userInfo.username,
          password: vm.userInfo.password
        };
        ApiService.account('login', payload).then(function() {
          $state.go('home');
        }, function(res) {
          vm.loginError = true;
          console.log(res);
        });
      }
    }

  }

})(angular);
