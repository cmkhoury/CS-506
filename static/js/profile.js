angular.module("ProfileApp", [])
	.controller('ImportCartCtrl', function($scope, $http) {
  		$scope.listOfCarts = [];
  		$scope.listOfItems = [];

  		$http({
		  method: 'GET',
		  url: '/api/searchCart'
		}).then(function successCallback(response) {
			$scope.listOfCarts = response.data[0];
			$scope.listOfItems = response.data[1];
		  }, function errorCallback(response) {
		    // called asynchronously if an error occurs
		    // or server returns response with an error status.
		});

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