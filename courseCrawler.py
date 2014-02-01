from bs4 import BeautifulSoup
import urllib2

baseurl = "http://coursecatalog.web.cmu.edu/dietrichcollegeofhumanitiesandsocialsciences/departmentofsocialanddecisionsciences/"

response = urllib2.urlopen(baseurl).read()

soup = BeautifulSoup(response)

print soup.prettify()