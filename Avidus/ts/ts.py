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

import string, math
import DateTime
import Numeric
#from Avidus.base.DataSet import *

class TradeData:
    """ TradeData - used as a struct """
    
    def __init__(self, _price=0, _date=None, _trade=0, \
                 _ticker='', _num=0):
        self.ticker = _ticker
        self.date = _date
        self.trade = _trade
        self.num = _num
        self.price = _price

    
# Global Data

# Series of TradeData
tsData = None

# Data used for backtest
Data = None

# index used to calculate location in backtest
ts_index = []

# Map of name/value for any pre calculated series.
series = {}

# Current Market Position (1 long, -1 short, 0 no position)
marketposition = 0

buy_market = 0
sell_market = 0

def init(data, tsd):
    """ Initialize the global data """
    
    global tsData
    global Data
    tsData = tsd
    Data = data

    global ts_index
    ts_index = []
    series.clear()

    global marketposition
    global buy_market
    global sell_market

    marketposition = 0
    buy_market = 0
    sell_market = 0
    
def run(data, filename, numDays, tsd):
    """ Backtest the trading system

    Backtest the trading system given by the input filename,
    over the last numDays of data.  This procedure stores the
    trade log as an array of TradeData.

    """

    init(data, tsd)


    calcfile = open(filename, 'r')
    calcbuf = calcfile.read()

    # split the file into init and main
    splitbuf = string.split(calcbuf, '---')

    if len(splitbuf) > 1: 
        calclines = string.split(splitbuf[1], '\n')
        initlines = string.split(splitbuf[0], '\n')

        # run the initialization code....
        initcontent = 'from Avidus.ts import *\n\n' \
                + 'def initVars(open, high, low, close, vol):\n' \
                +  '\tfrom Avidus.ind import *\n' 

        for i in range(len(initlines)):
            initcontent = initcontent + '\t' + initlines[i] + '\n'
        exec(initcontent)
        initVars(data.open, data.high, \
             data.low, data.close, \
             data.vol)

    else:
        calclines = string.split(splitbuf[0], '\n')

    contents = 'from Avidus.ts import *\n\n' \
           + 'def calc(open, high, low, close, vol, series):\n' \
             +  '\tfrom Avidus.ind import *\n' 

    # Add the code so that input series can be sliced, AND
    # referenced by name in the TS code
    k = series.keys()
    for i in range(len(k)):
        contents = contents + \
                   '\texec("'+k[i]+' = series[\''+\
                   k[i]+'\']")\n'

    # Add the user code, prefixed with a tab
    for i in range(len(calclines)):
        contents = contents + '\t' + calclines[i] + '\n'

    exec(contents)

    # Start from oldest bar and go forward
    r = range(min([numDays, len(data.adate)]))
    r.reverse()

    # go over each bar
    for index in r:
        global ts_index
        ts_index.append(index)
        k = series.keys()
        ser = {}
        for i in range(len(k)):
            ser[k[i]] = series[k[i]][index:]

        # Execute any outstanding trades
        execute(data.open[index:], \
             data.high[index:], \
             data.low[index:], \
             data.close[index:], \
             data.vol[index:])

        # Run the TS code, to generate signals/data
        calc(data.open[index:], \
             data.high[index:], \
             data.low[index:], \
             data.close[index:], \
             data.vol[index:],
             ser)

def execute(open, high, low, close, vol):
    """ Execute on any outstanding orders """

    global tsData
    global Data
    global buy_market
    global sell_market
    global ts_index
    global marketposition
    
    if buy_market == 1:
        marketposition = 1
        buy_market = 0
        
        i = ts_index[-1]

        # Buy at open 
        td = TradeData(Data.open[i], Data.adate[i], 1, Data.symbol)
        tsData.append(td)

    if sell_market == 1:
        if marketposition == 1:
            marketposition = 0
        else:
            marketposition = -1
        sell_market = 0
        
        i = ts_index[-1]

        # Sell at open
        td = TradeData(Data.open[i], Data.adate[i], -1, Data.symbol)
        tsData.append(td)

#
# TS Procs
# 
def Input(name, value, low=None, high=None, step=None):
    pass


def Series(name, value):
    series[name] = value
            
def showme():
    global tsData

    tsData.append(ts_index[-1])

def buy():
    global buy_market

    buy_market = 1
    

def buyStop(val):
    pass

def buyLimit(val):
    pass

def sell():
    global marketposition
    global tsData
    global Data

    marketposition = - 1
    i = ts_index[-1] - 1   # the next bar
    if i >= 0:
        td = TradeData(Data.open[i], Data.adate[i], -1, Data.symbol)
        tsData.append(td)

def sellStop(val):
    pass

def sellLimit(val):
    pass

def exitLong():
    global sell_market
    global marketposition
    
    if marketposition == 1:
        sell_market = 1
        

def exitLongStop(val):
    pass

def exitLongLimit(val):
    pass

def exitShort(val):
    pass

def exitShortStop(val):
    pass

def exitShortLimit(val):
    pass

#
# Utility Procs
#

# if s1 crosses over s2, then return true, else return false
def crossesOver(s1, s2):
    if len(s1) < 2 or len(s2) < 2:
        return 0
    
    if s1[0] > s2[0]:
        if s1[1] <= s2[1]:
            return 1

    return 0
