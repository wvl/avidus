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

class Vol(Indicator, Properties):

    def __init__(self, chartData, xAxis, yAxis):
        Indicator.__init__(self, chartData, xAxis, yAxis)
        Properties.__init__(self)
        
        self.setIndicatorType('filledline')

        tab = self.buildTab()
        self.addTab(tab[0], tab[1])

    def Calculate(self):
        self.mSeries = self.mData.vol

    def buildTab(self):
        self.tab = QWidget(self)

        self.tab.layout = QGridLayout(self.tab, 1, 2, 5,5)

        l1 = QLabel('Color: ', self.tab)
        self.tab.layout.addWidget(l1,0,0)
        self.cc = ColorCombo(self.tab)
        self.cc.setCurrentColor(self.Ind1Color)
        self.tab.layout.addWidget(self.cc,0,2)

        self.tab.layout.addColSpacing(1,20)

        return self.tab, 'Volume', self.applyPressed

    def applyPressed(self):
        self.Ind1Color = self.cc.currentColor()
        self.Calculate()
