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

#
# procs accessible within the data server:
#
# addSymbol(symbol)
# removeSymbol(symbol)
# listSymbols()
# setStartDate(date)
# updateData()
# getData(symbol, startdate, enddate)

import os
import string
import shelve
import DateTime
import Numeric
import yahoo

# Available procedures

# add Symbol adds the symbol to the symbol list
# it ensures that the data directory is created
def addSymbol(symbol):
    sybmol = string.lower(symbol)
    symbols.append(symbol)
    dir = os.path.join(data_dir, symbol)
    try:
        os.chdir(dir)
    except:
        os.makedirs(dir)

    startyear = db['startdate'].year
    for i in range(DateTime.now().year - startyear + 1):
        datepath = os.path.join(dir, `startyear+i`)
        try:
            os.chdir(datepath)
        except:
            os.makedirs(datepath)
    
    updateSymbol(symbol)
    db['symbols'] = symbols

# remove symbols removes the symbol from the symbol list
# it deletes all data within the data directory
def removeSymbol(symbol):
    symbol = string.lower(symbol)
    while symbol in symbols:
        symbols.remove(symbol)
    dir = os.path.join(data_dir, symbol)
    # recursively remove all files and data corresponding to this?
    #os.removedirs(dir)
    db['symbols'] = symbols
    if db.has_key(symbol):
        del db[symbol]

# returns the list of currently tracked symbols
def listSymbols():
    return symbols

def hasSymbol(symbol):
    symbol = string.lower(symbol)
    return (symbol in db['symbols'])
            
# sets the start date for available data.
# Q? - does it delete data if the new start date is after the current one?
def setStartDate(date):
    olddate = db['startdate']
    db['startdate'] = date
    if olddate.year > date.year:
        ds_createNewDirs(olddate.year, date.year)

def ds_createNewDirs(highyear, lowyear):
    for i in range(len(symbols)):
        dir = os.path.join(data_dir, symbols[i])
        for j in range(highyear - lowyear + 1):
            datepath = os.path.join(dir, `lowyear+j`)
            try:
                os.chdir(datepath)
            except:
                os.makedirs(datepath)

            
def updateSymbol(symbol):
    print 'Getting data for: ', symbol

    if db.has_key(symbol):
        symbdata = db[symbol]
    else:
        symbdata = {}
        
    if symbdata.has_key('StartDate'):
        date = symbdata['StartDate']
        
        if (db['startdate'] < date) and not \
           (symbdata.has_key('GotStart')):
                print 'Update all data'
                ds_updateSymbolData(symbol, db['startdate'], 1)
        else:
            print 'Just update latest data'
            if symbdata.has_key('LastDate'):
                lastdate = symbdata['LastDate']
            else:
                raise 'Have start date, but not Last Date'

            lastdate = lastdate + DateTime.RelativeDateTime(days=+1)
            ds_updateSymbolData(symbol, lastdate)            
    else:
        print 'No start date'
        ds_updateSymbolData(symbol, db['startdate'], 1)



def ds_updateSymbolData(symbol, begin_date, start=0):
    symbol = string.lower(symbol)

    lastdate = DateTime.now()
    if begin_date > lastdate:
        return
    else:
        date = DateTime.DateTime(begin_date.year, 1, 1)
    print 'Getting data for ', symbol, ' from ', str(date)
    
    infile = di.getData(symbol, date, lastdate)
    throwawayline = infile.readline()
    indata = infile.readlines()

    index = 0
    got_start = 0
    
    startyear = date.year
    endyear = lastdate.year
    curdate = lastdate

    for i in range(endyear - startyear + 1):
        print 'Adding year: ', `endyear - i`
        
        datastring = ''
        while index < len(indata):
            line = indata[index]
            nums = string.split(line, ',')
            if len(nums) >= 5:
                d = ds_toDate(nums[0])
                if d.year < (endyear - i):
                    break
                else:
                    index = index+1
                    curdate = ds_toDate(nums[0])
                    datastring = datastring + line

        dir = os.path.join(data_dir, symbol)
        datfilename = os.path.join(dir, `curdate.year`, 'daily.dat')
        print 'Writing to: ', datfilename, len(datastring)
        datfile = open(datfilename, 'w')
        datfile.write(datastring)
        datfile.close()

        # We didn't get all the data we asked for.  Set the start
        # date and exit our loop
        if index >= len(indata):
            begin_date = curdate
            got_start = 1
            print 'Hit got start for ', symbol
            break

    if db.has_key(symbol):
        symbdata = db[symbol]
    else:
        symbdata = {}
        
    if start:
        symbdata['StartDate'] = begin_date

    if not symbdata.has_key('GotStart'):
        if got_start:
            symbdata['GotStart'] = 1
            
    symbdata['LastDate'] = lastdate
    db[symbol] = symbdata
    
# syncs all the data
def updateData():
    for i in range(len(symbols)):
        updateSymbol(symbols[i])

# retrieves the data for the given symbol and dates
def getData(symbol, startdate=0):
    symbol = string.lower(symbol)

    adate = []
    open_tmp = []
    high_tmp = []
    low_tmp = []
    close_tmp = []
    vol_tmp = []
    have_vol = 0

    if startdate == 0:
        startdate = DateTime.DateTime(1900,1,1)

    if db[symbol].has_key('StartDate'):
        if startdate < db[symbol]['StartDate']:
            startdate = db[symbol]['StartDate']
    else:
        raise 'DB not set properly - no startdate'
        
    dir = os.path.join(data_dir, symbol)
    nowyear = DateTime.now().year
    for i in range(nowyear - startdate.year + 1):
        filename = os.path.join(dir, `nowyear-i`, 'daily.dat')

        infile = open(filename, 'r')
        filebuf = infile.read()
        infile.close
        l = string.split(filebuf,'\n')
        i=0
        
        while i<(len(l)):	
            nums = string.split(l[i], ',')
            if (len(nums) >= 5):
                date = ds_toDate(nums[0])
                if (date >= startdate) or startdate==0:
                    adate.append(date)
                    open_tmp.append(float(nums[1]))
                    high_tmp.append(float(nums[2]))
                    low_tmp.append(float(nums[3]))
                    close_tmp.append(float(nums[4]))
            else:
                pass

            if (len(nums) == 6):
                have_vol = 1
                vol_tmp.append(float(nums[5]))
            else:
                have_vol = 0
            
            i = i + 1

    return adate, Numeric.array(open_tmp), Numeric.array(high_tmp), \
           Numeric.array(low_tmp), Numeric.array(close_tmp), \
           Numeric.array(vol_tmp)

#
# Internal procedures
#
def ds_toDate(datestring):
    "convert a string to a DateTime object"
    
    # should catch exceptions here....
    #return(DateTimeFrom(datestring))
    return DateTime.strptime(datestring, "%d-%b-%y")


def ds_readSymbols():
    return db['symbols']

def ds_openConf():
    conf_file = os.path.join(avidus_dir, 'ds.conf')
    db = shelve.open(conf_file)

    # check for required keys
    #if not db.has_key('symbols'):
    #    print 'error, there should be a symbols key in the conf file'
        
    return db

def ds_closeConf():
    db.close()

#
# Initialization stuff
#
avidus_dir = os.path.join(os.environ['HOME'], '.avidus')
data_dir = os.path.join(avidus_dir, 'data')
db = ds_openConf()
symbols = ds_readSymbols()
di = yahoo.DataImporter()
