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

import sys, string, math
from qt import *


class YAxis:
    """ Y Axis class """

    def __init__(self, chartProperties, rect):
        self.mProps = chartProperties
        self.mYRect = rect
        self.mYRange = 0
        self.mMax = 0
        self.mMin = 0
        self.max = 0
        self.min = 0
        self.mMaxRange = []
        self.mMinRange = []
        
    def findY(self, val):
        return self.mYRect.height() - self.mPriceModifier* \
               (val - self.mMin) - self.mPriceOffset

    def setRange(self, min, max):
        self.min = min
        self.max = max
        self.mMin = min  # - (0.1*abs(min))
        self.mMax = max

        self.resize(self.mYRect)

    def adjustUp(self, maxinc):
        if (maxinc < 1):
            self.mMaxInc = 1
            self.mMinInc = 0.5
        elif (maxinc < 2):
            self.mMaxInc = 2
            self.mMinInc = 1
        elif (maxinc < 5):
            self.mMaxInc = 5
            self.mMinInc = 1
        elif (maxinc < 50):
            self.mMaxInc = (math.floor(maxinc / 5) + 1)*5
            self.mMinInc = self.mMaxInc / 2
        elif (maxinc < 1000):
            self.mMaxInc = (math.floor(maxinc / 50) + 1)*50
            self.mMinInc = self.mMaxInc / 2 
        elif (maxinc < 1e4):
            self.mMaxInc =  (math.floor(maxinc / 1000) + 1)*1000
            self.mMinInc = self.mMaxInc / 2
        elif (maxinc < 1e5):
            self.mMaxInc = (math.floor(maxinc / 2e4) + 1)*2e4
            self.mMinInc = self.mMaxInc / 6
        elif (maxinc < 1e6):   # 1 mil
            self.mMaxInc = (math.floor(maxinc / 2e5) + 1)*2e5
            self.mMinInc = self.mMaxInc / 2
        elif (maxinc < 1e7):  # 10 mil
            self.mMaxInc = (math.floor(maxinc / 5e6) + 1)*5e6
            self.mMinInc = self.mMaxInc / 2
        elif (maxinc < 1e8):
            self.mMaxInc = (math.floor(maxinc / 5e7)+ 1)*5e7
            self.mMinInc = self.mMaxInc / 2
        else:
            self.mMaxInc = (math.floor(maxinc/5e8) + 1)*5e8
            self.mMinInc = self.mMaxInc /2

    # major modes should be:
    # 1, 2, 5, 10, 15, 20, 25, ...
    # there should be approximately 4-5 major bars on the graph
    # that number should be based on the size of the graph
    def resize(self, rect):
        """ output is - price multiple, offset """

        self.mYRect = rect
        self.mYRange = (self.max - self.min)
        maxinc = self.mYRange/5  # ~5 major ticks
        self.adjustUp(maxinc)
        self.mMaxRange = []
        self.mMinRange = []

        # Get a list of max ticks
        i = math.floor(self.min/self.mMaxInc)
        tmp = self.mMaxInc*i
        self.mMin = tmp
        while tmp <= self.max:
            #if tmp > self.mMin:
            self.mMaxRange.append(tmp)
            i = i + 1
            tmp = self.mMaxInc * i
        self.mMaxRange.append(tmp)
        self.mMax = tmp
        self.mYRange = self.mMax - self.mMin

        # get a list of min ticks
        i = math.floor(self.min/self.mMinInc)
        tmp = self.mMinInc*i
        while tmp < self.max:
            if tmp > self.min:
                self.mMinRange.append(tmp)
            i = i+1
            tmp = self.mMinInc * i
            
        if self.mYRange == 0:
            self.mPriceModifier = 0
            self.mPriceOffset = 0
            return

        self.mPriceModifier = (self.mYRect.height()-20)/self.mYRange
        self.mPriceOffset = self.mPriceModifier / 2

        
        #self.mPriceOffset = (self.mYRange - (self.mMax - self.mMin)) \
        #                    * self.mPriceModifier / 2

    def PaintYAxis(self,widget,p):
        p.setPen(self.mProps.ChartColors['Axes Color'])
                    
        p.drawLine(0,0,0,self.mYRect.height())

        if self.mYRange > 0:
            for i in range(len(self.mMaxRange)):
                val = self.mMaxRange[i]
                y = self.findY(val)
                p.drawLine(0,y,10,y)
                yt = '%g' % val
                p.drawText(4,y-1,yt)
            for i in range(len(self.mMinRange)):
                val = self.mMinRange[i]
                y = self.findY(self.mMinRange[i])
                p.drawLine(0,y,5,y)





