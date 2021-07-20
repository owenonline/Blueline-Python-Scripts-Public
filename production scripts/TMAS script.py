from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import time
import csv
from datetime import date
import sys
sys.path.insert(1, 'email automation folder filepath')
from gmail_auto import send_mail

options=Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
#,options=options
driver=webdriver.Chrome("chromedriver filepaeth")
driver.get("https://customers.truechoicetech.com/login")
driver.find_element_by_css_selector("#text").send_keys("")
driver.find_element_by_css_selector("#password").send_keys("")
driver.find_element_by_css_selector("#app-layout > div.banner > div > div > div > div > div.panel-body > form > div.form-group.no-margin > div > button").click()
driver.get("https://customers.truechoicetech.com/billing")
colors = [x.get_attribute("style") for x in driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div[2]/div[3]/div/table/tbody/tr/td[8]/a")]

variances=[]
time.sleep(2)

for x in range(len(driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div[2]/div[3]/div/table/tbody/tr/td[8]/a"))):
    if driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div[2]/div[3]/div/table/tbody/tr/td[8]/a")[x].get_attribute("style")=="color: red;":
        variances.append([driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div[2]/div[3]/div/table/tbody/tr/td[1]/a")[x].text,driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div[2]/div[3]/div/table/tbody/tr/td[8]/a")[x].text])


with open("C:\\Users\\rdp\\Documents\\GitHub\\Blueline-Python-Scripts\\production scripts\\data_files\\week_of_"+str(date.today())+"_TMAS_variances.csv",'w',newline='') as csvfile:
    writer=csv.writer(csvfile, dialect='excel')
    for x in variances:
        writer.writerow(x)

send_mail("accountancy worker email address, accountancy worker email address","company automated email address","TMAS variances for the week of "+str(date.today()),"","C:\\Users\\rdp\\Documents\\GitHub\\Blueline-Python-Scripts\\production scripts\\data_files\\week_of_"+str(date.today())+"_TMAS_variances.csv")
