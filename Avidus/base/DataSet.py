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

""" DataSet

    OHLC data 

    contains:
	open
	high
	low
	close
	date

"""

import sys
import string
import pickle
from DateTime import *
from Numeric import *

class DataSet:
    """OHLC Data Set """
    symbol = ''
    adate = []
    open = []
    high = []
    low = []
    close = []
    vol = []
    signal = []
    capital = []
    pl = []

    def __init__ (self):
        "init function for dataset."
        self.Init()
    
    def Init(self):
        self.dateIndex = {}
        self.adate = []
        self.open = []
        self.high = []
        self.low = []
        self.close = []
        self.have_vol = 0
        self.vol = []
        self.mMin = 0
        self.mMax = 100
        self.mVolMin = 0
        self.mVolMax = 100000
        self.mFirstDate = now() + RelativeDateTime(months=-3)
        self.mLastDate = now()

    def setData(self, data, symbol):
        self.symbol = symbol
        
        if len(data) >=5:
            self.adate = data[0]
            self.open = data[1]
            self.high = data[2]
            self.low = data[3]
            self.close = data[4]
        else:
            return

        if len(data)==6:
            self.have_vol = 1
            self.vol = data[5]

        for i in range(len(self.adate)):
            self.dateIndex[self.adate[i]] = i
            
        self.setRanges()

    def indexFromDate(self, date):
        return self.dateIndex[date]
    
    def getMinPrice(self, bars):
        seq = self.low[0:bars]
        if len(seq)==0:
            return 0
        return min(seq)

    def getMaxPrice(self, bars):
        seq = self.high[0:bars]
        if len(seq)==0:
            return 100
        return max(seq)

    def getFirstDate(self, bars):
        return self.mFirstDate

    def getLastDate(self):
        return self.mLastDate
        
    def setRanges(self):
        if len(self.adate) <= 0:
            return
        self.mMax = max(self.high)
        self.mMin = min(self.low)
        if self.have_vol:
            self.mVolMax = max(self.vol)
            self.mVolMin = min(self.vol)
        self.mFirstDate = self.adate[0]
        self.mLastDate = self.adate[-1]

    def toDate(self, datestring):
        "convert a string to a DateTime object"

        # should catch exceptions here....
        #return(DateTimeFrom(datestring))
        return strptime(datestring, "%d-%b-%y")

    def isEmpty(self):
        return len(self.adate) == 0
    
    def parse(self, filename):
       	"parse an input file for data"
        self.Init()
	infile = open(filename, 'r')
	filebuf = infile.read()
	infile.close
	l = string.split(filebuf,'\n')
	i=0
        open_tmp = []
        high_tmp = []
        low_tmp = []
        close_tmp = []
        vol_tmp = []
	while i<(len(l)):	
	    nums = string.split(l[i], ',')
	    if (len(nums) == 6):
	        self.adate.append(self.toDate(nums[0]))
		open_tmp.append(float(nums[1]))
		high_tmp.append(float(nums[2]))
		low_tmp.append(float(nums[3]))
		close_tmp.append(float(nums[4]))
                self.have_vol = 1
                vol_tmp.append(float(nums[5]))
            elif (len(nums) == 5):
	        self.adate.append(self.toDate(nums[0]))
		open_tmp.append(float(nums[1]))
		high_tmp.append(float(nums[2]))
		low_tmp.append(float(nums[3]))
		close_tmp.append(float(nums[4]))
                self.have_vol = 0
            else:
                pass
            i = i + 1
        self.open = array(open_tmp)
        self.high = array(high_tmp)
        self.low = array(low_tmp)
        self.close = array(low_tmp)
        self.vol = array(vol_tmp)
            
        self.setRanges()
		
    def printme(self):
       	"output current data to screen"
	print "DataSet = "
	for i in range(len(self.adate)):
	    print self.adate[i], self.open[i], self.high[i], \
		  self.low[i], \
		  self.close[i], self.vol[i]
        print 'Ranges: ', self.mMax, self.mMin, self.mFirstDate, self.mLastDate
