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

#!/usr/bin/env python


import shelve
import os
import DateTime

tact_dir = os.path.join(os.environ['HOME'], '.tact')
data_dir = os.path.join(tact_dir, 'data')

def try_or_makedir(dir):
    try:
        os.chdir(dir)
    except:
        os.makedirs(dir)

try_or_makedir(tact_dir)
try_or_makedir(data_dir)

conf_file = os.path.join(tact_dir, 'ds.conf')
db = shelve.open(conf_file)

db['symbols'] = []
date = DateTime.now() - DateTime.RelativeDateTime(years=+3)
db['startdate'] = date

db.close()
