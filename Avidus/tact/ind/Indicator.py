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

from Avidus.base.DataSet import DataSet
from Avidus.tact.base.StyleCombo import *
from qt import *

class Indicator:
    """ Base class for indicators """

    def __init__(self, chartData, xAxis, yAxis):
        self.mData = chartData
        self.mXAxis = xAxis
        self.mYAxis = yAxis

        self.mSeries = []
        self.mSeries2 = []

        self.mOverrideMin = 0
        self.mMin = 0

        self.Ind1Color = Qt.cyan
        self.Ind2Color = Qt.blue
        

    def Min(self):
        if self.mOverrideMin:
            return self.mMin
        else:
            min = 9999999
            for i in range(len(self.mSeries)):
                if self.mSeries[i] != 'NULL':
                    if self.mSeries[i] < min:
                        min = self.mSeries[i]
            return min
    
    def Max(self):
        max = 0
        for i in range(len(self.mSeries)):
            if self.mSeries[i] != 'NULL':
                if self.mSeries[i] > max:
                    max = self.mSeries[i]
        return max
    
    def setIndicatorType(self, type):
        self.mType = type
        if self.mType == 'line':
            self.Paint = self.PaintLine
        elif self.mType == 'sparseline':
            self.Paint = self.PaintSparseLine
        elif self.mType == 'macd':
            self.Paint = self.PaintMACD
        elif self.mType == 'bar':
            self.Paint = self.PaintBar
        elif self.mType == 'filledline':
            self.Paint = self.PaintFilledLine
        else:
            raise 'Unknown Indicator Type'

    def setMin(self, min):
        self.mOverrideMin = 1
        self.mMin = min
        
    def PaintLine(self,widget,p):
        p.setPen(self.Ind1Color)
        self.paintLine(p,self.mSeries)
        
    def paintLine(self, p, data):
        for i in range(min([self.mXAxis.mNumDays, len(data)])-1):
            x1 = self.mXAxis.findX(i)
            x2 = self.mXAxis.findX(i+1)
            y1 = self.mYAxis.findY(data[i])
            y2 = self.mYAxis.findY(data[i+1])
            p.drawLine(x1,y1,x2,y2)
            
        
    def PaintMACD(self, widget, p):
        p.setPen(self.Ind1Color)
        for i in range(min([self.mXAxis.mNumDays, len(self.mSeries)])-1):
            x1 = self.mXAxis.findX(i)
            x2 = self.mXAxis.findX(i+1)
            y1 = self.mYAxis.findY(self.mSeries[i])
            y2 = self.mYAxis.findY(self.mSeries[i+1])
            p.drawLine(x1,y1,x2,y2)
        p.setPen(QPen(self.Ind2Color,1,Qt.PenStyle.DotLine))
        for i in range(min([self.mXAxis.mNumDays, len(self.mSeries2)])-1):
            x1 = self.mXAxis.findX(i)
            x2 = self.mXAxis.findX(i+1)
            y1 = self.mYAxis.findY(self.mSeries2[i])
            y2 = self.mYAxis.findY(self.mSeries2[i+1])
            p.drawLine(x1,y1,x2,y2)
        
    def PaintBar(self,widget,p):
        p.setPen(self.Ind1Color)
        for i in range(min([self.mXAxis.mNumDays, len(self.mSeries)])):
            x1 = self.mXAxis.findX(i)
            x2 = x1
            y1 = self.mYAxis.findY(self.mSeries[i])
            y2 = self.mYAxis.findY(self.Min())
            p.drawLine(x1,y1,x2,y2)

    def PaintFilledLine(self, widget, p):
        p.setPen(self.Ind1Color)
        p.setBrush(QBrush(self.Ind1Color,Qt.SolidPattern))
        if len(self.mSeries)==0:
            p.drawText(20,20,'No Data')
            return
        
        for i in range(min([self.mXAxis.mNumDays, len(self.mSeries)])-1):
            x1 = self.mXAxis.findX(i)
            x2 = self.mXAxis.findX(i+1)
            y1 = self.mYAxis.findY(self.mSeries[i])
            y2 = self.mYAxis.findY(self.mSeries[i+1])
            pa = QPointArray(4)
            pa.setPoint(0, QPoint(x1,self.mYAxis.findY(self.mYAxis.mMin)))
            pa.setPoint(1, QPoint(x1,y1))
            pa.setPoint(2, QPoint(x2,y2))
            pa.setPoint(3, QPoint(x2,self.mYAxis.findY(self.mYAxis.mMin)))
            p.drawPolygon(pa)

    def UpdateData(self, chartData):
        self.mData = chartData


    def Calculate(self):
        pass
