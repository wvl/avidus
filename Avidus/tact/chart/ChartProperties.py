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
from Avidus.tact.base.Properties import *
from Avidus.tact.base.StyleCombo import *

class ChartProperties(Properties):
    """ properties for the chart """

    def __init__(self, parent=None, name='Chart Properties'):
        Properties.__init__(self, parent, name)
        #self.colorcombo = ColorCombo(self.vbox)

        self.parent = parent
        self.setCaption('Edit Chart Properties')
        
        self.ChartColors = {'Background Color':Qt.black}
        self.ChartStyles = {}
        self.setDefaults()
        
        #self.cpt = ChartPropertiesTab(self)
        #self.addTab(self.cpt, 'Chart Properties')

        self.externalTabs = {}
        
        self.addColorTab()
        self.addStyleTab()
        
    def setDefaults(self):

        self.ChartColors['Background Color'] = Qt.black
        self.ChartColors['Grid Color'] = Qt.white
        self.ChartColors['Axes Color'] = Qt.white
        self.ChartColors['Price Color'] = Qt.red

        self.ChartStyles['Major Grid'] = 0
        self.ChartStyles['Minor Grid'] = 0
        self.ChartStyles['Major Grid Style'] = Qt.PenStyle.DotLine
        self.ChartStyles['Minor Grid Style'] = Qt.PenStyle.DotLine

    def addExternalTab(self, tab, name, apply):
        self.addTab(tab, name)
        self.externalTabs[name] = apply
        
    def addColorTab(self):

        self.colors = QWidget(self)

        self.colors.layout = QGridLayout(self.colors, 4, 3, 5, 5)
        #self.setMargin(5)
        self.colors.ccs = {}
        
        labels = self.ChartColors.keys()
        values = self.ChartColors.values()
        for i in range(len(self.ChartColors)):
            l = QLabel(labels[i], self.colors)
            self.colors.layout.addWidget(l,i,0)
            cc = ColorCombo(self.colors)
            cc.setCurrentColor(values[i])
            self.colors.layout.addWidget(cc,i,2)
            self.colors.ccs[labels[i]] = cc

        self.colors.layout.addColSpacing(1,20)
        #self.colors.layout.setColStretch(1,5)

        self.addTab(self.colors, 'Colors')
        
    def addStyleTab(self):
        self.styles = QWidget(self)
        self.styles.layout = QGridLayout(self.styles, 2, 4, 5, 5)

        self.MajorGrid = QRadioButton('Major Grid', self.styles)
        self.MajorGrid.setChecked(self.ChartStyles['Major Grid'])
        self.styles.layout.addWidget(self.MajorGrid,0,0) 
        l1 = QLabel('Style', self.styles)
        self.styles.layout.addWidget(l1,0,2)
        self.MajorGridStyle = PenStyleCombo(self.styles)
        self.MajorGridStyle.setCurrentStyle( \
            self.ChartStyles['Major Grid Style'])
        self.styles.layout.addWidget(self.MajorGridStyle,0,3)

        self.MinorGrid = QRadioButton('Minor Grid', self.styles)
        self.MinorGrid.setChecked(self.ChartStyles['Minor Grid'])
        self.styles.layout.addWidget(self.MinorGrid,1,0)
        l2 = QLabel('Style', self.styles)
        self.styles.layout.addWidget(l2,1,2)
        self.MinorGridStyle = PenStyleCombo(self.styles)
        self.MinorGridStyle.setCurrentStyle( \
            self.ChartStyles['Major Grid Style'])
        self.styles.layout.addWidget(self.MinorGridStyle,1,3)

        self.styles.layout.addColSpacing(1,20)
        #self.styles.layout.setColStretch(1,5)

        self.addTab(self.styles, 'Styles')
        

    def applyPressed(self):
        labels = self.colors.ccs.keys()
        values = self.colors.ccs.values()
        for i in range(len(self.colors.ccs)):
            self.ChartColors[labels[i]] = values[i].currentColor()
        self.ChartStyles['Major Grid'] = self.MajorGrid.isChecked()
        self.ChartStyles['Minor Grid'] = self.MinorGrid.isChecked()
        self.ChartStyles['Major Grid Style'] = \
                                self.MajorGridStyle.currentStyle()
        self.ChartStyles['Minor Grid Style'] = \
                                self.MinorGridStyle.currentStyle()
        self.emit(PYSIGNAL('propertiesChanged'), ())


        applies = self.externalTabs.values()
        for i in range(len(self.externalTabs)):
            applies[i]()
            
