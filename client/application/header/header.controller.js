(function(angular) {

  'use strict';

  angular.module('caproomster.header').controller('caproomster.header.HeaderController', HeaderController);
  HeaderController.$inject = ['$stateParams'];

  function HeaderController($stateParams) {

    var vm = this;
    vm.$onInit = init;

    function init() {
    }

  }

})(angular);
