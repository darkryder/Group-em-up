
// TODO
// As of now except for personal data, get all data from the api
// don't store anything locally
// Add flash messages


/* credits 
 * Server connection spinner: https://github.com/tobiasahlin/SpinKit
 * mocks ups: https://moqups.com/#!/edit/f.ssat95@gmail.com/EO52faS9
 */

/* Controllers */

/* Contains variables that should not be directly
 * accessed apart from using getter or setting methods
 * from commonFunctions object
 */
var _hiddenCommonData = {
	storage: window.localStorage,
	api_link: "http://blooming-badlands-6507.herokuapp.com/stuff/",
}


/* Common functions used throughout the app
 *
 */
var commonFunctions = {
	show_server_contact_attempt: function(){
		$("#server-connection-spinner-base").show();
		$("#server-connection-spinner-white").show();
		$("#server-connection-spinner-success").show();
		$("#server-connection-spinner-fail").hide()
	},

	show_server_contact_failed: function(){
		$("#server-connection-spinner-base").show();
		$("#server-connection-spinner-white").show();
		$("#server-connection-spinner-success").hide();
		$("#server-connection-spinner-fail").show()

		setTimeout(function(){commonFunctions.hide_server_contact();}, 1000 * 5)
	},

	hide_server_contact: function(){
		$("#server-connection-spinner-base").hide();
		$("#server-connection-spinner-white").hide();
		$("#server-connection-spinner-success").hide();
		$("#server-connection-spinner-fail").hide()
	},

	test_server_connection: function(http){
		return http.get(_hiddenCommonData.api_link + 'test/');
	},

	// sees if call was successfull
	api_call_successfull: function(data_from_server){
		return (data_from_server['result'] === true ? true : false);
	},

	get_empty_person_object: function(){
		return {
			first_name: '', last_name: '', gender: null, takentasks: [], posts: [], 
			groups: [], points: null, tasksIAssigned: [], completedtasks: [],
			badges: [], adminOf: [], email: ''
		};
	},

	get_empty_group_object: function(){
		return {
			name: "", description: "", pk: null, points: null,
			members: [], tasks: [], admins: [], posts: []
		}
	},

	// gets whatever the storage medium be
	get_storage: function(){
		return _hiddenCommonData.storage;
	},

	get_api_link: function(){
		return _hiddenCommonData.api_link;
	},

	// tells whether the person is logged in
	is_logged_in: function(){
		return (this.get_storage().getItem('is_logged_in') === 'true' ? true: false);
	},

	// sets whether person is logged in 
	set_logged_in: function(whether){
		this.get_storage().setItem('is_logged_in', whether);
	},

	// get authentication data
	get_auth_data: function(){
		return JSON.parse(this.get_storage().getItem('auth_data'));
	},

	// sets authentication data. used only once while registeration.
	_set_auth_data: function(data_from_server){
		var auth_data = {
			"pk": data_from_server['pk'],
			"key1": data_from_server['key1'],
			"key2": data_from_server["key2"]
		};
		this.get_storage().setItem('auth_data', JSON.stringify(auth_data));
	},

	get_self_details: function(){
		return JSON.parse(this.get_storage().getItem('self_details'));
	},

	set_self_details: function(data_from_server){
		var data = data_from_server.data;
		data.email = this._get_self_email;
		this.get_storage().setItem('self_details',
						JSON.stringify(data));
	},

	_get_self_email: function(){
		return this.get_storage().getItem('_self_email');
	},
	
	_set_self_email: function(email){
		return this.get_storage().setItem('_self_email', email);
	},

	// this follows builder pattern. It will return 
	// the implemented jqeury $.post
	fetch_self_details: function(http){
		return this.fetch_person_details(http, this.get_auth_data['pk']);
	},

	// this follows builder pattern. It will return 
	// the implemented jqeury $.post
	fetch_person_details: function(http, who_pk){
		var auth_data = this.get_auth_data();
		var self_pk = auth_data['pk']
		return http.post(_hiddenCommonData.api_link + 'person/' + self_pk +'/', auth_data);
	},

	get_person_details: function(who_pk){

	},

	set_person_details: function(who_pk, data_from_server){

	},

	fetch_group_details: function(http, which_pk){
		var auth_data = this.get_auth_data();
		return http.post(_hiddenCommonData.api_link + 'groups/' + which_pk + '/', auth_data);
	},

	set_group_details: function(which, data_from_server){

	},
}


var groupieAppControllers = angular.module('groupieAppControllers', []);


groupieAppControllers.controller('homePageController', ['$scope', '$http',
	function($scope, $http){

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
				// $scope.response_from_server = JSON.parse(JSON.stringify(data))['result'];
				$scope.response_from_server = data['result']
				console.log(JSON.stringify(data));
				console.log("success")
			})
			temp.error(function(data, status){
				$scope.response_from_server = data;
				console.log("error" + data);
				console.log("error" + status);
				
			})
		}
	}]);


/* Profile controller
 * If user is not logged in, it is redirected to signup page, which has the option of password reset too
 * It either gets the prefetched cached data or fetches the profile data
 * from the server and displays it to the user
 * As of now, it gets all the data from the api
 * TODO: = cache data
 */
groupieAppControllers.controller('profilePageController', ['$scope', '$http', '$location',
	function($scope, $http, $location){

		$scope.bucket = {person: commonFunctions.get_empty_person_object()};

		if (!commonFunctions.is_logged_in()){
			console.log("not logged in");
			$location.path("signup/");
		}
		else{
			var auth_data = commonFunctions.get_auth_data();

			commonFunctions.show_server_contact_attempt();
			
			// TODO remove fetch details to use get_self_details after caching output
			commonFunctions.fetch_self_details($http).
			success(function(data){
				commonFunctions.hide_server_contact();
				if (commonFunctions.api_call_successfull(data)){
					$scope.bucket.person = data.data;
					$scope.bucket.person.email = commonFunctions._get_self_email();
					console.log("fetched self details:" + JSON.stringify($scope.bucket.person));
				}else{
					commonFunctions.show_server_contact_failed();
					console.log("API call unsuccessful. " + JSON.stringify(data.reason));
				}
			}).
			error(function(status, data){
				commonFunctions.show_server_contact_failed();
				console.log("failed");
			});
		}
	}]);

/* Signup controller.
 * If person is already signed up, he should never be shown this page,
 * However if he is, by some mistake, he would be redirected back to home
 * with a flash message
 * TODO: = password reset
 *       = flash message
 */
groupieAppControllers.controller('signupController', ['$scope', '$http', '$location', 
	function($scope, $http, $location){

		if (commonFunctions.is_logged_in()){
			console.log("already logged in");
			$location.path("profile/");
		} 
		else {
			console.log("not logged in");
		};

		$scope.first_name = "";
		$scope.last_name = "";
		$scope.email = "";
		$scope.gender = "female";


		$scope.signup = function(){
			var data = {
				"first_name": $scope.first_name,
				"last_name": $scope.last_name,
				"email": $scope.email,
				"gender": ($scope.gender == "female" ? true: false)
			};
			console.log("Sending data: " + JSON.stringify(data));

			commonFunctions.show_server_contact_attempt();

			$http.post(_hiddenCommonData.api_link+'signup/', data).
			success(function(data){
				console.log(JSON.stringify(data));

				if (commonFunctions.api_call_successfull(data)){
					commonFunctions._set_auth_data(data);
					commonFunctions.set_logged_in(true);
					commonFunctions._set_self_email($scope.email);
					commonFunctions.hide_server_contact();
					console.log("Signup completed");
					$location.path("profile/");
				} else {
					commonFunctions.show_server_contact_failed();
					console.log("API call: response from server. result false");
					console.log("RESPONSE: " + JSON.stringify(data));
				}
			}).
			error(function(data, status){
				console.log("error" + data);
				console.log("error" + status);
				commonFunctions.show_server_contact_failed();
			});
		}
	}]);

/* Allows creating new groups
 * If not logged in, redirects to signup page.
 * TODO: save group data in storage
 */
groupieAppControllers.controller('groupsNewController', ['$scope', '$location', '$http',
	function($scope, $location, $http){

		if (!commonFunctions.is_logged_in()){
			console.log("not logged in");
			$location.path("signup/");
		}
		else {
			$scope.group_name = "";
			$scope.group_description = "";
			$scope.group_visibility = "public";

			$scope.create_group = function(){
				var link = commonFunctions.get_api_link();
				var data = commonFunctions.get_auth_data();
				data['name'] = $scope.group_name;
				data['description'] = $scope.group_description;
				data['private'] = ($scope.group_visibility === 'private' ? true: false);

				console.log("Sending data: " + JSON.stringify(data));
				commonFunctions.show_server_contact_attempt();

				$http.post(link + 'groups/new/', data).
					success(function(data){
						if (commonFunctions.api_call_successfull(data)){
							commonFunctions.hide_server_contact();
							console.log("new group created");
							console.log(JSON.stringify(data));
						} else {
							commonFunctions.show_server_contact_failed();
							console.log("API call: response from server. result false");
							console.log("RESPONSE: " + JSON.stringify(data));
						}
					}).
					error(function(data, status){
						console.log("error data " + data);
						console.log("error status " + status);
						commonFunctions.show_server_contact_failed();
					});
			}
		}
	}]);

groupieAppControllers.controller('groupSpecificView', ['$scope', '$http', '$location', '$routeParams',
	function($scope, $http, $location, $routeParams){

		if (!commonFunctions.is_logged_in()){
			console.log("not logged in");
			$location.path("signup/");
		} else {
			$scope.bucket = {group: commonFunctions.get_empty_group_object()};
			var group_pk = $routeParams.group_pk;

			commonFunctions.show_server_contact_attempt();
			commonFunctions.fetch_group_details($http, group_pk).
				success(function(data){
					if (commonFunctions.api_call_successfull(data)){
						commonFunctions.hide_server_contact();
						$scope.bucket.group = data.data;
						console.log("FETCHED: " + JSON.stringify(data));
					} else{
						commonFunctions.show_server_contact_failed();
						console.log("API call: response from server. result false");
						console.log("RESPONSE: " + JSON.stringify(data));
					}
				}).
				error(function(data, status){
					console.log("error data " + data);
					console.log("error status " + status);
					commonFunctions.show_server_contact_failed();
				});
		}
	}]);