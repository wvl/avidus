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

import sys, string
from TradeAnalysis import *

class SystemTest:
    """ Test environment for trading systems """
    
    def __init__(self, data):
        self.mData = data

        self.Capital = 10000
        self.commission = 20
        self.mNumTrades = 0
        self.trades = TradeAnalysis()
        
    def Test(self, system):
        self.mData.signal.append(0)
        for i in range(len(self.mData.adate)):
            signal = system.NewBar(self.mData.open[i], \
                                   self.mData.high[i], \
                                   self.mData.low[i], \
                                   self.mData.close[i])
            self.mData.signal.append(signal)

        last_signal = 0
        d = self.mData.adate
        c = self.mData.close
        o = self.mData.open
        s = self.mData.signal
        open_pos = 0
        
        for i in range(len(c)):
            if s[i]==last_signal:
                pass
                # do nothing
            elif s[i]==1:
                self.trades.Buy(d[i], o[i])
                last_signal = 1
            elif s[i] == -1:
                self.trades.Sell(d[i], o[i])
                    #self.EvalTrade(open_pos, o[i], 1)
                #open_pos = o[i]
                last_signal = -1
            else:
                self.EvalTrade(open_pos, o[i], -1)
                last_signal = 0
                # should handle this case
            self.mData.capital.append(self.trades.getCapital())

        self.trades.CalcStats()
        self.trades.printme()
        
    def EvalTrade(self, open, close, pos):
        self.mNumTrades = self.mNumTrades + 1
        if self.mNumTrades == 1:
            # ignore first trade
            return
        
        num = math.floor(self.Capital/open)
        #leftover = self.Capital - open*num
        self.Capital = self.Capital + pos*(close-open)*num
        
