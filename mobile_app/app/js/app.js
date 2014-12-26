'use strict';

/* App Module */

var groupieApp = angular.module('groupieApp',[
	'ngRoute',
	'groupieAppControllers']);

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
			otherwise({
				redirectTo: '/home/'
			});
	}]);

groupieApp.config(['$httpProvider', function($httpProvider) {
		$httpProvider.defaults.headers.common['Content-Type'] = 'application/json; charset=utf-8';
		$httpProvider.defaults.useXDomain = true;
        delete $httpProvider.defaults.headers.common['X-Requested-With'];

        /**
		* Stolen shamelessly from http://stackoverflow.com/a/20276775/2851353 with loads of thanks
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