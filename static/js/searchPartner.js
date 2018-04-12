angular.module("SearchPartnerApp", [])
	.controller('MainController', ['$scope', function($scope) {
  		$scope.greeting = 'd!';
  		alert("hello")

  		$scope.testFn = function(){
  			alert();
  		}
	}]);