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

import sys,string,math
from qt import *
from DateTime import *

class XAxis(QWidget):
    """ XAxis for the chart """

    def __init__(self, data, yAxisSize, chartProperties, \
                 parent=None, name='XAxis'):
        """ constructor """
        QWidget.__init__(self, parent, name)
        self.mYAxisSize = yAxisSize

        self.setMinimumSize(800,30)
        self.setMaximumSize(4000,30)

        self.minimumPixelsBetweenBars = 5
        self.numberOfBars = 80 # one year default (252)
        
        self.mProps = chartProperties
        self.connect(self.mProps, PYSIGNAL('propertiesChanged'), self.redraw)
     
        self.mMajorTicks = []
        self.mMinorTicks = []

        self.xsize = self.width() - self.mYAxisSize

        self.UpdateData(data)
        self.redraw()

    def setMinimumPixelsBetweenBars(self, val):
        self.minimumPixelsBetweenBars = val
        
    def setNumBars(self, numBars):
        self.numberOfBars = numBars
        
    def getNumBars(self):
        return self.numberOfBars
    
    def changeTimeFrame(self, bars):
        self.numberOfBars = bars
        self.emit(PYSIGNAL('propertiesChanged'))
                  
    def UpdateData(self, chartData, width=0):
        self.mData = chartData
        newsize = self.setDateRange(width)
        self.repaint(self.rect(), 0)
        return newsize

    def resizeEvent(self, resizeEvent):
        self.xsize = self.width() - self.mYAxisSize
        self.repaint(self.rect(),0)
        
    def redraw(self):
        self.setBackgroundColor(self.mProps.ChartColors['Background Color'])
        self.repaint(self.rect(), 0)

    # return x coords of given indice
    def findX(self, val):
        #print 'XAXis findX: ', val, self.xsize, self.mDateModifier, \
        #      self.mDateOffset, \
        #      self.xsize - (self.mDateModifier*val + self.mDateOffset)
        return self.width()-self.mYAxisSize - (self.mDateModifier*val + self.mDateOffset)

    # return indice given input x coords
    def findXindex(self, val):
        if val>(self.width()-self.mYAxisSize):
            return 0
        
        i = abs(round((self.width()-self.mYAxisSize - val - \
                         self.mDateOffset)/self.mDateModifier))
        if i >= self.mNumDays:
            i = self.mNumDays - 1
        return i
    
    def setDateRange(self, windowWidth=0):
        """ find the date modifier, offset """

        self.mNumDays = len(self.mData.adate)+1
        if self.mNumDays > self.numberOfBars:
            self.mNumDays = self.numberOfBars
        
        if self.mNumDays <= 0:
            self.mDateModifier = 0
            self.mDateOffset = 0
            return

        #if self.xwidth != windowWidth:
        #    self.xwidth = windowWidth

        #if self.width() > self.xwidth:
        #    self.xwidth = self.width()

        # try the window width
        self.mDateModifier = int((windowWidth-self.mYAxisSize)/float(self.mNumDays))
        self.mDateOffset = self.mDateModifier/2

        newXSize = windowWidth
        
        if self.mDateModifier < self.minimumPixelsBetweenBars:
            self.mDateModifier = self.minimumPixelsBetweenBars
            newXSize = self.mDateModifier*float(self.mNumDays)
            self.mDateOffset = self.mDateModifier/2

        else:
            # Add a few bars, so left side is not blank
            self.mNumDays = self.mNumDays + 10
            
        self.setTicks()

        return newXSize
        

    def setTicks(self):
        self.mMajorTicks = []
        self.mMinorTicks = []
        if (self.mNumDays < 67):
            for i in range(len(self.mData.adate)):
                if self.mData.adate[i].day_of_week == 0:
                    self.mMajorTicks.append(i)
                else:
                    self.mMinorTicks.append(i)
        else:
            cur_month = self.mData.adate[0].month
            for i in range(len(self.mData.adate)):
                if self.mData.adate[i].month != cur_month:
                    cur_month = self.mData.adate[i].month
                    self.mMajorTicks.append(i-1)
                elif self.mData.adate[i].day_of_week == 0:
                    self.mMinorTicks.append(i)

    def paintEvent(self, e):
        p = QPainter()
        p.begin(self)

        xr = self.rect()
        pix = QPixmap(xr.size())
        tmp = QPainter()
        pix.fill(self, xr.topLeft())
        tmp.begin(pix)

        tmp.setPen(self.mProps.ChartColors['Axes Color'])
        tmp.drawLine(0,0,self.width(),0)
        tmp.drawLine(self.width()-self.mYAxisSize,0, \
                     self.width()-self.mYAxisSize, self.height())
        for i in range(len(self.mMajorTicks)):
            x = self.findX(self.mMajorTicks[i])
            tmp.drawLine(x,0,x,10)
            if self.mNumDays < 67:
                xt = self.toDay(self.mData.adate[self.mMajorTicks[i]])
            else:
                xt = self.toMonth(self.mData.adate[self.mMajorTicks[i]])
            tmp.drawText(x+1,20, xt)

        for i in range(len(self.mMinorTicks)):
            x = self.findX(self.mMinorTicks[i])
            tmp.drawLine(x,0,x,5)
            
            
            #for i in range(self.mNumDays):
            #    x = self.findX(i)
            #    tmp.drawLine(x,0,x,10)
                    
        tmp.end()

        p.drawPixmap(xr.topLeft(), pix)
        p.end()

    def increment(self, date):
        date = date + RelativeDateTime(days=+1)
        if date.day_of_week == 5:
            date = date + RelativeDateTime(days=+2)
        return date
        
    def toDOW(self, date):
        dow = date.day_of_week
        if dow == 0:
            return 'M'
        elif dow == 1:
            return 'T'
        elif dow == 2:
            return 'W'
        elif dow == 3:
            return 'T'
        elif dow == 4:
            return 'F'
        else:
            return 'Error'

    def toMonth(self, date):
        if date.month == 1:
            return date.strftime("%Y")
        return date.strftime("%b")

    def toDay(self, date):
        return str(date.day)



