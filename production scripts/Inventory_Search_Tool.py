import xlsxwriter
from openpyxl import load_workbook
import requests
import sqlite3

user=input("Please enter your computer username: ")
command=input("Please enter SQL search query: ")
returned=requests.get("http://172.30.211.33:5000/run_sql?command="+command+"&cmdtype=read")
workbook=xlsxwriter.Workbook('C:\\Users\\'+user+'\\Downloads\\Inventory_Selection.xlsx')
worksheet = workbook.add_worksheet()
data=returned.json()
data=list(map(lambda x:["'"+str(y)+"'" if y else 'NULL' for y in x],data))
worksheet.add_table('A1:O'+str(len(data)),{'data':data,'columns':[
    {'header':'Id'},
    {'header':'Brand'},
    {'header':'Model'},
    {'header':'Serial Number'},
    {'header':'MAC Address'},
    {'header':'Universal Product Code'},
    {'header':'Uploader Name'},
    {'header':'Date'},
    {'header':'Customer'},
    {'header':'Price'},
    {'header':'Vendor'},
    {'header':'Invoice / PO'},
    {'header':'PO Registered'},
    {'header':'Incontrol Expiration'},
    {'header':'Notes'}
    ]})
workbook.close()
print("You can find your search results in your downloads folder in a file called 'Inventory_Selection.xlsx'")
print("When entering data into the spreadsheet, be sure to surround it with single quotes. If there is no data, type NULL without single quotes.")
upload=input("Press enter once you have saved your changes in the file to upload your changes to the inventory database.")
workbook=load_workbook(filename = 'C:\\Users\\'+user+'\\Downloads\\Inventory_Selection.xlsx')
changed_data=list(map(lambda x:[y.value for y in x],workbook['Sheet1']))
changed_data_set=set(map(lambda x: '~~~~~'.join(x),changed_data))
data_set=set(map(lambda x: '~~~~~'.join(x),data))
return_data=[x.split('~~~~~') for x in changed_data_set-data_set]
return_data.remove(['Id','Brand', 'Model', 'Serial Number', 'MAC Address', 'Universal Product Code', 'Uploader Name', 'Date', 'Customer', 'Price', 'Vendor', 'Invoice / PO', 'PO Registered', 'Incontrol Expiration', 'Notes'])
for query in return_data:
    for x in range(len(query)):
        if 'NULL' not in query[x]:
            if query[x][0]!="'":
                query[x]="'"+query[x]
            if query[x][-1]!="'":
                query[x]=query[x]+"'"
        else:
            query[x]='NULL'
    x=requests.get("http://172.30.211.33:5000/run_sql?command=UPDATE devices SET Brand = "+query[1]+", Model = "+query[2]+", Serial_Number = "+query[3]+", MAC_Address = "+query[4]+", Universal_Product_Code = "+query[5]+", Uploader_Name = "+query[6]+", Scan_Date = "+query[7]+", Recipient = "+query[8]+", Paid_Amount = "+query[9]+", Vendor = "+query[10]+", Invoice_IPO = "+query[11]+", PO_Registered = "+query[12]+", InControl_Expiration = "+query[13]+", Notes = "+query[14]+" WHERE Id="+query[0][1:-1]+"&cmdtype=write")


#selecting just one row doesn't work
