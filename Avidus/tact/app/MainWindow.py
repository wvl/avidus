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
from ChartWindow import * 

arrow_left = [
"16 14 6 1",
"       c None",
".      c #FFFFFF",
"+      c #4366FF",
"@      c #002CF0",
"#      c #001EA2",
"$      c #000000",
"        $       ",
"       +$       ",
"      +@$       ",
"    $+@@$       ",
"   $#@@@$$$$$$$ ",
"  $#@@@@@@@@@@+ ",
" $#@@@@@@@@@@@+ ",
" $#@@@@@@@@@@@+ ",
"  $#@@@@@@@@@@+ ",
"   $#@@@######+ ",
"    $+@@$       ",
"      +@$       ",
"       +$       ",
"        $       "
]

arrow_right = [
"16 14 6 1",
"       c None",
".      c #FFFFFF",
"+      c #4366FF",
"@      c #002DF2",
"#      c #001EA2",
"$      c #000000",
"       $        ",
"       $+       ",
"       $@+      ",
"       $@@+$    ",
" $$$$$$$@@@#$   ",
" +@@@@@@@@@@#$  ",
" +@@@@@@@@@@@#$ ",
" +@@@@@@@@@@@#$ ",
" +@@@@@@@@@@#$  ",
" +######@@@#$   ",
"       $@@+$    ",
"       $@+      ",
"       $+       ",
"       $        "
]

class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, None, 'chart main',
                             Qt.WDestructiveClose)

        # Create the chart window
        self.mw = ChartWindow(self)

        # Menu Bar
        self.file = QPopupMenu(self)
        self.menuBar().insertItem('&File', self.file)
        self.file.insertItem('&Quit', qApp.closeAllWindows,
                             Qt.CTRL+Qt.Key_Q)

        self.edit = QPopupMenu(self)
        self.menuBar().insertItem('&Edit', self.edit)
        self.edit.insertItem('&Add Indicator', self.mw.mChart.AddIndicator)
        self.edit.insertItem('&New Indicator', self.mw.newChart)
        self.edit.insertItem('&Properties', self.mw.editProperties,
                             Qt.ALT+Qt.Key_P)
        
        self.help = QPopupMenu(self)
        self.menuBar().insertItem('&Help', self.help)
        self.help.insertItem('&About', self.about, Qt.Key_F1)

        # Tool Bar
        self.toolbar = QToolBar(self, 'toolbar')
        self.ticker = QComboBox(1, self.toolbar, 'ticker')

        #self.toolbar.insertSeparator()
        
        leftIcon = QPixmap(arrow_left)
        self.rightArrow = QToolButton(leftIcon, 'Next', QString.null, \
                                self.mw.left, self.toolbar, 'Next')

        rightIcon = QPixmap(arrow_right)
        self.rightArrow = QToolButton(rightIcon, 'Next', QString.null, \
                                self.mw.right, self.toolbar, 'Next')

        self.selectChartStyle = QComboBox(self.toolbar, 'Chart Style')
        for i in range(len(self.mw.chartStyle)):
            self.selectChartStyle.insertItem(self.mw.chartStyle[i])
        self.selectChartStyle.setCurrentItem(1)
        self.connect(self.selectChartStyle, SIGNAL("activated(int)"), \
                     self.mw.selectChartStyle)

        self.selectTimeScale = QComboBox(self.toolbar, 'Time Scale')
        for i in range(len(self.mw.timeScale)):
            self.selectTimeScale.insertItem(self.mw.timeScale[i][0])
        self.connect(self.selectTimeScale, SIGNAL('activated(int)'),
                     self.mw.selectTimeScale)
        self.selectTimeScale.setCurrentItem(0)
        
        # Central Widget
        self.mw.setGeometry(100,100,500,355)
        self.connect(self.ticker, SIGNAL('activated(int)'),
                     self.mw.LoadTicker)
        self.mw.setToolBarWidgets(self.ticker, \
                                  self.selectChartStyle, \
                                  self.selectTimeScale)
        self.setCentralWidget(self.mw)

        # Status Bar
        self.connect(self.mw, PYSIGNAL("statusMessage"), self.displayMessage)
        self.statusBar().message('Ready',2000)

    def displayMessage(self, val):
        self.statusBar().message(str(val))
        
    def about(self):
        QMessageBox.about(self, 't a c t',
          """t a c t - Technical Analysis and Charting Tool
          
             Copyright (c) Wayne Larsen""")

    def set_ticker(self, ticker):
        self.ticker.insertItem(ticker)
        self.mw.LoadTicker(self.ticker)
