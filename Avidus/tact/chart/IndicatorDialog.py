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

class IndicatorDialog(QDialog):
    def __init__(self, ind_map, parent=None, name='Chart'):
        QDialog.__init__(self, parent, name)

        self.IndicatorMap = ind_map
        
        self.setMinimumSize(200,200)
        self.layout = QVBoxLayout(self)

        ind_names = self.IndicatorMap.keys()
        self.listbox = QListBox(self, 'listbox')
        for i in range(len(ind_names)):
            self.listbox.insertItem(ind_names[i])
        self.layout.addWidget(self.listbox)

        self.edit = QPushButton('Edit Indicator', self)
        self.layout.addWidget(self.edit)
        self.connect(self.edit, SIGNAL('clicked()'), \
                     self.editPressed)
        
        self.butbox = QHBoxLayout(self.layout)
        self.ok = QPushButton("OK", self)
        self.butbox.addStretch(10)
        self.butbox.addWidget(self.ok)
        self.connect(self.ok, SIGNAL('clicked()'), self.okPressed)
        self.cancel = QPushButton("Cancel", self)
        self.butbox.addWidget(self.cancel)
        self.connect(self.cancel, SIGNAL('clicked()'), self, SLOT('reject()'))

    def okPressed(self):
        self.emit(PYSIGNAL('addIndicator'), \
                  (self.listbox.text(self.listbox.currentItem()).ascii(),))
        self.accept()

    def editPressed(self):
        self.emit(PYSIGNAL('editIndProperties'), \
                  (self.listbox.text(self.listbox.currentItem()).ascii(),)) 
