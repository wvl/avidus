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

class LastDay(Indicator, Properties):

    def __init__(self, chartData, xAxis, yAxis):
        Indicator.__init__(self, chartData, xAxis, yAxis)
        Properties.__init__(self)
            
        tab = self.buildTab()
        self.addTab(tab[0], tab[1])
        
    def buildTab(self):
        self.tab = QWidget(self)

        self.tab.layout = QGridLayout(self.tab, 1,2, 5,5)

        color_label = QLabel('Color: ', self.tab)
        self.tab.layout.addWidget(color_label,1,0)
        self.cc = ColorCombo(self.tab)
        self.cc.setCurrentColor(self.Ind1Color)
        self.tab.layout.addWidget(self.cc,1,2)

        self.tab.layout.addColSpacing(1,20)

        return self.tab, 'Last Day', self.applyPressed

    def applyPressed(self):
        self.Ind1Color = self.cc.currentColor()
        self.Calculate()

    def updateSMALength(self, val):
        self.length = val


    def Calculate(self):
        if len(self.mData.adate)==0:
            return

        self.c = 'Close:  %6.3f' % self.mData.close[0]
        self.o = 'Open:   %6.3f' % self.mData.open[0]
        self.h = 'High:   %6.3f' % self.mData.high[0]
        self.l = 'Low:    %6.3f' % self.mData.low[0]
        change = self.mData.close[0]-self.mData.close[1]
        percent = change/self.mData.close[1]*100
        self.d = 'Change: %6.3f (%5.2f %%)' % (change, percent)
        
    def Paint(self, widget, p):
        if len(self.mData.adate)==0:
            p.drawText(20,20,'No Data')
            return

        p.setPen(self.Ind1Color)

        ht = 18
        w = 200
        x = self.mXAxis.findX(0) - w - 10
        p.drawText(x,0*ht,w,ht,Qt.AlignmentFlags.AlignLeft,self.c)
        p.drawText(x,1*ht,w,ht,Qt.AlignmentFlags.AlignLeft,self.o)
        p.drawText(x,2*ht,w,ht,Qt.AlignmentFlags.AlignLeft,self.d)
        p.drawText(x,3*ht,w,ht,Qt.AlignmentFlags.AlignLeft,self.h)
        p.drawText(x,4*ht,w,ht,Qt.AlignmentFlags.AlignLeft,self.l)
