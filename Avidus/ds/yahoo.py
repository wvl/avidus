#
# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Original Code is  Avidus.
#
# The Initial Developer of the Original Code is Wayne Larsen.  
# Portions created by Wayne Larsen are
# Copyright (C) 2000.  All Rights Reserved.
#
# Contributor(s):
#

from DateTime import *
import httplib

class DataImporter:

    def __init__(self):
        self.startdate = now() + RelativeDateTime(months=-3)
        self.stopdate = now()

        self.dataserver = "chart.yahoo.com"

    def getData(self, symbol, start=0, stop=0):
        h = httplib.HTTP(self.dataserver)

        if start==0:
            start=self.startdate
        if stop==0:
            stop=self.stopdate
            
        request = '/table.csv?s=' + symbol + \
                  '&a=' + `start.month` + \
                  '&b=' + `start.day` + \
                  '&c=' + `start.year` + \
                  '&d=' + `stop.month` + \
                  '&e=' + `stop.day` + \
                  '&f=' + `stop.year` + \
                  '&g=d&q=q&y=0&z=' + symbol + \
                  '&x=.csv'
        h.putrequest('GET', request)
        h.putheader('Accept', 'text/html')
        h.putheader('Accept', 'text/plain')
        h.endheaders()
        errcode, errmsg, headers = h.getreply()
        if errcode != 200:
            print 'Error getting data: ', errcode
        f = h.getfile()
        return f

if __name__=='__main__':
    d = DataImporter()
    f = d.getData('TDFX', now() - RelativeDateTime(years=+2), \
              now() - RelativeDateTime(years=+1))
    data = f.read()
    print data
