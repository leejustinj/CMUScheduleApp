from bs4 import BeautifulSoup
import urllib2
import simplejson

app_id = '30b2a2d8-cbe4-4103-bbf7-f5c559f44a98'
app_secret = 'Jo7ga9mgpaBeJm6T4ro57NA-ifXXziNl-ghmGu-t4z3-t9lHuWee6LL3'

def parseLectures(lectures):
	for lecture in lectures:
        lec_keys = lecture.keys()
        


def findCourses(semester, department):
    baseUrl = 'https://apis.scottylabs.org/v1/schedule/%s/departments/%s/courses?app_id=%s&app_secret_key=%s' % (semester, department, app_id, app_secret)
    response = urllib2.urlopen(baseUrl)
    courseJson = simplejson.load(response)
    courses = courseJson['courses']
    for course in courses[:2]:
        units = course['units']
        lectures = course['lectures']
        number = course['number']
        name = course['name']
        

findCourses("S14","15")