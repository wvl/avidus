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
from Avidus.ts import *

class ShowMe(Indicator, Properties):

    def __init__(self, chartData, xAxis, yAxis):
        Indicator.__init__(self, chartData, xAxis, yAxis)
        Properties.__init__(self)
            
        tab = self.buildTab()
        self.addTab(tab[0], tab[1])

        s =  QFileDialog.getOpenFileName( QString.null, \
                                           "*.sm", self)
        self.lineedit.setText(s)
        self.filename = `s`

        self.index = 0
        
    def Calculate(self):
        self.tsData = []
        run(self.mData, self.filename, self.mXAxis.mNumDays, \
            self.tsData)
        
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

        return self.tab, 'ShowMe', self.applyPressed

    def applyPressed(self):
        self.Ind1Color = self.cc.currentColor()
        self.Calculate()

    def Paint(self, widget, p):
        p.setPen(self.Ind1Color)
        for i in range(len(self.tsData)):
            w = 5
            h = 5
            #index = self.mData.indexFromDate(self.tsData[i].date)
            index = self.tsData[i]
            x = self.mXAxis.findX(index)-(w/2)
            y = self.mYAxis.findY(self.mData.high[index])-10-(h/2)
            p.drawArc(x,y,w,h,5760,5760)
