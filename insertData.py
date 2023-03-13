import datetime
import re
import pyodbc   #database usage

file = open('confidential.txt', 'r')    #database security
secret = file.readlines()

server = secret[0].strip()  #Database connection is putted here as pages need to use conn (it is global here)
database = secret[1].strip()
username = secret[2].strip()
password = secret[3].strip()   
driver= '{ODBC Driver 18 for SQL Server}'
Authentication='ActiveDirectoryPassword' #This is so very important, email format issue https://github.com/mkleehammer/pyodbc/issues/1008
conn = pyodbc.connect(
    'AUTHENTICATION='+Authentication+
    ';DRIVER='+driver+
    ';SERVER='+server+
    ';PORT=1433;DATABASE='+database+
    ';UID='+username+
    ';PWD='+ password
) 

cursor = conn.cursor()

def checkValidPMID(PMID):
    isValid = False
    givenPMIDs = ['671A', '672', '673', '674A', '675A', '676']
    for i in range(len(givenPMIDs)):
        if (PMID == givenPMIDs[i]):
            isValid = True
            break
    return isValid

def inputToday():
    today = datetime.date.today()
    todayYear = str(today.year)
    todayMonth = str(today.month)
    todayDay = str(today.day)
    if (len(todayMonth)<2):
        todayMonth = '0' + todayMonth
    if (len(todayDay)<2):
        todayDay = '0' + todayDay     

    returnRDate = int(todayYear+todayMonth+todayDay)   
    return returnRDate

def checkValidRTime(RTime, lastRDate, lastRTime):
    def containENG(toCheck):
        for i in range(len(toCheck)):
            if toCheck[i] != '0' and toCheck[i] != '1' and toCheck[i] != '2' and toCheck[i] != '3' and toCheck[i] != '4' and toCheck[i] != '5' and toCheck[i] != '6' and toCheck[i] != '7' and toCheck[i] != '8' and toCheck[i] != '9':
                return True
            else: return False

    isValid = [False, False, True, False]    #[Hour, Mins, all are numbers, Last Operation Time]
    RTime_str = str(RTime)
    if len(RTime_str) == 4:
        if containENG(RTime_str) == True:
            isValid[2] = False
        RHour_str = RTime_str[0] + RTime_str[1]
        RMins_str = RTime_str[2] + RTime_str[3]
        if containENG(RHour_str) == False and containENG(RMins_str) == False:    #Protect int() from non-numberic input
            RHour = int(RHour_str)
            RMins = int(RMins_str)
            if ((RHour > -1) and (RHour < 24)):
                isValid[0] = True
            if ((RMins > -1) and (RMins < 60)):
                isValid[1] = True
    
    if isValid == [True, True, True, False]:    #All OK -> check early time
        today = inputToday()
        if int(lastRDate) == int(today):    #Type not the same
            if (int(lastRTime) < int(RTime)): #First Correct Format, then check earlier or not
                isValid[3] = True
        else:   #A new day
            isValid[3] = True

    return isValid

def inputPMID(lastPMID):
    isInputValidPMID = False
    if 'A' in lastPMID:
        inputPMID = lastPMID[0] + lastPMID[1] + lastPMID[2] + 'B'
        print('PMID this time (last time was ' + lastPMID + '): ' + inputPMID)
        isInputValidPMID = True
        return inputPMID
    while (isInputValidPMID == False):
        print('Enter PMID: (Available PMID: 671A, 672, 673, 674A, 675A, 676)')
        inputPMID = input()
        if (checkValidPMID(inputPMID) == False):
            print('Invalid PMID (Available PMID: 671A, 672, 673, 674A, 675A, 676)')
        else:
            isInputValidPMID = True
            return inputPMID
    
def inputRDate():
    print('RDate (yyyymmdd):')
    print(inputToday()) #return RDate
    return inputToday()

def inputRTime(lastRDate, lastRTime):
    isValidRTime = False
    while (isValidRTime == False):
        print('Enter Record Time (hhmm):')
        inputRTime = input()
        checkValidRTime_bool = checkValidRTime(inputRTime, lastRDate, lastRTime)
        if (checkValidRTime_bool[0] == False):
            print('Invalid RTime: Wrong Hour. Acceptable range: 0-23')
        if (checkValidRTime_bool[1] == False):
            print('Invalid RTime: Wrong Minute. Acceptable range: 00-59')
        if (checkValidRTime_bool[2] == False):
            print('Invalid RTime: Numbric Inputs ONLY')
        if checkValidRTime_bool == [True, True, True, False]:
            print('Invalid RTime: Earlier than last Record.')
        if checkValidRTime_bool == [True, True, True, True]:
            isValidRTime = True
            return inputRTime

def checkValidData(data:str):
    countComma = 0
    isValid = [False, True, True]    #[34 items, all are floats, no negative]
    for i in range(len(data)):
        if data[i] == ',':
            countComma += 1
    if countComma == 33:
        isValid[0] = True       #contain 34 items
    for i in range(len(data)):
        if data[i] != '0' and data[i] != '1' and data[i] != '2' and data[i] != '3' and data[i] != '4' and data[i] != '5' and data[i] != '6' and data[i] != '7' and data[i] != '8' and data[i] != '9' and data[i] != '.' and data[i] != ',' and data[i] != ' ' and data[i] != '-':
            isValid[1] = False      #contain ABCabc!@#
    for i in range(len(data)):
        if data[i] == '-':
            isValid[2] = False  #Have -ve number
    return isValid


def inputData():
    isValidInputData = False
    inputData = ''  #Initialize
    while isValidInputData == False:
        print('Enter Data 1 to Data 34. Use "," to Seperate every Data.')
        inputData = input()
        checkValidData_bool = checkValidData(inputData)
        if checkValidData_bool[0] == False:
            print('Do Not Have EXACTLY 34 sets of numbers.')
        if checkValidData_bool[1] == False:
            print('Illegal Input (Incorrect Format)')
        if checkValidData_bool[2] == False:
            print('Illegal Input (Negative Numbers)')
        if checkValidData_bool == [True, True, True]:
            isValidInputData = True

    counter = 0     #start to form array
    dataInArray_str = [''] * 34
    for i in range(len(inputData)):
        if inputData[i] != ',':
            dataInArray_str[counter] += inputData[i]
        else:
            counter += 1

    dataInArray = [0.00] * 34
    for i in range(len(dataInArray_str)):
        dataInArray[i] = float(dataInArray_str[i])

    return dataInArray

def writeToSQL(PMID, RDate, RTime, Data):
    SQLcode = "INSERT INTO Records (PMID, RDate, RTime, Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10, Data11, Data12, Data13, Data14, Data15, Data16, Data17, Data18, Data19, Data20, Data21, Data22, Data23, Data24, Data25, Data26, Data27, Data28, Data29, Data30, Data31, Data32, Data33, Data34) VALUES ((?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?))"
    cursor.execute(SQLcode, PMID, RDate, RTime, Data[0], Data[1], Data[2], Data[3], Data[4], Data[5], Data[6], Data[7], Data[8], Data[9], Data[10], Data[11], Data[12], Data[13], Data[14], Data[15], Data[16], Data[17], Data[18], Data[19], Data[20], Data[21], Data[22], Data[23], Data[24], Data[25], Data[26], Data[27], Data[28], Data[29], Data[30], Data[31], Data[32], Data[33])

    conn.commit()

    print('Successfully Input a New Record!')

def takeRecord():
    def SQLResultToUsable(SQL):
        usable = re.findall("[a-zA-Z0-9]+",SQL)
        return usable[0]
    cursor.execute('SELECT TOP 1 PMID FROM Records ORDER BY (str(RDate) + str(RTime)) DESC;')
    lastPMID_SQL = str(cursor.fetchall())
    lastPMID = SQLResultToUsable(lastPMID_SQL)
    cursor.execute('SELECT TOP 1 RDate FROM Records ORDER BY (str(RDate) + str(RTime)) DESC;')
    lastRDate_SQL = str(cursor.fetchall())
    lastRDate = SQLResultToUsable(lastRDate_SQL)
    cursor.execute('SELECT TOP 1 RTime FROM Records ORDER BY (str(RDate) + str(RTime)) DESC;')
    lastRTime_SQL = str(cursor.fetchall())
    lastRTime = SQLResultToUsable(lastRTime_SQL)

    return [lastPMID, lastRDate, lastRTime]

#----------------------Main-----------------------------------------------------------------------------------------------------
lastRecord = takeRecord()   #return last operation [PMID, RDate, RTime]
finalRDate = inputRDate()    #return RDate (today)
finalPMID = inputPMID(lastRecord[0])     #return PMID
finalRTime = inputRTime(lastRecord[1], lastRecord[2])   #return RTime
finalData = inputData()
writeToSQL(finalPMID, finalRDate, finalRTime, finalData)
#-------------------------------------------------------------------------------------------------------------------------------


#ALL FAULTS: 0, 16, 12, 3.20, 2.90, 2.72, 2.60, 2.51, 2.45, 2.40, 6, 6, 6, 6, 6, 2.20, 2.30, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 1.50, 1.50, 1.50, 1.50, 1.50, 1.50, 1.50,0,0,0,0

#Normal: 0, 8, 8, 3.20, 2.90, 2.72, 2.60, 2.51, 2.45, 2.40, 2.23, 2.10, 2.10, 2.10, 2.10, 2.20, 2.30, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 1.50, 1.50, 1.50, 0, 0,0,0,0,0,0,0

#Fails to Start: 0, 16, 16, 3.20, 2.90, 2.72, 2.60, 2.51, 2.45, 2.40, 2.23, 2.10, 2.10, 2.10, 2.10, 2.20, 2.30, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 1.50, 1.50, 1.50, 0, 0,0,0,0,0,0,0

#Fails to Switch: 0, 8, 8, 7, 7, 7, 7, 6.8, 6.8, 6.8, 6, 6, 6, 6, 6, 6, 5, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 1.50, 1.50, 1.50, 0, 0,0,0,0,0,0,0

#Sticky Chair: 0, 12, 12, 7.2, 6.9, 6.72, 6.6, 6.51, 6.45, 6.4, 6.23, 6.10, 5.1, 5.1, 4.6, 4.7, 4.8, 4.9, 4.9, 4.9, 4.9, 4.9, 3.5, 3.5, 3.5, 3.5, 0, 0,0,0,0,0,0,0

#Fails to Lock: 0, 8, 8, 3.20, 2.90, 2.72, 2.60, 2.51, 2.45, 2.40, 2.23, 2.10, 2.10, 2.10, 2.60, 2.70, 2.80, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 2.90, 0

#Encounters Obstructions: 0, 8, 8, 3.20, 2.90, 2.72, 2.60, 2.51, 2.45, 2.40, 2.23, 2.10, 2.10, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0

#Normal margin: 0, 11, 12, 6.20, 5.90, 5.72, 5.60, 5.51, 4.45, 3.40, 2.00, 1.90, 1.90, 2.0, 2.0, 2.50, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 1.50, 1.50, 1.50, 1.0, 0,0,0,0,0,0,0