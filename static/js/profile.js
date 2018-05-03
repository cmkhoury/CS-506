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


	})
	.controller('ImportMatchCtrl', function($scope, $http) {
		$scope.listOfMatches = [];
		// $scope.showMatchSuccessfulModal = true;

		$http({
		  method: 'GET',
		  url: '/api/getCurrentMatches'
	  }).then(function successCallback(response) {
			$scope.listOfMatches = response.data

		}, function errorCallback(response) {
			// called asynchronously if an error occurs
			// or server returns response with an error status.
		});

		$scope.showModal = function(nameOfModal, info) {
			showModal(nameOfModal, info)
		}

		// $scope.showMatchSuccessfulModal = function(){
		// 	$scope.showMatchSuccessfulModal = fals
		// }
        //
		// $scope.closeMatchSuccessfulModal = function(){
		// 	$scope.showMatchSuccessfulModal = false;
		// }
	}
);
