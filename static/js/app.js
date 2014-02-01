var scheduleApp = angular.module('scheduleApp', []);

scheduleApp.config(function ($interpolateProvider)
{
    $interpolateProvider.startSymbol('|}');
    $interpolateProvider.endSymbol('{|');
})

scheduleApp.controller('ScheduleCtrl', function () {})

scheduleApp.controller('AddCourseCtrl', function ($scope, $http) {
    $http.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";

    $scope.semesterLabel = function(s)
    {
	return (s.semester + " " + s.year.toString())
    }

    $scope.semesters = 
	[
	    {semester : "Spring", year : 2014},
	    {semester : "Fall", year : 2014},
	    {semester : "Spring", year : 2015},
	    {semester : "Fall", year : 2015}
	]

    $scope.addCourse = function(user, course)
    {
	var courseId = undefined
	var courseUrl = '/course/' + course.departmentNumber.toString() + '/' + course.courseNumber.toString()

	function addScheduledClass(user, courseId)
	{
	    $http.post('/user/' + user.andrewId + '/schedule', 
		       {course : courseId,
			year : $scope.semester.year,
			semester : $scope.semester.semester
		       })
	}

	$http.get(courseUrl).
	    success(function(data)
		    {
			if (data.courses.length > 0)
			{
			    courseId = data.courses[0].id;
			    addScheduledClass(user, courseId);
			}
			else
			{
			    $http.put(courseUrl).
				success(function(data)
					{
					    courseId = data.id;
					    addScheduledClass(user, courseId); 
					})
			}
		    })
    }
})
