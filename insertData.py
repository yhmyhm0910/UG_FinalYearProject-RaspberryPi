import pyodbc   #database usage

file = open('confidential.txt', 'r')    #database security
secret = file.readlines()

server = secret[0].strip()  #Database connection is putted here as pages need to use conn (it is global here)
database = secret[1].strip()
username = secret[2].strip()
password = secret[3].strip()   
driver= '{ODBC Driver 17 for SQL Server}'
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

PMID = '677'  #varchar
RDate = 20230210    #int
RTime = 2021    #varchar

SQLcode = "INSERT INTO Records (PMID, RDate, RTime, Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10, Data11, Data12, Data13, Data14, Data15, Data16, Data17, Data18, Data19, Data20, Data21, Data22, Data23, Data24, Data25, Data26, Data27, Data28, Data29, Data30, Data31, Data32, Data33, Data34) VALUES ((?), (?), (?), 0, 8, 8, 3.20, 2.90, 2.72, 2.60, 2.51, 2.45, 2.40, 2.23, 2.10, 2.10, 2.10, 2.10, 2.20, 2.30, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 1.50, 1.50, 1.50, 0, 0,0,0,0,0,0,0)"

cursor.execute(SQLcode, PMID, RDate, RTime)

conn.commit()

#ALL FAULTS: "INSERT INTO Records (PMID, RDate, RTime, Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10, Data11, Data12, Data13, Data14, Data15, Data16, Data17, Data18, Data19, Data20, Data21, Data22, Data23, Data24, Data25, Data26, Data27, Data28, Data29, Data30, Data31, Data32, Data33, Data34) VALUES ((?), (?), (?), 0, 16, 12, 3.20, 2.90, 2.72, 2.60, 2.51, 2.45, 2.40, 6, 6, 6, 6, 6, 2.20, 2.30, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 1.50, 1.50, 1.50, 1.50, 1.50, 1.50, 1.50,0,0,0,0)"

#Normal: "INSERT INTO Records (PMID, RDate, RTime, Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10, Data11, Data12, Data13, Data14, Data15, Data16, Data17, Data18, Data19, Data20, Data21, Data22, Data23, Data24, Data25, Data26, Data27, Data28, Data29, Data30, Data31, Data32, Data33, Data34) VALUES ((?), (?), (?), 0, 8, 8, 3.20, 2.90, 2.72, 2.60, 2.51, 2.45, 2.40, 2.23, 2.10, 2.10, 2.10, 2.10, 2.20, 2.30, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 1.50, 1.50, 1.50, 0, 0,0,0,0,0,0,0)"

#Fails to Start: "INSERT INTO Records (PMID, RDate, RTime, Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10, Data11, Data12, Data13, Data14, Data15, Data16, Data17, Data18, Data19, Data20, Data21, Data22, Data23, Data24, Data25, Data26, Data27, Data28, Data29, Data30, Data31, Data32, Data33, Data34) VALUES ((?), (?), (?), 0, 8, 32, 3.20, 2.90, 2.72, 2.60, 2.51, 2.45, 2.40, 2.23, 2.10, 2.10, 2.10, 2.10, 2.20, 2.30, 2.40, 2.40, 2.40, 2.40, 2.40, 2.40, 1.50, 1.50, 1.50, 0, 0,0,0,0,0,0,0)"

#671A, 671B, 
#672,
#673, 
#674A, 674B
#675A, 675B
#676
