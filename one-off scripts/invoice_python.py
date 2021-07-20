import pyperclip
import pyautogui as pya
from tika import parser
import csv
import re
from geotext import GeoText
with open('template.csv','w',newline='') as csvfile:
    writer=csv.writer(csvfile,dialect='excel')
    writer.writerow(['','Non-recurring charges','Recurring Charges','Fees','Total'])
    print("enter filepath of invoice pdf")
    raw = str(parser.from_file(input()))
    raw=raw.replace("\\n","|")
    mrc=raw.split("Item # QTY Name Description Amount Ext. Amount")[1].split("Total Monthly Recurring Charges")[0]
    nrc=raw.split("Item # QTY Name Description Amount Ext. Amount")[2].split("Taxes and Fees")[0]
    fees=raw.split("Item # Amount")[1].split("Calling Summary")[0]
    #garbage disposal
    raw=0
    ##SEPARATE MRC INTO ITEMS
    ##regex find strings of || followed by 3 nums then - and 2 numbers and -
    x=re.findall("\|\|...-..-",mrc)
    y=[0,mrc]
    for z in x:
        if z in y[-1]:
            d=y[:-1]
            d.append(str(y[-1]).split(z,1)[0])
            if str(y[-1]).split(z,1)[1]!='':
                d.append(str(y[-1]).split(z,1)[1])
            y=d
    separated_mrc=[]
    y=y[2:]
    for d in range(len(y)):
        separated_mrc.append(x[d]+y[d])


    #in case the pdf is weird and adds the billing info to one of the mrc items this removes it
    for x in range(len(separated_mrc)):
        if "Account Number" in separated_mrc[x]:
            separated_mrc[x]=separated_mrc[x].replace(re.findall("\|\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|\|[^|]*\|[^|]*\|\|[^|]*\|[^|]*\|\|",separated_mrc[x])[0],'')
            

    ##SEPARATE NRC INTO ITEMS
    x=re.findall("\|\|...-..-",nrc)
    y=[0,nrc]
    for z in x:
        if z in y[-1]:
            d=y[:-1]
            d.append(str(y[-1]).split(z,1)[0])
            if str(y[-1]).split(z,1)[1]!='':
                d.append(str(y[-1]).split(z,1)[1])
            y=d
    separated_nrc=[]
    y=y[2:]
    for d in range(len(y)):
        separated_nrc.append(x[d]+y[d])

    ##SEPARATE FEES
    #regex finds the .##|| at the end of each fee line
    x=re.findall("\...\|\|",fees)
    y=[0,fees]
    for z in x:
        if z in y[-1]:
            d=y[:-1]
            d.append(str(y[-1]).split(z,1)[0])
            if str(y[-1]).split(z,1)[1]!='':
                d.append(str(y[-1]).split(z,1)[1])
            y=d
    separated_fees=[]
    y=y[1:]
    for d in range(len(y)):
        separated_fees.append(y[d]+x[d])

    #this code gets city names from the different things
    locations=[]

    for x in separated_mrc:
        places=GeoText(x.title())
        for y in places.cities:
            locations.append(y)
                
    for x in separated_nrc:
        places=GeoText(x.title())
        for y in places.cities:
            locations.append(y)

    for x in separated_fees:
        places=GeoText(x.title())
        for y in places.cities:
            locations.append(y)

    #removes duplicates and non-city names
    locations=list(dict.fromkeys(locations))
    locations=[x for x in locations if x!="Of" and x!="Date"]

    #gets any names that weren't caught the first time cause of a bug that prevents 1 words names from getting notices by geotext sometimes
    split_locations=[]
    for z in locations:
        z=z.split(" ")
        for d in z:
            split_locations.append(d)

    for x in separated_mrc:
        x=x.split(" ")
        x=[y for y in x if y.title() not in split_locations]
        for y in x:
            places=GeoText(y.title())
            for z in places.cities:
                if z=="York":
                    print(x)
                locations.append(z)

    for x in separated_nrc:
        x=x.split(" ")
        x=[y for y in x if y.title() not in split_locations]
        for y in x:
            places=GeoText(y.title())
            for z in places.cities:
                locations.append(z)

    for x in separated_fees:
        x=x.split(" ")
        x=[y for y in x if y.title() not in split_locations]
        for y in x:
            places=GeoText(y.title())
            for z in places.cities:
                locations.append(z)

    locations=list(dict.fromkeys(locations))
    locations=[x for x in locations if x!="Of" and x!="Date"]

    #creates the data strcuture for organizing costs by location
    locations_data=[[x,[["mrc",[0]],["nrc",[0]],["fees",[0]]]] for x in locations]

    #adds the costs to the locations
    for x in separated_mrc:
        location=""
        for y in locations:
            if y in x.title():
                location=y
                continue
        cost=float(re.search("\....\$.*\...",x)[0][5:].replace(',',''))
        for y in locations_data:
            if y[0]==location:
                y[1][0][1][0]+=cost

    for x in separated_nrc:
        location=""
        for y in locations:
            if y in x.title():
                location=y
                continue
        cost=float(re.search("\....\$.*\...",x)[0][5:].replace(',',''))
        for y in locations_data:
            if y[0]==location:
                y[1][1][1][0]+=cost

    for x in separated_fees:
        location=""
        for y in locations:
            if y in x.title():
                location=y
                continue
        cost=float(re.search("\$.*\...",x)[0][1:].replace(',',''))
        for y in locations_data:
            if y[0]==location:
                y[1][2][1][0]+=cost  

    for x in locations_data:
        print(x[0]+"\n\t"+x[1][0][0]+": "+str(x[1][0][1][0])+"\n\t"+x[1][1][0]+": "+str(x[1][1][1][0])+"\n\t"+x[1][2][0]+": "+str(x[1][2][1][0])+"\n")

        
    for x in locations_data:
        writer.writerow([x[0],x[1][1][1][0],x[1][0][1][0],x[1][2][1][0],(x[1][1][1][0]+x[1][0][1][0]+x[1][2][1][0])])

    totals=[0,0,0]
    for x in locations_data:
        totals[0]=totals[0]+x[1][1][1][0]
        totals[1]=totals[1]+x[1][0][1][0]
        totals[2]=totals[2]+x[1][2][1][0]

    writer.writerow(["Totals",totals[0],totals[1],totals[2],(totals[0]+totals[1]+totals[2])])
