angular.module("CombineCartApp", [])
	.controller('MainCtrl', function($scope, $http, $q) {
			$scope.currUserId = 0;
  		$scope.matchedUsers = [];
			$scope.listOfItems = [];
			$scope.itemsForCurrentUser = [];
			getMatchedUsers();

			//getItemsFromId(103, $scope.itemsForCurrentUser)

			function getMatchedUsers(){
				$http.get('/api/searchMatches')
				.then(function successCallback(response) {
					console.log(response.data)
					$scope.matchedUsers = response.data[0];
					$scope.listOfItems = response.data[1];
					$scope.currUserId = response.data[2];
			})

			$scope.cartCombination = function(rightCartID){
				var leftCartID = 0;
				for(var i = 0; i < $scope.listOfItems.length; i++){
					if($scope.listOfItems[i].uid == $scope.currUserId){
						leftCartID = $scope.listOfItems[i].cartID;
						break;
					}
				}
					$http.get('/api/cartCombination?cart1Id='+leftCartID+'&cart2Id='+rightCartID)
					.then(function successCallback(response){
						console.log("success")
						getMatchedUsers();
					})
			}
		}
/*
			$scope.getItemsFromUserId = function(userId){
				return $http.get('/api/searchCartFromUserID?userID=' + userId)
					.then(function successCallback(response) {
					 	 var items = response.data;
						 return items;
					});
			}

			$scope.getItemsFromUserId(103).then(function(response){
				console.log(response);
				$scope.itemsForCurrentUser = response;
			});

			function test(uid){
				$scope.getItemsFromUserId(uid).then(function(response){
					$scope.itemsForOtherUsers
				});
			}*/

	});
