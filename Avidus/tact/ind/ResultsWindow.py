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

from qt import *

class TradeLogTable(QMultiLineEdit):
    def __init__(self, parent=None):
        QMultiLineEdit.__init__(self, parent)

    def setTradeLog(self, tl):
        self.clear()
        self.insertLine(' Date - Trade - Price ')
        for i in range(len(tl)):
            d = tl[i].date
            if tl[i].trade == 1:
                pos = 'Buy'
            else:
                pos = 'Sell'
            price = tl[i].price

            line = str(d) + ' - ' + pos + ' - ' + `price`
            self.insertLine(line)
        

class ResultsWindow(QFrame):
    def __init__(self, parent=None, name='Results Window'):
        QFrame.__init__(self, parent, name)

        self.setMinimumSize(400,300)
        self.vbox = QVBox(self)
        self.tab = ResultsTabWidget(self.vbox)
        self.dismiss = QPushButton('Dismiss', self.vbox)
        self.vbox.setGeometry(0,0,self.width(), self.height())

        self.connect(self.dismiss, SIGNAL("clicked()"), \
                     self.hide)
        
    def setTradeLog(self, tl):
        self.tab.setTradeLog(tl)
        
class ResultsTabWidget(QTabWidget):
    def __init__(self, parent=None, name='Results Tab Widget'):
        QTabWidget.__init__(self, parent, name)

        self.setTabPosition(1)
        self.buildTradeLogPage()
        self.buildStatsPage()


    def buildStatsPage(self):
        self.stats = QWidget(self)
        self.stats_layout = QGridLayout(self.stats, 1, 2, 3, 3)
        label = QLabel('Test Stat: ', self.stats)
        self.stats_layout.addWidget(label, 1, 0)
        self.addTab(self.stats, 'Stats')
        

    def buildTradeLogPage(self):
        self.table = TradeLogTable(self)
        self.addTab(self.table, 'Trade Log')        

    def setTradeLog(self, tradelog):
        self.table.setTradeLog(tradelog)
