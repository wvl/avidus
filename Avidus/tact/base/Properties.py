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
        
class Properties(QTabDialog):
    """ base class for properties """

    def __init__(self, parent=None, name='Chart Properties', modal=1):
        QTabDialog.__init__(self, parent, name, modal)

        self.setCancelButton()
        self.setDefaultButton('Apply')
        
        #self.tab1 = QVBox(self)
        #self.tab1.setMargin(5)
        #l = QLabel('this is a label', self.tab1)
        
        #self.addTab(self.tab1, 'Tab 1')

        self.connect(self, SIGNAL('applyButtonPressed()'), \
                     self.applyPressed)
        self.connect(self, SIGNAL('defaultButtonPressed()'), \
                     self.applyPressed)
        self.connect(self, SIGNAL('cancelButtonPressed()'), \
                     self.reject)

    def editProperties(self):
        self.show()
        
    def applyPressed(self):
        print 'Apply pressed'

    #def reject(self):
    #    print 'cancel pressed'
        
    def resizeEvent(self, resizeEvent):
        #self.vbox.resize(self.width(), self.height())
        pass
    
    def setDefaults(self):
        pass
