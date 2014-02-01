from bs4 import BeautifulSoup
import urllib2
import time

def getCategory(tbody):
    rows = tbody.find('tr')
    columns = rows.find('td')
    print columns.text

def getClasses(tbody):
    classes = tbody.findAll('tr')
    for clazzes in classes:
    	individualCourse = clazzes.findAll('td')
    	components = [course.text for course in individualCourse]
    	if len(components) == 3:
    	    (course_number, course_name, units) = components
    	    print course_number, course_name

baseurl = "http://coursecatalog.web.cmu.edu/dietrichcollegeofhumanitiesandsocialsciences/departmentofsocialanddecisionsciences/"

response = urllib2.urlopen(baseurl).read()

soup = BeautifulSoup(response)

results = soup.findAll('table',{'class':'sc_courselist'})

for result in results:
    tbodies = result.findAll('tbody')
    for (i, tbod) in enumerate(tbodies):
        if i == 0:
            getCategory(tbod)
        else:
            getClasses(tbod)
    print "Break"
    time.sleep(2)

