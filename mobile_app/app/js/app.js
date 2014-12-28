'use strict';

/* App Module */

var groupieApp = angular.module('groupieApp',[
	'ngRoute',
	'groupieAppControllers']);

/* Routes are defined herein
 * Difficult battles with trainers ensue
 * Proceed with caution. 
 * This is the only part you are allowed to touch
 */

groupieApp.config(['$routeProvider',
	function($routeProvider){
		$routeProvider.
			when('/home/',{
				templateUrl: 'partials/home-partial.html',
				controller: 'homePageController'
			}).
			when('/profile/', {
				templateUrl: 'partials/profile-partial.html',
				controller: 'profilePageController'
			}).
			when('/person/:person_pk', {
				templateUrl: 'partials/person-details.html',
				controller: 'personSpecificViewController'
			}).
			when('/signup/', {
				templateUrl: 'partials/signup-partial.html',
				controller: 'signupController'
			}).
			when('/groups/new/', {
				templateUrl: 'partials/groups-new.html',
				controller: 'groupsNewController'
			}).
			when('/groups/:group_pk/', {
				templateUrl: 'partials/groups-details.html',
				controller: 'groupSpecificViewController'
			}).
			when('/posts/new/:group_pk/', {
				templateUrl: 'partials/posts-new.html',
				controller: 'postsNewController'
			}).
			when('/tasks/new/:group_pk', {
				templateUrl: 'partials/tasks-new.html',
				controller: 'tasksNewController'
			}).
			when('/tasks/:task_pk', {
				templateUrl: 'partials/tasks-details.html',
				controller: 'taskSpecificViewController'
			}).
			otherwise({
				redirectTo: '/home/'
			});
	}]);

/* You may not proceed further into the forbidden forest harry,
 * except with Hagrid, then god bless you, you've got a dim witted giant for support
 */

/* Magic shit which enables 
 * sending Cross Domain Post Requests with JSON
 * Don't touch. Just be grateful and pray.
 */ 
groupieApp.config(['$httpProvider', function($httpProvider) {
		$httpProvider.defaults.headers.common['Content-Type'] = 'application/json; charset=utf-8';
		$httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-Requested-With'];

        /**
		* All code below this has been stolen shamelessly from http://stackoverflow.com/a/20276775/2851353 with loads of thanks
        */
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

		/**
		* The workhorse; converts an object to x-www-form-urlencoded serialization.
		* @param {Object} obj
		* @return {String}
		*/ 
		var param = function(obj) {
		var query = '', name, value, fullSubName, subName, subValue, innerObj, i;

		for(name in obj) {
		  value = obj[name];

		  if(value instanceof Array) {
		    for(i=0; i<value.length; ++i) {
		      subValue = value[i];
		      fullSubName = name + '[' + i + ']';
		      innerObj = {};
		      innerObj[fullSubName] = subValue;
		      query += param(innerObj) + '&';
		    }
		  }
		  else if(value instanceof Object) {
		    for(subName in value) {
		      subValue = value[subName];
		      fullSubName = name + '[' + subName + ']';
		      innerObj = {};
		      innerObj[fullSubName] = subValue;
		      query += param(innerObj) + '&';
		    }
		  }
		  else if(value !== undefined && value !== null)
		    query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
		}

		return query.length ? query.substr(0, query.length - 1) : query;
		};

		// Override $http service's default transformRequest
		$httpProvider.defaults.transformRequest = [function(data) {
		return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
		}];
    }
]);

/* Removes the unsafe extension from app: protocal
 * see here http://stackoverflow.com/a/15769779/2851353
 */
groupieApp.config( [
    '$compileProvider',
    function( $compileProvider )
    {   
        $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|chrome-extension|app):/);
        // Angular before v1.2 uses $compileProvider.urlSanitizationWhitelist(...)
    }
]);