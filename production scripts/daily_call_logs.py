from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import csv
import datetime
import os
import pyautogui
from selenium.webdriver.chrome.options import Options
import sys
sys.path.insert(1, 'email automation folder filepath')
from gmail_auto import send_mail

options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
#,options=options
driver=webdriver.Chrome("chromedriver filepath")

driver.get("https://voip.bluelinetelecom.com/login")
driver.find_element_by_name("username").send_keys("")
driver.find_element_by_name("password").send_keys("")
driver.find_element_by_name("password").send_keys(Keys.RETURN)
time.sleep(1)

#get today's date
today=datetime.datetime.now()
day=""
if len(str(today.day))<2:
    day="0"+str(today.day)
else:
    day=str(today.day)

#get the date however long ago we need to look back    
time_ago=datetime.datetime.now()-datetime.timedelta(days=1)
old_day=""
if len(str(time_ago.day))<2:
    old_day="0"+str(time_ago.day)
else:
    old_day=str(time_ago.day)
#download the log covering that period
driver.get("https://voip.bluelinetelecom.com/customer/60830/report/activity/asterisk?reset=0&searchTerms=&start_date="+str(time_ago.month)+"%2F"+old_day+"%2F"+str(time_ago.year)+"&end_date="+str(today.month)+"%2F"+day+"%2F"+str(today.year)+"&callType=5&filterBy=&didId=631409&timezone=America%2FNew_York&do_export=&export_download=c8132c5c1ec8d8e7")
try:
    driver.find_element_by_css_selector("#export_btn").click()
except:
    driver.execute_script("return document.getElementsByClassName('modal global-alert-modal ng-scope overlay')[0].remove();")
    driver.find_element_by_css_selector("#export_btn").click()
time.sleep(1)
driver.get("https://voip.bluelinetelecom.com/customer/60830/service/extension")

#write the new log
with open('call activity csv filepath'+str(today.year)+'_'+str(today.month)+'_'+day+'.csv',newline='') as exported:
    export_reader=csv.reader(exported,dialect='excel')
    #delete the old log
    try:
        os.remove("old log filepath")
    except:
        pass
    with open('new log filepath','w',newline='') as export:
        #today_date=datetime.datetime(int(today.year),int(today.month),int(day))
        export_writer=csv.writer(export,dialect='excel')
        export_writer.writerow(next(export_reader, None))
        for row in export_reader:
            if row[-1]!="":
                try:
                    try:
                        driver.find_element_by_css_selector("#searchBox").send_keys(row[-1])
                    except:
                        driver.execute_script("return document.getElementsByClassName('modal global-alert-modal ng-scope overlay')[0].remove();")
                        driver.find_element_by_css_selector("#searchBox").send_keys(row[-1])
                    driver.find_element_by_css_selector("#searchBox").send_keys(Keys.RETURN)
                    time.sleep(1)
                    print(driver.find_element_by_css_selector("#standard > tbody > tr > td:nth-child(4)").text)
                    row[-1]=driver.find_element_by_css_selector("#standard > tbody > tr > td:nth-child(4)").text
                except:
                    print("this extension doesn't exist")
            export_writer.writerow(row)
            driver.find_element_by_css_selector("#searchBox").clear()
        send_mail("sales rep email address, customer email address","company automated email address","Call Logs for "+str(time_ago.month)+"-"+old_day+"-"+str(time_ago.year)+" to "+str(today.month)+"-"+day+"-"+str(today.year),"","C:\\Users\\rdp\\Documents\GitHub\\Blueline-Python-Scripts\\production scripts\\data_files\\new_log.csv")
