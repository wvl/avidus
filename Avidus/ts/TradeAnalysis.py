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
import math

class TradeAnalysis:
    def __init__(self):
        self.open_date = []
        self.open_price = []
        self.position = []
        self.close_date = []
        self.close_price = []
        self.trade_amount = []
        self.trade_percent = []
        self.cum_amount = []
        self.cum_percent = []
        self.num_trades = 0

        self.total_longs = 0
        self.total_shorts = 0
        self.profitable_longs = 0
        self.profitable_shorts = 0
        self.biggest_gain = 0
        self.biggest_loss = 0
        self.successive_gains = 0
        self.successive_losses = 0
        self.total_gain = 0
        self.average_gain = 0
        self.total_gain_p = 0
        
        self.shorts_allowed = 0
        self.starting_capital = 10000
        self.capital = self.starting_capital
        self.commission = 20
        self.cur_pos = 0

    def pd(self, date):
        print date.year, '-', date.month, '-', date.day
        
    def printme(self):
        print 'Trading System Summary'
        print 80*'-'
        for i in range(self.num_trades):
            od = self.open_date[i]
            cd = self.close_date[i]
            print '%4d-%2d-%2d %7.3f %2d %4d-%2d-%2d %7.3f %8.2f %6.2f %8.2f %6.2f ' % \
                  (od.year, od.month, od.day, self.open_price[i], \
                   self.position[i], \
                   cd.year, cd.month, cd.day, self.close_price[i], \
                   self.trade_amount[i], self.trade_percent[i], \
                   self.cum_amount[i], self.cum_percent[i])

        print 80*'-'
        print 'Total Longs:      ', self.total_longs
        print 'Profitable Longs: %7.2f' % self.profitable_longs
        print 'Biggest Gain:     %8.2f' % self.biggest_gain
        print 'Successive Gains: ', self.successive_gains
        print 'Average Gain:     %8.2f' % self.average_gain
        print 'Total Gain:       %8.2f' % self.total_gain
        print 'Total Gain:       %7.2f'  % self.total_gain_p
        print 80*'-'
            

            
    def Buy(self, date, price):
        if self.shorts_allowed:
            if self.cur_pos == -1:
                self.close_date.append(date)
                self.close_price.append(price)        
                self.new_capital = self.capital + self.cur_pos * \
                                   (price - \
                                    self.open_price[len(self.open_price)-1]) \
                                    *self.num - 2*self.commission
                
                trade_amount = self.new_capital - self.capital
                self.trade_amount.append(trade_amount)
                self.trade_percent.append(100*(trade_amount/self.capital))
                self.cum_amount.append(self.new_capital)
                self.cum_percent.append(100* (self.new_capital/    \
                                              self.starting_capital)-100)
                self.capital = self.new_capital
                self.num_trades = self.num_trades + 1

        if self.cur_pos == 0:
            return

        self.cur_pos = 1
        if self.cur_pos == 1:
            self.open_date.append(date)
            self.open_price.append(price)
            self.position.append(1)
            self.num = math.floor(self.capital/price)

    def Sell(self, date, price):
        if self.cur_pos == 1:
            self.close_date.append(date)
            self.close_price.append(price)        
            self.new_capital = self.capital + self.cur_pos * \
                               (price - \
                                self.open_price[len(self.open_price)-1]) \
                               *self.num - 2*self.commission
            
            trade_amount = self.new_capital - self.capital
            self.trade_amount.append(trade_amount)
            self.trade_percent.append(100*(trade_amount/self.capital))
            self.cum_amount.append(self.new_capital)
            self.cum_percent.append(100* (self.new_capital/    \
                                          self.starting_capital)-100)
            self.capital = self.new_capital
            self.num_trades = self.num_trades + 1

        if self.shorts_allowed:
            self.cur_pos = -1
            if self.cur_pos == -1:
                self.open_date.append(date)
                self.open_price.append(price)
                self.position.append(-1)
                self.num = math.floor(self.capital/price)
        else:
            self.cur_pos = -1

    def CalcStats(self):
        if self.num_trades == 0:
            return
        
        self.total_longs = len(self.open_date)

        gains = 0
        for i in range(self.num_trades):
            if self.trade_percent > 0:
                self.profitable_longs = self.profitable_longs + 1
                gains = gains + 1
            else:
                self.successive_gains = max([self.successive_gains,gains]) 
                gains = 0

        self.biggest_gain = max(self.trade_percent)
        self.total_gain = self.cum_amount[self.num_trades -1] \
                          - self.starting_capital
        self.total_gain_p = self.cum_percent[self.num_trades - 1]
        self.average_gain = self.total_gain / self.num_trades
        
    def getCapital(self):
        return self.capital
    
