import requests
import time
from time import sleep
import csv
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
        x=requests.get("http://172.30.211.33:5000/run_sql?command=INSERT INTO devices (Brand, Model, Serial_Number, MAC_Address, Universal_Product_Code, Uploader_Name, Scan_Date, Recipient, Paid_Amount, Vendor, Invoice_IPO, PO_Registered, InControl_Expiration, Notes) VALUES ("+query[0]+","+query[1]+","+query[2]+","+query[3]+","+query[4]+","+query[5]+","+query[6]+","+query[7]+","+query[8]+","+query[9]+","+query[10]+","+query[11]+","+query[12]+","+query[13]+")&cmdtype=write")
        if x.content!= b'complete':
            print(query)
