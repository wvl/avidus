#!/usr/bin/env python
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
from Avidus.tact.app.MainWindow import *

if __name__=='__main__':
    a = QApplication(sys.argv)
    mw = MainWindow()
    a.setMainWidget(mw)
    mw.setCaption('t a c t')
    mw.show()
    if len(sys.argv) > 1:
        mw.set_ticker(sys.argv[1])
    a.exec_loop()