# getExcelData.py 
# snags excel data from DailE spreadsheet
    # WILL give data to Dash (graph program) to display

# Ethan Jones
# Wendesday, 9:13pm 12-26-18
# ~36 hours

# TODO: Put DailE on google sheets (for mobile use) and maybe write script to pull in and put it into excel or tool to read sheets (but then you have the potential lack of macros, so couldn't do hex color... unless sheets handles color differently?)

# TODO: Macro in excel file to automatically sort cells by cell height (biggest at bottom)

# TODO: Find % of days 100% done for ran

import xlrd
from xlrd import *
from collections import OrderedDict
from operator import itemgetter
import datetime # to display dates properly
import pprint
import pandas as pd # in case xlrd isn't v good


# CELL VALUE FUNCTIONS
def cellValue(row, col):
    return (sheet.cell_value(row, col))

def isntEmpty(row, col):
    return cellValue(row, col) != empty_cell.value

def isEmpty(row, col):
    return cellValue(row, col) == empty_cell.value


# GETTER FUNCTIONS
# Returns thingsDone key when given half of the tuple (data type of keys)
def getKeyFromHalfTuple(half):
    for key in thingsDone.keys():
        if ( (key[0] == half) or (key[1] == half) ):
            return key
    print ("There is no such thing to do currently. Please double-check your data to be able to find the key you're looking for")

# Returns row number from row name
def getRowNumber(rowName):
    for row in range(sheet.nrows):
        if (cellValue(row, 0) == rowName):
            return row
    print ("Row you're searching for does not exist")

# Returns row name from row number
def getRowName(rowNum):
    return cellValue(rowNum, 0)

def getLastColInRow(row):
    lastColumn = sheet.ncols - 1
    while (isEmpty(row, lastColumn)):
        lastColumn -= 1
    return lastColumn

def getTotalInRangeFromDatetime(date):
    listOfThingsAtDate = list(amountOfThingsAtDate.items())
    # May need to generalize the below into a function for use with other functions
    # Maybe recursively?
    for i in range(len(listOfThingsAtDate)):
        listDate = listOfThingsAtDate[i][0]
        listDateThingTotal = listOfThingsAtDate[i][1]
        # If loop has reached last iteration (it is in the current date range of changes) return the current total. Prevents an off by 1 error putting this before defining the variable for the next date
        if (i == len(listOfThingsAtDate) - 1):
            return listDateThingTotal
        nextListDate = listOfThingsAtDate[i+1][0]
        if (date >= listDate and date < nextListDate):
            return listDateThingTotal
        


# MAIN FUNCTIONS
# TODO: Function to snag data from certain date
# Add prompt in normal functions to ask for data only after certain date?
# Initialize dictionary thingsDone with DailE things to do and their row numbers
def initialize():
    global datesRowsChanged
    global masterListOfRows

    for row in range(1, sheet.nrows):
        # Initializes master list of all rows 
        if(isntEmpty(row, 0)):
            masterListOfRows.append((row, cellValue(row, 0)))

        # Gets rid of tracking data so it doesn't count it as things completed in thingsDone dictionary or hold their info in the row date start dictionary
        if(isntEmpty(row, 0) 
            and row != getRowNumber('Column Number')
            and row != getRowNumber('Real Day Number')
            and row != getRowNumber('Daily Color in Hex')):
                key = (row, cellValue(row, 0))
                initializeWhenThingsWereAdded(row, key)
                if (row != getRowNumber('Screen Time')
                and row != getRowNumber('Video Game Time')
                and row != getRowNumber('Amount of Snoozes')):
                    thingsDone[key] = 0

    # Sets important global variables. One dependent on masterListOfRows, hence placement.
    setGlobals()

    # Sets how many things there were to do at each date new things were added
    initializeTotalThingsAtDate()

    # Initializes columns of what days were actually logged
    initializeRealDayColumns()

    # Initializes dictionary storing total of things done in certain range of dates
    for date in datesRowsChanged:
        totalsDoneInRange[date] = 0

    # TODO: Assess if this should be taken out. Dictionary never used
    for key, val in whenThingsWereAdded.items():
        columnWhenThingsWereAdded[(getRowNumber(key), key)] = excelColumnFromDatetime(val)

# Necessary hardcoding of dates when new rows were added
# TODO: Add start dates as comment on first column. Access these values and initialize them here instead of hardcoding
# Also add a suffix of T for tracker columns. create a dictionary to track date and amount of tracker columns added (.endswith('T'))
# TODO: Create a dictionary storing totals of just things to be done at certain dates (NO TRACKERS) by copying amountOfThingsAtDate
# Subtract the tracker rows from things to be done dict
# Check if the total things to be done at dates are the same. If so, only keep the smaller date
def initializeWhenThingsWereAdded(rowNum, key):
    global whenThingsWereAdded

    # Only stores row name as key so can convert this into an ordered dictionary
    # TODO: Figure out how to do with tuple key (for dict key consistency of (rowNum, rowName))
    if(getRowName(rowNum) == 'Read Paper'
    or getRowName(rowNum) == 'Exercise'
    or getRowName(rowNum) == 'Write 100 Words'
    or getRowName(rowNum) == 'Do Music'
    or getRowName(rowNum) == 'Study Something'
    or getRowName(rowNum) == 'Meditate'
    or getRowName(rowNum) == 'Observe in Present'
    or getRowName(rowNum) == 'Breathe'
    or getRowName(rowNum) == 'Read Rules'
    or getRowName(rowNum) == 'DRINK WATER'
    or getRowName(rowNum) == 'Create Something Tangible'
    or getRowName(rowNum) == 'Look at and adjust beliefs'
    or getRowName(rowNum) == 'Spend Time Outside'
    or getRowName(rowNum) == 'Do Work'
    or getRowName(rowNum) == 'Listen to a New Song'
    or getRowName(rowNum) == 'Eat Greens/Fruit'
    or getRowName(rowNum) == 'Wake Up Early'
    or getRowName(rowNum) == 'Learn Something'
    or getRowName(rowNum) == 'Name 3 Good Things From Today'
    or getRowName(rowNum) == 'Reflect Back on Day'
    or getRowName(rowNum) == 'Talk to Someone'
    or getRowName(rowNum) == 'Make Bed'
    or getRowName(rowNum) == 'Not Sober'):
        whenThingsWereAdded[key[1]] = stringToDatetime('01/01/2018')

    if(getRowName(rowNum) == 'Think About Yourself'
    or getRowName(rowNum) == 'Give Time for Yourself'):
        whenThingsWereAdded[key[1]] = stringToDatetime('01/10/2018')

    if(getRowName(rowNum) == 'Take a Break'
    or getRowName(rowNum) == "Today's Color"):
        whenThingsWereAdded[key[1]] = stringToDatetime('01/22/2018')

    if(getRowName(rowNum) == 'Quality of day /10'):
        whenThingsWereAdded[key[1]] = stringToDatetime('02/08/2018')

    if(getRowName(rowNum) == 'Watch Sunset'):
        whenThingsWereAdded[key[1]] = stringToDatetime('04/12/2018')

    if(getRowName(rowNum) == 'Find Beauty'):
        whenThingsWereAdded[key[1]] = stringToDatetime('04/17/2018')

    if(getRowName(rowNum) == 'Do Something You Enjoy'):
        whenThingsWereAdded[key[1]] = stringToDatetime('05/02/2018')

    if(getRowName(rowNum) == 'Write 4 bars'):
        whenThingsWereAdded[key[1]] = stringToDatetime('08/12/2018')

    if(getRowName(rowNum) == 'Special Comments'):
        whenThingsWereAdded[key[1]] = stringToDatetime('11/08/2018')

    if(getRowName(rowNum) == 'Laugh'):
        whenThingsWereAdded[key[1]] = stringToDatetime('12/04/2018')

    if(getRowName(rowNum) == 'Try Something'):
        whenThingsWereAdded[key[1]] = stringToDatetime('12/15/2018')

    if(getRowName(rowNum) == 'Code'):
        whenThingsWereAdded[key[1]] = stringToDatetime('12/17/2018')

    if(getRowName(rowNum) == 'Listen to Someone'):
        whenThingsWereAdded[key[1]] = stringToDatetime('01/14/2019')

    if(getRowName(rowNum) == 'Watch TED Talk'):
        whenThingsWereAdded[key[1]] = stringToDatetime('01/15/2019')

    if(getRowName(rowNum) == 'Predict Something'
    or getRowName(rowNum) == 'Were you correct?'
    or getRowName(rowNum) == 'Be Grateful'
    or getRowName(rowNum) == 'Do Your Best at Something'):
        whenThingsWereAdded[key[1]] = stringToDatetime('01/19/2019')

    if(getRowName(rowNum) == 'Screen Time'
    or getRowName(rowNum) == 'Video Game Time'):
        whenThingsWereAdded[key[1]] = stringToDatetime('01/22/2019')

    if(getRowName(rowNum) == 'Amount of Snoozes'):
        whenThingsWereAdded[key[1]] = stringToDatetime('01/23/2019')
    
    if(getRowName(rowNum) == 'Think Deeply'):
        whenThingsWereAdded[key[1]] = stringToDatetime('01/25/2019')

    if(getRowName(rowNum) == 'Do Something Kind for Yourself'):
        whenThingsWereAdded[key[1]] = stringToDatetime('01/26/2019')
        
    # Amount of Sleep 1/30/19
    # Floss 1/30/19
    # Fail 1/31/19
    # Reflect on Feelings 2/9/19
    # Review List 2/9/19
    # Write on paper 2/15/19
    # Ask Question 2/21/19
    # Todays color2 3/1/19
    # Todays color3 3/1/19
    # Face something 3/5/19
    # Observe system, not see individual 3/5/19
    # Think about neuroplasticity 3/17/19
    # Exercize self discipline 3/18/19
    # Do personal work 3/21/19
    # Reflect back on past 3/21/19
    # Talk & Listen to yourself out loud 3/21/19
    # Liesure Screen Time 3/22/19
    # Think about future 3/27/19
    # Solve a puzzle 3/27/19
    # Note area to improve 4/2/19
    # Learn skill 4/2/19
    # Do something with intent 4/13/19
    

    # Converted to ordered dict here instead of from beginning because you can't guarantee the rows stay in the same order
    whenThingsWereAdded = OrderedDict(sorted(whenThingsWereAdded.items(), key=itemgetter(1)))

# Sets how many things there were to do at each date new things were added
def initializeTotalThingsAtDate():
    global datesRowsChanged

    # First finds unique amounts of things to do added at each date
    for val in whenThingsWereAdded.values():
        newKey = val
        amountOfThingsAtDate[newKey] = amountOfThingsAtDate.get(newKey, 0) + 1

    # Adds these dates to an important list, then sorts it
    for key in amountOfThingsAtDate.keys():
        datesRowsChanged.append(key)
    datesRowsChanged.sort()

    # Then sums up these values last to first to get totals of things to do at each date new things were added
    for i in range(len(datesRowsChanged) - 1, 0, -1):
        for j in range(i):
            amountOfThingsAtDate[datesRowsChanged[i]] += amountOfThingsAtDate[datesRowsChanged[j]]

# Initializes columns of what days were actually logged
def initializeRealDayColumns():
    global realDayColumns

    realDayRow = getRowNumber('Real Day Number')
    for col in range(1, currentColumnNumber + 1):
        if isntEmpty(realDayRow, col):
            realDayColumns.append(col)

def setGlobals():
    global currentAmountOfDailyThings
    global realDayNumber
    global currentColumnNumber
    global currentDay

    for rows in masterListOfRows:
        currentAmountOfDailyThings += 1
    currentAmountOfDailyThings -= totalTrackerRows
    
    columnCounterRow = getRowNumber('Column Number')
    currentColumnNumber = int(cellValue(columnCounterRow, getLastColInRow(columnCounterRow)))
    currentDay = excelCellToDatetime(0, currentColumnNumber)
    realDayRow = getRowNumber('Real Day Number')
    realDayNumber = int(cellValue(realDayRow, getLastColInRow(realDayRow)))


# CALCULATOR FUNCTIONS
# Sums up all things done, storing the info in dictionaries
# TODO: sum rows that keep track by number (minutes of music, screen time, snoozes, etc)
def calculateTotals():
    global totalOfAllThingsDone
    global totalsDoneInRange
    global correctNumberOfPredictions

    for col in realDayColumns:
        for row in thingsDone.keys():
            row = row[0]
            if (cellValue(row, col) == '-'):
                continue
            if ((isntEmpty(row, col) and row != getRowNumber('Not Sober')) 
            or  (isEmpty(row, col) and row == getRowNumber('Not Sober'))):
                    addToRangedTotal(col)
                    thingsDone[getKeyFromHalfTuple(row)] += 1
                    totalOfAllThingsDone += 1
                    if (row == getRowNumber('Were you correct?') and cellValue(row, col).startswith('y')):
                        correctNumberOfPredictions += 1

# Helper function for calculateTotals
# Checks what range the given column is in, then adds 1 to the count of things done in that range (since this is only called after a cell empty check)
def addToRangedTotal(col):
    global totalsDoneInRange
    # iterator goes through the dates rows were added to check for the range col is in. Has to be total to keep value outside of this function
    global iterator

    date = excelCellToDatetime(0, col)
    if (iterator != (len(datesRowsChanged) - 1) and 
        date == datesRowsChanged[iterator + 1]):
            iterator += 1
    if (iterator != (len(datesRowsChanged) - 1) and
        date >= datesRowsChanged[iterator] and 
        date < datesRowsChanged[iterator + 1]):
            totalsDoneInRange[datesRowsChanged[iterator]] = totalsDoneInRange.get(datesRowsChanged[iterator], 0) + 1
    if (iterator == len(datesRowsChanged) - 1):
        totalsDoneInRange[datesRowsChanged[iterator]] = totalsDoneInRange.get(datesRowsChanged[iterator], 0) + 1

# TODO: Find average of each row done
def calculateAverages():
    global daysQualityCounted
    global averageQuality
    global overallAverageThings
    global overallAverageThingsDone
    global overallAveragePercentageOfThingsDone

    # Average quality of days
    quality = 0
    qualityRow = getRowNumber('Quality of day /10')
    # Starts at 39 because you didn't start tracking your quality of day until then
    for col in realDayColumns:
        if (isntEmpty(qualityRow, col)):
            quality += cellValue(qualityRow, col)
            daysQualityCounted += 1
    averageQuality = quality/daysQualityCounted

    # Average amount of things done/day in ranges

    # Listify to access by index
    rangedTotalKeyList = list(totalsDoneInRange.keys())
    rangedTotalValueList = list(totalsDoneInRange.values())
    rangedAmountOfThingsList = list(amountOfThingsAtDate.values())
    for i in range (len(totalsDoneInRange)):
        if (i == len(totalsDoneInRange) - 1):
        # Do last changed date to current date key here
            keyString = str(datetimeToString(rangedTotalKeyList[i]) + '-' + datetimeToString(currentDay))
        else:
            previousDayToEndDate = rangedTotalKeyList[i + 1] - datetime.timedelta(1)
            keyString = str(datetimeToString(rangedTotalKeyList[i]) + '-' + datetimeToString(previousDayToEndDate))
        # Calculates averages
        averagePerDay = rangedTotalValueList[i] / daysBetweenRanges[i]
        averageTotalThingsCompletedPerDay = averagePerDay / rangedAmountOfThingsList[i]
        # Adds them to dictionary
        averagesDoneInRangePerDay[keyString] = (averagePerDay, rangedAmountOfThingsList[i], averageTotalThingsCompletedPerDay)

    # Average amount of things to do and average amount of things done
    acc = 0
    for val in averagesDoneInRangePerDay.values():
        overallAverageThingsDone += val[0]
        overallAverageThings += val[1]
        overallAveragePercentageOfThingsDone += val[2]
        acc += 1
    overallAverageThingsDone /= acc
    overallAverageThings /= acc
    overallAveragePercentageOfThingsDone /= acc
    overallAveragePercentageOfThingsDone *= 100

def calculateDaysBetweenRanges():
    global daysBetweenRanges

    # TODO: Assess if should be changed to for loop
    i = 0
    while (i <= len(datesRowsChanged) - 1):
        # This part calculates the distance between the last day things were changed and the current day
        if (i == len(datesRowsChanged) - 1):
            dayGap = currentDay - datesRowsChanged[i]
        else:
            dayGap = datesRowsChanged[i + 1] - datesRowsChanged[i]
        dayGap = dayGap.days

        # If the current day is the same day that things were changed last, the difference between those days is 0. This treats the day as a whole day, and avoids a Zero Division Error when calculating averages
        if (dayGap == 0):
            dayGap = 1

        daysBetweenRanges.append(dayGap)
        i += 1
    # Hardcoding in the crossfaded period. Inaccurate representation of days between will be represented but only dependency is average, and this'll allow that to calculate properly
    daysBetweenRanges[6] = 19


# PRINTER FUNCTIONS
def printTotals():
    # Prints list of things to do and how much they've been done
    printThingsDone()
    
    # Prints days logged
    print ('\nDays logged: {}'.format(realDayNumber))

    # Prints sum of all things done
    print ('Total of all things done: {}'.format(totalOfAllThingsDone))

    # Prints new line for cleanliness
    print ()

# TODO: Print total screen and video game time, as well as averages, and snooze average. 
# How many days for each also
# TODO: Change predictions correct to incorrect? (since that lines up more with goal)
def printAverages():
    # Percentage of days logged
    percentageOfDaysLogged = (realDayNumber / currentColumnNumber) * 100
    print ("Days logged {0:.0f}% of the time".format(percentageOfDaysLogged))

    # Things to do and log
    totalToLog = len(masterListOfRows) - totalTrackerRows
    print ("There's currently {} things to do, and {} total things to log".format(len(thingsDone), totalToLog))

    # Things done
    print ("Average amount of things done per day: {0:.0f}, which is {1:.0f}% of all things to do".format(overallAverageThingsDone, overallAveragePercentageOfThingsDone))

    # Sober/high average
    percentageOfDaysSober = (thingsDone[getKeyFromHalfTuple('Not Sober')] / realDayNumber) * 100
    print ("Percent of days sober: {0:.0f}%".format(percentageOfDaysSober))

    # Quality of day
    print ("Average day quality is {0:.0f}/10 for {1} days logged ({2:.0f}% of total days)".format(averageQuality, daysQualityCounted, daysQualityCounted/realDayNumber * 100))

    # Predictions correct
    print ("Predictions have been correct {0:.0f}% of the time".format(correctNumberOfPredictions/thingsDone[getRowNumber('Predict Something'), 'Predict Something'] * 100))

    # Prints new line after all data, so looks cleaner
    print ()

def printDatetime(datetime):
    print(datetimeToString(datetime))

def printWhenThingsStarted():
    for key, value in whenThingsWereAdded.items():
        print('{} (row {}) started on {}'.format(key[1], key[0], value))

def printThingsDone():
    for key, val in thingsDone.items():
        if (key == getKeyFromHalfTuple("Quality of day /10")
            or key == getKeyFromHalfTuple("Today's Color")):
                continue
        # Print sober instead of not sober because excel sheet tracks not sober so high days can be visualized, data tracks sober days
        if (key == getKeyFromHalfTuple("Not Sober")):
            print (key[0], "Sober", '=>', val)
            continue
        if( key[0] < 10 ):
            print(str(0) + str(key[0]), key[1], '=>', val)
        else:
            print (key[0], key[1], '=>', val)

def printTotalThingsAtDate():
    for key, value in amountOfThingsAtDate.items():
        print('On {} there was a total of {} things to be done'.format(datetimeToString(key), value))


# CONVERTERS
def stringToDatetime(dateStr):
    d = datetime.datetime.strptime(dateStr, '%m/%d/%Y')
    return d

def datetimeToString(datetime):
    dateStr = datetime.strftime('%m/%d/%Y')
    month, day, year = dateStr.split('/')
    if (month.startswith('0')):
        month = month.lstrip('0')
    if (day.startswith('0')):
        day = day.lstrip('0')
    dateStr = '/'.join([month, day, year])
    return (dateStr)

def dateToExcelDate(day):
    # Okay things get a bit hinky here, thanks excel...
    # Excel dates formulated on days past since 1/0/1900
    # Since 0 not valid for datetime, did 12/31/1899
    # To include the current day, made it go back 1 day further to 12/30/1899
    date0 = datetime.datetime(1899, 12, 30)
    try:
        date1 = stringToDatetime(day)
    except TypeError:
        date1 = day
    daysInBetween = date1 - date0
    return (daysInBetween.days)

def excelCellToDatetime(row, col):
    d = xlrd.xldate_as_tuple(cellValue(row, col), file.datemode)
    return datetime.datetime(*d)

def excelColumnFromDatetime(date):
    date = dateToExcelDate(date)
    for col in range(sheet.ncols):
        if (cellValue(0, col) == date):
            return col


# ERROR CHECKERS
def errorChecker():
    if (currentAmountOfDailyThings != len(whenThingsWereAdded)):
        raise Warning('\nThere is an inconsistency in your data. \nThis is likely caused by adding a new row in your excel file and not hardcoding it into whenThingsWereAdded. \nIt can also be caused by renaming rows in the excel file and not making the appropriate adjustments in whenThingsWereAdded. \nIt can also be caused by adding a new tracking row and not adding it to totalTrackerRows')


# DATA TYPES
# TODO: For dates tracking: Class? Or just keep info of columns in dict? Seems class bc naming is clearer
# % of things done that day (out of hardcoding total of things that can be done at given date (or column #?)) 
# excluding not sober, daily color, hex of daily color, quality of day, column number
# quality of day
# daily color hex
# not sober
class dateInfo():
    def __init__(self, date):
        self.date = date
        self.column = excelColumnFromDatetime(date)
        self.amountDone = 0
        self.percentageDone = getTotalInRangeFromDatetime(date)
        self.quality = 0
        self.notSober = False
        self.sober = False
        self.color = ''

        for row in thingsDone.keys():
            row = row[0]
            if (isntEmpty(row, self.column)):
                self.amountDone += 1

        



# TODO: Change string and get functions to .upper() or .lower() so capitalization changes in excel sheet don't matter

# TODO: Add print functions to all important dictionaries

# TODO: See if dicts need to be prefaced with global before modification in a function

file = xlrd.open_workbook('OneDrive\\dailE.xlsm')
sheet = file.sheet_by_index(0)
totalTrackerRows = 3
masterListOfRows = []
realDayColumns = []
# The below just has the row name, not the tuple of (#, name)
whenThingsWereAdded = {}
columnWhenThingsWereAdded = OrderedDict()
amountOfThingsAtDate = OrderedDict()
totalsDoneInRange = OrderedDict()
thingsDone = {}
datesRowsChanged = []
daysBetweenRanges = []
averagesDoneInRangePerDay = OrderedDict()
currentAmountOfDailyThings = 0
currentColumnNumber = 0
currentDay = 0
realDayNumber = 0
daysQualityCounted = 0
averageQuality = 0
totalOfAllThingsDone = 0
overallAverageThings = 0
overallAverageThingsDone = 0
overallAveragePercentageOfThingsDone = 0
correctNumberOfPredictions = 0
iterator = 0

initialize()
calculateDaysBetweenRanges()
calculateTotals()
calculateAverages()
printTotals()
printAverages()
print(amountOfThingsAtDate)
errorChecker()



today = dateInfo(currentDay)
print (today.percentageDone)
