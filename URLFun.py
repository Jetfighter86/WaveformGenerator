__author__ = 'Phillip'

import urllib2, httplib
import requests
# addr = 'http://localhost:19501/sniffers/COM13'
# req = urllib2.Request(addr)
# res = urllib2.urlopen(req)
# print res.read()
# httplib.HTTPConnection.request('PUT',addr,'action=start',"Sniffer")


# using requests
payload = {'action':'stop'}
r=requests.put('http://localhost:19501/sniffers/COM13',data=payload)
print r.status_code