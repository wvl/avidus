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

from Chart import *
from Avidus.tact.ind import *

class PriceChart(Chart):

    def __init__(self, xAxis, chartData, yAxisSize, chartProperties, \
                 parent=None, name='Chart'):
        Chart.__init__(self, xAxis, chartData, yAxisSize, chartProperties, \
                       parent, name)
        self.setMinimumSize(800,400)
        self.setMaximumSize(4000,2000)
        self.IndicatorMap = TopIndicatorMap

        self.mChartStyle = 'Candle'

    def PaintData(self, p):
        self.PaintTimeSeries(p)
        self.PaintIndicators(p)

    def PaintTimeSeries(self, p):

        if len(self.mData.adate)==0:
            return
        
        p.setPen(self.mProps.ChartColors['Price Color'])

        width = self.mX.findX(0) - self.mX.findX(1)
        ticklength = min([(width/4), 5])
        
        p.setPen(self.mProps.ChartColors['Price Color'])
        b = QBrush(self.mProps.ChartColors['Price Color'])

        p.scale(1,1)

        for i in range(min([self.mX.mNumDays, len(self.mData.adate)])):
            #if self.mData.signal[i] == 1:
            #    p.setPen(Qt.magenta)
            #elif self.mData.signal[i] == -1:
            #    p.setPen(Qt.yellow)
            #else:

            if self.mChartStyle == 'OHLC':
                x1 = self.mX.findX(i)
                x2 = x1
                y1 = self.mY.findY(self.mData.high[i])
                y2 = self.mY.findY(self.mData.low[i])
                p.drawLine(x1,y1,x2,y2)
                
                x2 = x1 - ticklength
                y1 = self.mY.findY(self.mData.open[i])
                y2 = y1
                p.drawLine(x1,y1,x2,y2)
                
                x2 = x1 + ticklength
                y1 = self.mY.findY(self.mData.close[i])
                y2 = y1
                p.drawLine(x1,y1,x2,y2)

            elif self.mChartStyle == 'Candle':
                if self.mData.close[i] >= self.mData.open[i]:
                    open = 1
                    top = self.mY.findY(self.mData.close[i])
                    bottom = self.mY.findY(self.mData.open[i])
                else:
                    open = 0
                    top = self.mY.findY(self.mData.open[i])
                    bottom = self.mY.findY(self.mData.close[i])
                    
                x1 = self.mX.findX(i)
                x2 = x1
                y1 = self.mY.findY(self.mData.high[i])
                y2 = top
                p.drawLine(x1,y1,x2,y2)

                y1 = self.mY.findY(self.mData.low[i])
                y2 = bottom
                p.drawLine(x1,y1,x2,y2)

                x1 = x1 - ticklength
                w = 2*ticklength+1
                h = bottom-top+1
                r = QRect(x1,top,w,h)

                if open:
                    p.drawRect(r)
                else:
                    p.fillRect(r, b)

            elif self.mChartStyle == 'Line':
                if len(self.mData.close) > i+1:
                    x1 = self.mX.findX(i)
                    x2 = self.mX.findX(i+1)
                    y1 = self.mY.findY(self.mData.close[i])
                    y2 = self.mY.findY(self.mData.close[i+1])
                    p.drawLine(x1,y1,x2,y2)

            else:
                raise 'Invalid Chart Style: '+self.mChartStyle
                
        #tmp.setBrush(self.mProps.Ind1Color)
        #tmp.setPen(self.mProps.Ind1Color)
 
    def setChartStyle(self, style):
        self.mChartStyle = style
        if self.mChartStyle == 'Line':
            self.mX.setMinimumPixelsBetweenBars(2)
        else:
            self.mX.setMinimumPixelsBetweenBars(5)
            
        self.repaint(self.rect(),0)
        
    def UpdateData(self,chartData):
        self.mData = chartData
        numbars = self.mX.getNumBars()
        
        self.mY.setRange(self.mData.getMinPrice(numbars), \
                         self.mData.getMaxPrice(numbars))   
        for i in range(len(self.mIndicators)):
            self.mIndicators[i].UpdateData(chartData)
            self.mIndicators[i].Calculate()
        
        self.repaint(self.rect(),0)
