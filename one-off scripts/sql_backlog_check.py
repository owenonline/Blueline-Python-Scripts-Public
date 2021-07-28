from selenium import webdriver
import csv
import requests
missing=[]
with open('C:\\Users\\owenb\\OneDrive\\Documents\\Work Documents\\combined_inventory.csv',newline='') as csvfile:
    reader=csv.reader(csvfile,dialect='excel')
    next(reader)
    for row in reader:
        query=[]
        for x in row[:6]:
            if len(x)>0 and x!="Not Found" and x!="missing":
                x=x.replace("'","''")
                x=x.replace("&","and")
                x=x.replace('#','%23')
                query.append("'"+x+"'")
            else:
                query.append("NULL")
        split=row[6].split('/')
        if len(row[6])>0 and len(split)==3:
            if len(split[0])==1:
                split[0]="0"+split[0]
            if len(split[1])==1:
                split[1]="0"+split[1]
            query.append("datetime('"+split[2]+"-"+split[0]+'-'+split[1]+" 00:00:00')")
        elif len(row[6])>0:
            x=x.replace("'","''")
            x=x.replace("&","and")
            x=x.replace('#','%23')
            query.append("'"+x+"'")
        else:
            query.append("NULL")
        for x in row[7:]:
            if len(x)>0 and x!="Not Found":
                x=x.replace("'","''")
                x=x.replace("&","and")
                x=x.replace('#','%23')
                query.append("'"+x+"'")
            else:
                query.append("NULL")
        x=requests.get("http://172.30.211.33:5000/run_sql?command=SELECT * FROM devices WHERE Brand IS "+query[0]+" AND Model IS "+query[1]+" AND Serial_Number IS "+query[2]+" AND MAC_Address IS "+query[3]+" AND Scan_Date IS "+query[6]+"&cmdtype=read")
        if x.content==b'[]\n':
            print(x.content)
            missing.append(query)
