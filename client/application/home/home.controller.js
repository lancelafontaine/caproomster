(function(angular){

  'use strict';

  angular.module('caproomster').controller('HomeController', HomeController);

  HomeController.$inject = ['$scope', '$state'];

  function HomeController($scope, $state) {

    $scope.uiConfig = {
      calendar:{
        height: 450,
        editable: true,
        header:{
          left: 'month basicWeek basicDay agendaWeek agendaDay',
          center: 'title',
          right: 'today prev,next'
        },
        eventClick: $scope.alertEventOnClick,
        eventDrop: $scope.alertOnDrop,
        eventResize: $scope.alertOnResize
      }
    };

  }

})(angular);
