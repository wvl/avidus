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
from Avidus.ind import *

class Capital(Indicator, Properties):

    def __init__(self, chartData, xAxis, yAxis):
        Indicator.__init__(self, chartData, xAxis, yAxis)
        Properties.__init__(self)
            
        #self.setIndicatorType('line')        

        tab = self.buildTab()
        self.addTab(tab[0], tab[1])
        
    def Calculate(self):
        self.mSeries = self.mData.pl
        #self.mSeries = []
        #for i in range(len(self.mData.capital)):
        #    self.mSeries.append(self.mData.capital[i][0])

    
    def buildTab(self):
        self.tab = QWidget(self)

        self.tab.layout = QGridLayout(self.tab, 1,2, 5,5)

        color_label = QLabel('Color: ', self.tab)
        self.tab.layout.addWidget(color_label,1,0)
        self.cc = ColorCombo(self.tab)
        self.cc.setCurrentColor(self.Ind1Color)
        self.tab.layout.addWidget(self.cc,1,2)

        self.tab.layout.addColSpacing(1,20)

        return self.tab, 'Capital', self.applyPressed

    def applyPressed(self):
        self.Ind1Color = self.cc.currentColor()
        self.Calculate()


    def Paint(self, widget, p):
        p.setPen(self.Ind1Color)
        for i in range(len(self.mData.capital)-1):
            index1 = self.mData.indexFromDate(self.mData.capital[i][1])
            x1 = self.mXAxis.findX(index1)
            index2 = self.mData.indexFromDate(self.mData.capital[i+1][1])
            x2 = self.mXAxis.findX(index2)
            y1 = self.mYAxis.findY(self.mData.capital[i][0])
            y2 = self.mYAxis.findY(self.mData.capital[i+1][0])
            p.drawLine(x1,y1,x2,y2)                      

        p.setPen(self.Ind2Color)
        for i in range(min([self.mXAxis.mNumDays, len(self.mSeries)])-1):
            x1 = self.mXAxis.findX(i)
            x2 = self.mXAxis.findX(i+1)
            y1 = self.mYAxis.findY(self.mSeries[i])
            y2 = self.mYAxis.findY(self.mSeries[i+1])
            p.drawLine(x1,y1,x2,y2)
