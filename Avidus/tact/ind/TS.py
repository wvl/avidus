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

from Avidus.tact.base.Properties import *
from Indicator import *
from ResultsWindow import *
from Avidus.ind import *
from Avidus.ts import *

class TS(Indicator, Properties):

    def __init__(self, chartData, xAxis, yAxis):
        Indicator.__init__(self, chartData, xAxis, yAxis)
        Properties.__init__(self)
            
        tab = self.buildTab()
        self.addTab(tab[0], tab[1])

        s =  QFileDialog.getOpenFileName( QString.null, \
                                           "*.ts", self)
        self.lineedit.setText(s)
        self.filename = `s`

        self.index = 0

        self.results_window = ResultsWindow()
        
    def Calculate(self):
        self.tsData = []
        run(self.mData, self.filename, \
            self.mXAxis.mNumDays, self.tsData)

        calculateStats(self.mData, self.tsData, self.mXAxis.mNumDays)

        self.results_window.setTradeLog(self.tsData)
        self.results_window.show()
        #self.mSellSeries = self.tsData.sellData
        #self.mBuySeries = self.tsData.buyData
        
    def buildTab(self):
        self.tab = QWidget(self)

        self.tab.layout = QGridLayout(self.tab, 1,2, 3,3)

        file_label = QLabel('File: ', self.tab)
        self.tab.layout.addWidget(file_label, 1, 0)
        self.lineedit = QLineEdit(self.tab)
        self.tab.layout.addWidget(self.lineedit,1,2)
        
        color_label = QLabel('Color: ', self.tab)
        self.tab.layout.addWidget(color_label,3,0)
        self.cc = ColorCombo(self.tab)
        self.cc.setCurrentColor(self.Ind1Color)
        self.tab.layout.addWidget(self.cc,3,2)

        self.tab.layout.addColSpacing(1,20)

        return self.tab, 'TS', self.applyPressed

    def applyPressed(self):
        self.Ind1Color = self.cc.currentColor()
        self.Calculate()

    def Paint(self, widget, p):
        p.setPen(self.Ind1Color)
        w = 5

        for i in range(len(self.tsData)):
            pa = QPointArray(4)

            index = self.mData.indexFromDate(self.tsData[i].date)
            if self.tsData[i].trade == -1:
                h=-5
                y = self.mYAxis.findY(self.mData.high[index])-10
            else:
                h=5 
                y = self.mYAxis.findY(self.mData.low[index])+10
               
            x = self.mXAxis.findX(index)
            pa.setPoint(0,x,y)
            pa.setPoint(1,x+w/2,y+h)
            pa.setPoint(2,x-w/2,y+h)
            pa.setPoint(3,x,y)
            p.drawPolyline(pa)




