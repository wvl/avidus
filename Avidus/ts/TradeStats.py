def calculateStats(data, tsd, numDays=0):
    # Calculates the stats based on an input series of buy, sell orders

    # assume single symbol for now, ignore num

    if numDays==0:
        numDays = len(data.adate)

    cap = 10000
    open_price = 0
    
    capital = []
    stats = {}
    
    stats['NumTrades'] = len(tsd)

    # Start from oldest bar and go forward
    r = range(min([numDays, len(data.adate)]))
    r.reverse()

    pl = [cap]
    trade_index = 0
    cur_pos = 0
    for i in r:
        if data.adate[i] == tsd[trade_index].date:
            price = tsd[trade_index].price
            pos = tsd[trade_index].trade
            date = tsd[trade_index].date
                
            if cur_pos == 0: # open
                num = cap/price
                open_price = price
                cur_pos = pos

                capital.append((cap, date))
                pl.insert(0, cap)
                
            else: # close
                cap = cap + pos*(price - open_price)*num
                cur_pos = cur_pos + pos
                
                capital.append((cap,date))
                pl.insert(0, cap)

            if len(tsd) > (trade_index + 1):
                trade_index = trade_index + 1
                          
        else:
            if open_price != 0:
                val = cap + cur_pos*(data.close[i]-open_price)*num
            else:
                val = cap
            pl.insert(0, val)
   
    data.capital = capital
    data.pl = pl

