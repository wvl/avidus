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
import time
from Numeric import *

def sma(input, length):

    if length==0:
        raise 'Cannot have a MA length of 0'

    if len(input)==0:
        return []

    num = len(input)

    if num <= length:
        return []
    
    var = input[0:num-length]
    for i in range(1, length):
        var = var + input[i:num+i-length]
    out= var/length
    return out
    
def ema(input, length):
    
    if length==0:
        raise 'Cannot have a MA length of 0'
    
    if len(input)==0:
        return []

    exp = 2.0/(length+1.0)
    #exp = 0.2*(10/length)

    #fixme: ema too slow!
    num = len(input)

    if num <= length:
        return []

    numlength = num-length
    out = array(zeros(numlength+1),Float)
    
    var = sum(input[numlength:num])
    
    out[numlength] = var/length
    for i in range(1,numlength+1):
        out[numlength-i] = out[numlength-i+1]*(1-exp) + input[numlength-i]*exp

    return out

def macd(input, long=26, short=14, signal_length=9):
    if len(input) == 0:
        return [],[]

    if long <= short:
        raise 'MACD calculation: Long must be larger than Short'
    
    ema_l = ema(input, long)
    ema_s = ema(input, short)

    out = ema_l - ema_s[0:len(ema_l)]
    signal = ema(out, signal_length)

    return out, signal

