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

""" Test program

"""
from DataSet import *

class sma_crossover_system:
    def __init__(self):
        self.open = []
        self.high = []
        self.low = []
        self.close = []

        self.ema_length = 15
        self.exp = 0.2*(10.0/self.ema_length)
        self.input_m1 = 0
        self.bar = 0
        self.var = 0
        
    def ema(self, input):
        if self.bar > self.ema_length:
            self.input_m1 = self.input_m1 + (input-self.input_m1)*self.exp
            return self.input_m1
        elif self.bar < self.ema_length:
            self.input_m1 = self.input_m1 + input
            return 'NULL'
        else:
            self.var = self.var + input
            self.input_m1 =  self.input_m1/self.ema_length
            return self.input_m1
    
    def NewBar(self, open, high, low, close):
        self.bar = self.bar + 1
        self.open.append(open)
        self.high.append(high)
        self.low.append(low)
        self.close.append(close)
        ema = self.ema(close)
        if ema=='NULL':
            return 0
        elif close > ema:
            return 1
        elif close < ema:
            return -1
        else:
            return 'ERROR'

