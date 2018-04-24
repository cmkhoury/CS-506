angular.module("ProfileApp", [])
	.controller('ImportCartCtrl', function($scope, $http) {
  		$scope.greeting = 'd!';

  		$scope.importCart = function(){
  			$http({
			  method: 'GET',
			  url: '/wishlist?id='+$scope.wishtlistID
			}).then(function successCallback(response) {
			    closeModal()
			  }, function errorCallback(response) {
			    // called asynchronously if an error occurs
			    // or server returns response with an error status.
			  });
  			
  		}

	});