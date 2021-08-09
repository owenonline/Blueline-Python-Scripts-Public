from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import csv
import xlrd
import datetime
from datetime import datetime as dtt
import os
import pyautogui
import datetime
from selenium.webdriver.chrome.options import Options
import sys
sys.path.insert(1, 'C:\\Users\\rdp\\Documents\\GitHub\\Blueline-Python-Scripts\\email automation')
from gmail_auto import send_mail

#reference variables
dates={
    'Jan':'01',
    'Feb':'02',
    'Mar':'03',
    'Apr':'04',
    'May':'05',
    'Jun':'06',
    'Jul':'07',
    'Aug':'08',
    'Sep':'09',
    'Oct':'10',
    'Nov':'11',
    'Dec':'12'
}
target_items=['Single Static IP','Static IP Block','Managed Service Provider Fee','Managed Services - Broadband','Managed Services - Coax','Managed Services - Dedicated','Managed Services - Router','Managed Services - Satellite Service','Managed Services - TV']

#navigate to TMAS
options = Options()
#options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
#,options=options
driver=webdriver.Chrome("C:\\Users\\rdp\\Documents\\GitHub\\Blueline-Python-Scripts\\chromedriver.exe",options=options)
driver.get("https://customers.truechoicetech.com/login")
driver.find_element_by_css_selector("#text").send_keys("")
driver.find_element_by_css_selector("#password").send_keys("")
driver.find_element_by_css_selector("#app-layout > div.banner > div > div > div > div > div.panel-body > form > div.form-group.no-margin > div > button").click()
driver.get("https://customers.truechoicetech.com/billing")
time.sleep(5)

#only include bills due in current month and get all of them
driver.find_element_by_css_selector("#billdaterange").click()
driver.find_element_by_css_selector("#leads-changes > div.daterangepicker.dropdown-menu.opensleft.cls_bill_date_range > div.ranges > ul > li:nth-child(5)").click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/button").click()
dt=dtt.now()
time.sleep(2)

TMAS_info={}
def tmas():
    global dt
    try:
        book = xlrd.open_workbook("C:\\Users\\rdp\\Downloads\\Billing_"+dt.strftime("%Y-%m-%d %H_%M_%S")+".xls")
        sh = book.sheet_by_index(0)
        for rx in range(1,sh.nrows):
            name=sh.cell_value(rowx=rx, colx=1)
            provider=sh.cell_value(rowx=rx, colx=4)
            bill_date=sh.cell_value(rowx=rx, colx=5)
            bill_amount=sh.cell_value(rowx=rx, colx=8)
            bill_date=datetime.date.fromisoformat(bill_date.split(" ")[2]+'-'+dates[bill_date.split(" ")[0]]+'-'+bill_date.split(" ")[1][:2])
            if "Blueline" in name or "True Choice" in name or "Waste Pro" in name:
                #excluded entities
                continue
            TMAS_info[name]={
                'provider':provider,
                'bill date':bill_date,
                'bill amount':bill_amount
            }
    except:
        dt=dt-datetime.timedelta(0,1)
        tmas()

tmas()

#sign into coredial
driver.get("https://voip.bluelinetelecom.com/login")
driver.find_element_by_name("username").send_keys("")
driver.find_element_by_name("password").send_keys("")
driver.find_element_by_name("password").send_keys(Keys.RETURN)
time.sleep(5)

#coredial info's keys are the TMAS customer name for easy indexing, with the coredial name stored as a field
coredial_info={}
for customer in TMAS_info:
    #go to customer page
    driver.get("https://voip.bluelinetelecom.com/customer/customer")
    time.sleep(5)
    #turn customer name into char list. Input each character until there is only one or 0 matches, and then get either that one result or input one fewer character and navigate to the top result
    chars=list(customer)
    for y in range(len(chars)):
        if "4C" in customer:
            #4C special case
            driver.get("https://voip.bluelinetelecom.com/provider/102/customer/72180/home")
            break
        driver.find_element_by_css_selector("#searchBox").clear()
        driver.find_element_by_css_selector("#searchBox").send_keys(chars[:y])
        time.sleep(1)
        if len(driver.find_elements_by_css_selector("#standard > tbody > tr"))==1 and driver.find_element_by_css_selector('#standard > tbody > tr > td').text!="No Records Found":
            driver.find_element_by_css_selector("#standard > tbody > tr:nth-child(1) > td.sorting_1 > a").click()
            break
        elif driver.find_element_by_css_selector('#standard > tbody > tr > td').text=="No Records Found":
            driver.find_element_by_css_selector("#searchBox").clear()
            driver.find_element_by_css_selector("#searchBox").send_keys(chars[:y-1])
            time.sleep(1)
            driver.find_element_by_css_selector("#standard > tbody > tr:nth-child(1) > td.sorting_1 > a").click()
            break
        elif y==range(len(chars))[-1]:
            #if there are multiple names left after all the letters in the tmas name are entered, click the top name
            driver.find_element_by_css_selector("#standard > tbody > tr:nth-child(1) > td.sorting_1 > a").click()
    time.sleep(1)

    #go to the accounting tab
    driver.find_element_by_css_selector("body > div.tab-nav-bar2.navbar-collapse.collapse > div > div > ul > li:nth-child(5) > a").click()
    time.sleep(3)

    #find the first invoice with a date after the TMAS bill date and navigate to it
    saved=None
    saved_date=None
    for y in range(len(driver.find_elements_by_css_selector("#transaction_records > tr"))-1):
        date_str=driver.find_elements_by_css_selector('#transaction_records > tr > td:nth-child(1) > a')[y].text
        date=datetime.date.fromisoformat('20'+date_str.split('/')[2]+"-"+date_str.split('/')[0]+'-'+date_str.split('/')[1])
        ftype=driver.find_elements_by_css_selector('#transaction_records > tr > td:nth-child(2)')[y].text
        if date>=TMAS_info[customer]['bill date'] and ftype=="Invoice":
            saved=driver.find_elements_by_css_selector("#transaction_records > tr > td:nth-child(1) > a")[y].get_attribute("href")
            saved_date=date
        elif date<TMAS_info[customer]['bill date'] and saved:
            driver.get(saved)
            break
        elif date<TMAS_info[customer]['bill date'] and not saved and ftype=="invoice":
            #if there's no current invoice, get the most recent one instead
            saved=driver.find_elements_by_css_selector("#transaction_records > tr > td:nth-child(1) > a")[y].get_attribute("href")
            driver.get(saved)
            break
        elif y==range(len(driver.find_elements_by_css_selector("#transaction_records > tr"))-1)[-1] and saved!=None:
            #if the last iteration is reached and an invoice has been found but no earlier one has been found
            driver.get(saved)

    #get all the relevant charges and put them in a dictionary with the item names as keys
    charges={}
    total=0
    if saved!=None:
        for x in range(len(driver.find_elements_by_css_selector("#content-wrapper > div > form > div:nth-child(4) > div.box-content.box-overflow-fix > table > tbody > tr"))-1):
            text=driver.find_elements_by_css_selector("#content-wrapper > div > form > div:nth-child(4) > div.box-content.box-overflow-fix > table > tbody > tr > td:nth-child(3)")[x].text
            if text in target_items:
                if not text+'_0' in charges:
                    charges[text+"_0"]={
                        "quantity":driver.find_elements_by_css_selector("#content-wrapper > div > form > div:nth-child(4) > div.box-content.box-overflow-fix > table > tbody > tr > td:nth-child(1)")[x].text,
                        "charge":driver.find_elements_by_css_selector("#content-wrapper > div > form > div:nth-child(4) > div.box-content.box-overflow-fix > table > tbody > tr > td:nth-child(6)")[x].text
                    }
                else:
                    charges[text+"_"+str(sorted([int(key.split('_')[1]) for key in charges if key.startswith(text)])[-1]+1)]={
                        "quantity":driver.find_elements_by_css_selector("#content-wrapper > div > form > div:nth-child(4) > div.box-content.box-overflow-fix > table > tbody > tr > td:nth-child(1)")[x].text,
                        "charge":driver.find_elements_by_css_selector("#content-wrapper > div > form > div:nth-child(4) > div.box-content.box-overflow-fix > table > tbody > tr > td:nth-child(6)")[x].text
                    }
                total+=float(driver.find_elements_by_css_selector("#content-wrapper > div > form > div:nth-child(4) > div.box-content.box-overflow-fix > table > tbody > tr > td:nth-child(6)")[x].text.replace(',',''))
                
        coredial_info[customer]={
            'Coredial Name':driver.find_element_by_css_selector("#content-wrapper > div > form > div:nth-child(1) > div.box-content.box-overflow-fix > div:nth-child(1) > div:nth-child(1) > div > div").text,
            'Relevant Charges':charges,
            'Total':total,
            'Date':saved_date
        }
    else:
        #if no invoice
        coredial_info[customer]={
            'Coredial Name':driver.find_element_by_css_selector('#content-wrapper > div > h1 > span').text[16:],
            'Relevant Charges':"No Invoice",
            'Total':"No Invoice",
            'Date':"No Invoice"
        }

with open('C:\\Users\\rdp\\Documents\\GitHub\\Blueline-Python-Scripts\\production scripts\\data_files\\ISP Billing Data '+datetime.date.today().strftime("%b-%Y")+'.csv','w',newline='') as csvfile:
    writer=csv.writer(csvfile,dialect='excel')
    writer.writerow(['TMAS Name','Provider','TMAS Bill Date','TMAS Bill Amount','|||||','Coredial Name','Charge Info','Charge Total','Coredial Invoice Date'])
    for x in TMAS_info:
        writer.writerow([x,TMAS_info[x]['provider'],str(TMAS_info[x]['bill date']),TMAS_info[x]['bill amount'],'|||||',coredial_info[x]['Coredial Name'],coredial_info[x]['Relevant Charges'],coredial_info[x]['Total'],str(coredial_info[x]['Date'])])

send_mail("glao@bluelinetelecom.com","bluelinetelecom.python@gmail.com",'ISP Billing Data '+datetime.date.today().strftime("%b-%Y"),"",'C:\\Users\\rdp\\Documents\\GitHub\\Blueline-Python-Scripts\\production scripts\\data_files\\ISP Billing Data '+datetime.date.today().strftime("%b-%Y")+'.csv')
os.remove('C:\\Users\\rdp\\Documents\\GitHub\\Blueline-Python-Scripts\\production scripts\\data_files\\ISP Billing Data '+datetime.date.today().strftime("%b-%Y")+'.csv')
