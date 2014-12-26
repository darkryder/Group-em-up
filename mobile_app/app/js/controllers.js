
/* Controllers */

var groupieAppControllers = angular.module('groupieAppControllers', []);

groupieAppControllers.controller('profilePageController', ['$scope', 
	function($scope){
		$scope.person = {
			"name": "John Doe",
			"email": "ssatija95@gmail.com",
			"gender": "M"
		};
	}]);

groupieAppControllers.controller('homePageController', ['$scope', '$http',
	function($scope, $http){
		$scope.people = [
			{	name: "A",
				email: "a@b.com",
				gender: "M"
			},
			{	name: "B",
				email: "b@b.com",
				gender: "M"
			},
			{	name: "C",
				email: "c@b.com",
				gender: "F"
			},
			{	name: "D",
				email: "d@b.com",
				gender: "F"
			},
			{	name: "E",
				email: "e@b.com",
				gender: "M"
			}
		];

		$scope.response_from_server = "Nothing"

		$scope.server_test = function(){

			// var temp = $http.get('https://blooming-badlands-6507.herokuapp.com/stuff/test_logged_in/');
			var temp = $http.post('https://blooming-badlands-6507.herokuapp.com/stuff/test_logged_in/', {
				'pk': '1',
				'key1': '7ekDAErMWS9enfmkkbE26rPovMd3lAkd',
				'key2': 'Z5MCEuMek3ALipPAJuttuHdDWobmVFHL',
			});
			
			console.log("Sending");
			temp.success(function(data){
				$scope.response_from_server = JSON.parse(JSON.stringify(data))['result'];
				console.log(JSON.stringify(data));
				console.log("success")
			})
			temp.error(function(data, status){
				$scope.response_from_server = data;
				console.log("error" + data);
				console.log("error" + status);
				
			})

			// $.get("https://blooming-badlands-6507.herokuapp.com/stuff/test/", function(data){
			// 	console.log("success");
			// 	console.log("" + JSON.stringify(data));
			// })
			// .fail(function(data, status){
			// 	console.log("failed " + JSON.stringify(data) + " " + status);
			// })
			// .always(function(){
			// 	console.log('finished');
			// })
		}
	}])