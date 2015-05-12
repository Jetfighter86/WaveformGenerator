__author__ = 'Phillip'

import urllib2

req = urllib2.Request('http://www.voidspace.org.uk')
response =urllib2.urlopen(req)
the_page = response.read()
print the_page