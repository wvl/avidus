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

class IndicatorChart(Chart):

    def __init__(self, xAxis, chartData, yAxisSize, chartProperties, \
                 parent=None, name='Chart'):
        Chart.__init__(self, xAxis, chartData, yAxisSize, chartProperties, \
                       parent, name)
        self.setMinimumSize(800,50)
        self.setMaximumSize(4000,1000)

        self.IndicatorMap = BottomIndicatorMap

        if not chartData.isEmpty():
            self.UpdateData(chartData)

    def PaintData(self, p):        
        self.PaintIndicators(p)

    def UpdateData(self,chartData):
        self.mData = chartData
        minval = []
        maxval = []
        
        for i in range(len(self.mIndicators)):
            self.mIndicators[i].UpdateData(self.mData)
            self.mIndicators[i].Calculate()
            minval.append(self.mIndicators[i].Min())
            maxval.append(self.mIndicators[i].Max())

        if len(self.mIndicators) > 0:
            self.mY.setRange(min(minval), max(maxval))

        self.repaint(self.rect(), 0)
