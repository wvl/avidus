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

class EMA(Indicator, Properties):

    def __init__(self, chartData, xAxis, yAxis):
        Indicator.__init__(self, chartData, xAxis, yAxis)
        Properties.__init__(self)
            
        self.setIndicatorType('line')        
        self.length = 30

        tab = self.buildTab()
        self.addTab(tab[0], tab[1])
        
    def Calculate(self):
        self.mSeries = ema(self.mData.close, self.length)
    
    def buildTab(self):
        self.tab = QWidget(self)

        self.tab.layout = QGridLayout(self.tab, 1,2, 5,5)


        l1 = QLabel('Length: ', self.tab)
        self.tab.layout.addWidget(l1,0,0)

        self.length_spinbox = QSpinBox(0,300,1,self.tab)
        self.length_spinbox.setValue(self.length)

        self.tab.layout.addWidget(self.length_spinbox,0,2)

        color_label = QLabel('Color: ', self.tab)
        self.tab.layout.addWidget(color_label,1,0)
        self.cc = ColorCombo(self.tab)
        self.cc.setCurrentColor(self.Ind1Color)
        self.tab.layout.addWidget(self.cc,1,2)

        self.tab.layout.addColSpacing(1,20)

        self.connect(self.length_spinbox, SIGNAL('valueChanged(int)'), \
                     self.updateEMALength)
        return self.tab, 'EMA', self.applyPressed

    def applyPressed(self):
        self.Ind1Color = self.cc.currentColor()
        self.length = self.length_spinbox.value()
        self.Calculate()

    def updateEMALength(self, val):
        self.length = val
