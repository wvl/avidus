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
from YAxis import *
from IndicatorDialog import *
from Avidus.tact.ind import *

class Chart(QWidget):
    """ Chart - charts something """

    def __init__(self, xAxis, chartData, yAxisSize, chartProperties, \
                 parent=None, name='Chart'):
        """ constructor """
        QWidget.__init__(self, parent, name)

        self.setMinimumSize(400,30)
        
        self.IndicatorMap = IndicatorMap
        self.mX = xAxis
        
        self.mYAxisSize = yAxisSize
        self.mY = YAxis(chartProperties, self.YAxisRect())
        self.mIndicators = []

        self.UpdateData(chartData)

        self.mProps = chartProperties
        self.setProperties()

        self.connect(self.mProps, PYSIGNAL('propertiesChanged'), self.redraw)

        self.setMouseTracking(1)

        self.redraw()

    def redraw(self):
        self.setBackgroundColor(self.mProps.ChartColors['Background Color'])
        self.repaint(self.rect(),0)

    def editProperties(self):
        self.mProps.show()
        self.repaint(self.rect(),0)

    def setProperties(self):
        #self.setPalette(QPalette(QColor(250,250,220)))
        self.setMinimumSize(800,600)
        self.setMaximumSize(1600,1200)

    def AppendIndicator(self, ind):
        self.mIndicators.append(ind)
        
    def AddIndicator(self):
        self.indd = IndicatorDialog(self.IndicatorMap, self)
        self.connect(self.indd, PYSIGNAL('addIndicator'), \
                     self.AddThisIndicator)
        self.connect(self.indd, PYSIGNAL('editIndProperties'),
                     self.EditThisIndicator)
        self.indd.show()

    def EditThisIndicator(self, ind):
        newind = self.IndicatorMap[ind](self.mData, self.mX, self.mY)
        newind.editProperties()
    
    def AddThisIndicator(self, ind, edit=1):
        newind = self.IndicatorMap[ind](self.mData, self.mX, self.mY)
        if edit:
            newind.editProperties()
        self.mIndicators.append(newind)
        tab = newind.buildTab()
        self.mProps.addExternalTab(tab[0], tab[1], tab[2])
        self.UpdateData(self.mData)
        
        #params = self.newindprop.IndicatorMap[ind][1]
        #print 'Adding ', ind, ' now: ', params[1]
        #newind = Indicator(self.mData, self.newindprop, \
        #                  self.mX, self.mY, ind,
        #                   self.newindprop.IndicatorMap[ind][2])
        #self.mIndicators.append(newind)
        #self.UpdateData(self.mData)
        
    def AddTradeSystem(self):
        #s =  QFileDialog.getOpenFileName( QString.null, \
                                          # "*.ts", self)
        #print 'Got file: ', `s`
        self.AddThisIndicator('Trade System')
   
    def AddShowMeStudy(self):
        self.AddThisIndicator('ShowMe')
        
    def setXAxis(self, xAxis):
        self.mX = xAxis
        
 
    def YAxisRect(self):
        r = QRect(0,0,self.mYAxisSize, self.height())
        r.moveTopRight(self.rect().topRight())
        return r

    def DataRect(self):
        r = QRect(0,0,self.width() - self.mYAxisSize, \
                  self.height())
        return r
    
    def paintEvent(self,e):
        updateR = e.rect()
        if updateR.intersects(self.YAxisRect()):
            p = QPainter()
            p.begin(self)
            p.eraseRect(self.YAxisRect())
            p.translate(self.width()-self.mYAxisSize, 0)
            self.mY.PaintYAxis(self, p)
            p.end()
        if updateR.intersects(self.DataRect()):
            p = QPainter()
            p.begin(self)

            dr = self.DataRect()
            pix = QPixmap(dr.size())
            tmp = QPainter()
            pix.fill(self, dr.topLeft())
            tmp.begin(pix)

            self.PaintGrid(tmp)
            self.PaintData(tmp)
            
            tmp.end()
            p.drawPixmap(dr.topLeft(), pix)
            
            p.end()

    def PaintGrid(self, p):
        if self.mProps.ChartStyles['Major Grid']:
            p.setPen(QPen(self.mProps.ChartColors['Grid Color'], 0, \
                          self.mProps.ChartStyles['Major Grid Style']))
            for i in range(len(self.mX.mMajorTicks)):
                x1 = self.mX.findX(self.mX.mMajorTicks[i])
                p.drawLine(x1,0,x1,self.height())

            for i in range(len(self.mY.mMaxRange)):
                y1 = self.mY.findY(self.mY.mMaxRange[i])
                p.drawLine(0,y1,self.DataRect().width(), y1)

        if self.mProps.ChartStyles['Minor Grid']:
            p.setPen(QPen(self.mProps.ChartColors['Grid Color'], 0, \
                          self.mProps.ChartStyles['Minor Grid Style']))
            for i in range(len(self.mX.mMinorTicks)):
                x1 = self.mX.findX(self.mX.mMinorTicks[i])
                p.drawLine(x1,0,x1,self.height())

            for i in range(len(self.mY.mMinRange)):
                y1 = self.mY.findY(self.mY.mMinRange[i])
                p.drawLine(0,y1,self.DataRect().width(), y1)

            
    def PaintIndicators(self, p):
        for i in range(len(self.mIndicators)):
            self.mIndicators[i].Paint(self, p)

    def resizeEvent(self,resizeEvent):
        self.mY.resize(self.YAxisRect())
        self.repaint(self.rect(),0)


    def UpdateData(self, chartData):
        pass

        
    def mousePressEvent(self, e):
       if e.button() == Qt.RightButton:
           options = QPopupMenu(self)
           i = options.insertItem('Add Indicator', \
                                  self.AddIndicator)
           options.insertSeparator(i)
           i = options.insertItem('PaintMe Study', None)
           i = options.insertItem('ShowMe Study', \
                                  self.AddShowMeStudy)
           i = options.insertItem('Trade System', \
                                  self.AddTradeSystem)
           options.insertSeparator(i)
           i = options.insertItem('Edit Properties', self.editProperties)
           options.exec_loop(QCursor.pos())

 
    def mouseMoveEvent(self, e):
        if len(self.mData.adate) > 0:
            i = int(self.mX.findXindex(e.pos().x()))
            #message = self.mData.adate[i].strftime("%y-%m-%d") + \
            #          ' O: '+`self.mData.open[i]`+ \
            #          ' H: '+`self.mData.high[i]`+ \
            #          ' L: '+`self.mData.low[i]`+ \
            #          ' C: '+`self.mData.close[i]`+ \
            #          ' V: '+`self.mData.vol[i]`
            #print message
            #self.emit(PYSIGNAL("statusMessage"), (message,))
    
