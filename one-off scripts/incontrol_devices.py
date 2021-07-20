from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import csv

driver=webdriver.Chrome("chromedriver path")
driver.get("https://incontrol2.peplink.com/login?origin=https%3A%2F%2Fearth.ic.peplink.com%2Fo%2F48Pmn4%2Foverview")
time.sleep(1)
driver.find_element_by_name("email").send_keys("")
driver.find_element_by_name("password").send_keys("")
driver.find_element_by_id("loginBtn").click()
time.sleep(3)

driver.get("https://earth.ic.peplink.com/o/48Pmn4/n/1/overview")
time.sleep(3)
devices=[]
with open('blueline_info-desmond_not_done_devices.csv', newline='') as csvfile:
    reader=csv.reader(csvfile, dialect='excel')
    
    for row in reader:
        driver.find_element_by_css_selector("#table_search").send_keys(row)
        time.sleep(2)
        if not driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div/div[4]/div[1]/div[1]/div[5]/div[3]/div/div[1]/table/tbody/tr/td").text=="No matching records found":
            devices.append(driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div/div[4]/div[1]/div[1]/div[5]/div[3]/div/div[1]/table/tbody/tr/td[5]").text)
        else:
            devices.append("not in wealth")
        driver.find_element_by_css_selector("#table_search").clear()
with open('csv filepath',newline='') as csvfile2:
    writer=csv.reader(csvfile2,dialect='excel')
    for x in devices:
        writer.writerow(x)
