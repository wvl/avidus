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

import sys,string
from qt import *
from Avidus.tact.chart.PriceChart import *
from Avidus.tact.chart.IndicatorChart import *
from Avidus.tact.chart.XAxis import *
from Avidus.tact.chart.ChartProperties import *
from Avidus.base.DataSet import *
import Avidus.ds

class ChartWindow(QScrollView):
    """ the chart window manages the main window level charts """
    def __init__(self, parent=None, name='Chart Window'):
        """ Constructor """
        
        QScrollView.__init__(self, parent, name)

        #fixme: for some reason, the following statement throws
        #error output, but still seems to work....
        self.setMinimumSize(800,600)

        self.xsize = self.width()
        self.mYAxisSize = 60

        self.chartStyle = ['OHLC', 'Candle', 'Line']
        self.timeScale = [('3 Months',80), \
                          ('1 Year',260), \
                          ('2 Years',520), \
                          ('3 Years',780)]
        #self.numberOfBars = 80
        
        self.mData = DataSet()
        self.mProps = ChartProperties(self)
        self.connect(self.mProps, \
                     PYSIGNAL('propertiesChanged'), self.redraw)

        self.mIndCharts = []
        self.mNumIndCharts = 0
        self.mMaxNumIndCharts = 5
        
        self.setHScrollBarMode(QScrollView.ScrollBarMode.AlwaysOn)
        self.setVScrollBarMode(QScrollView.ScrollBarMode.AlwaysOff)
        self.splitter = QSplitter(Qt.Orientation.Vertical, self.viewport())
        self.addChild(self.splitter,0,0)

        #X Axis
        self.mX = XAxis(self.mData, self.mYAxisSize, self.mProps, \
                        self.splitter, 'XAxis')
        self.splitter.setResizeMode(self.mX, \
                                    QSplitter.ResizeMode.Stretch)
        

        # Price Chart
        self.mChart = PriceChart(self.mX, self.mData, \
                                 self.mYAxisSize, self.mProps,  \
                                 self.splitter, 'Main Chart')
        #self.splitter.setResizeMode(self.mChart, \
        #                            QSplitter.ResizeMode.FollowSizeHint)

        self.splitter.moveToLast(self.mX)

        #self.mChart.AddThisIndicator('SMA')

        #for i in range(self.mMaxNumIndCharts):
        #    indchart = IndicatorChart(self.mX, self.mData, \
        #                              self.mYAxisSize, \
        #                              self.mProps, \
        #                              self.splitter, 'Indicator Chart')
            #self.splitter.setResizeMode(indchart, \
            #                            QSplitter.ResizeMode.Stretch)
        #    indchart.hide()
        #    self.mIndCharts.append(indchart)

        self.newIndicatorChart('Volume')

        self.symbols = Avidus.ds.listSymbols()
        self.symbol_index = -1

        #print 'Splitter height: ', self.splitter.height(), self.height()
        #self.splitter.resize(self.width(), self.height())
        
        
    def redraw(self):
        self.repaint(self.rect(), 0)

    def newChart(self):
        self.newIndicatorChart('Volume')

    def newIndicatorChart(self, indicator):
        indchart = IndicatorChart(self.mX, self.mData, \
                                  self.mYAxisSize, \
                                  self.mProps, \
                                  self.splitter, 'Indicator Chart')
        self.splitter.setResizeMode(indchart, \
                                    QSplitter.ResizeMode.Stretch)
        
        self.mIndCharts.append(indchart)
        
        if self.mNumIndCharts >= self.mMaxNumIndCharts:
            message = 'Too many Charts'
            self.emit(PYSIGNAL("statusMessage"), (message,))
            QMessageBox.information(self, 't a c t',
                                    message)
            return
        
        self.mIndCharts[self.mNumIndCharts].AddThisIndicator(indicator,0)
        
        self.splitter.moveToLast(self.mX)
        
        self.resizeContents(self.xsize, self.visibleHeight())
        self.splitter.resize(self.xsize, self.visibleHeight())
        self.mIndCharts[self.mNumIndCharts].show()
        self.mNumIndCharts = self.mNumIndCharts + 1

    def setToolBarWidgets(self,ticker,chartstyle, timescale):
        self.ticker = ticker
        self.chartStyleCombo = chartstyle
        self.timeScaleCombo = timescale

    def resizeEvent(self, resizeEvent):
        self.resize()

    def resize(self):
        self.xsize = self.mX.setDateRange(self.visibleWidth())
        #print 'resize: ', self.xsize,  self.width(), self.height(), \
        #      self.visibleWidth(), self.visibleHeight()
        #self.splitter.resize(self.xsize, self.visibleHeight())
        #fixme: hack, this should look like above!
        if self.xsize < (self.width()-4):
            self.xsize = self.width() - 4
        self.splitter.resize(self.xsize, self.height()-20)
        
    def left(self):
        if self.symbol_index <= 0:
            return

        self.symbol_index = self.symbol_index - 1
        symbol = self.symbols[self.symbol_index]
        self.ticker.setCurrentItem(0)
        self.loadSymbol(symbol)
        
    def right(self):
        if self.symbol_index >= (len(self.symbols) - 1):
            return

        self.symbol_index = self.symbol_index + 1
        symbol = self.symbols[self.symbol_index]
        #self.ticker.insertItem(symbol)
        self.ticker.setCurrentItem(0)
        self.loadSymbol(symbol)

    def selectChartStyle(self, style):
        chartstyle = self.chartStyleCombo.currentText().ascii()
        self.mChart.setChartStyle(chartstyle)

    def selectTimeScale(self, scale):
        length = self.timeScaleCombo.currentText().ascii()
        for i in range(len(self.timeScale)):
            if length == self.timeScale[i][0]:
                self.mX.setNumBars(self.timeScale[i][1])

        if self.mData.symbol != '':
            self.loadSymbol(self.mData.symbol)

        
    def LoadTicker(self, ticker):
        symbol = self.ticker.currentText().ascii()
        for i in range(len(self.symbols)):
            if self.symbols[i] == symbol:
                self.symbol_index = i
                
        self.loadSymbol(symbol)

    def loadSymbol(self, symbol):
        if Avidus.ds.hasSymbol(symbol):
            import DateTime
            date = DateTime.now() - DateTime.RelativeDate(years=+5)
            self.mData.setData(Avidus.ds.getData(symbol, date), symbol)
        else:
            message = 'Invalid symbol'
            self.emit(PYSIGNAL("statusMessage"), (message,))
            QMessageBox.information(self, 't a c t',
               """Invalid Symbol""")
            return
        
        self.xsize = self.mX.UpdateData(self.mData,self.width())

        
        if self.splitter.width() != self.xsize:
            self.mChart.UpdateData(DataSet())
            for i in range(len(self.mIndCharts)):
                self.mIndCharts[i].UpdateData(DataSet())
            self.resizeContents(self.xsize, self.visibleHeight())
            self.splitter.resize(self.xsize, self.visibleHeight())
            
            # move to the far right
            self.center(4000,0,0,0)
            
        #print 'got a size of: ', self.width(), self.height()
        #print 'got a size of: ', self.mChart.width(), self.mChart.height()
        #print 'got a size of: ', self.splitter.width(), self.splitter.height()
        
        self.mChart.UpdateData(self.mData)
        for i in range(len(self.mIndCharts)):
            self.mIndCharts[i].UpdateData(self.mData)

        # move to the far right
        self.center(4000,0,0,0)
        
        message = symbol + ' loaded.'
        self.emit(PYSIGNAL("statusMessage"), (message,))

        self.ticker.insertItem(symbol,0)
        
    def editProperties(self):
        self.mProps.show()
        self.repaint(self.rect(),0)

    def XAxisRect(self):
        r = QRect(0,0,self.width() - self.mYAxisSize, self.mXAxisSize)
        r.moveBottomLeft(self.rect().bottomLeft())
        return r
