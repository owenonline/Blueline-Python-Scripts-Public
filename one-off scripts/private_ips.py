from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from time import sleep
from selenium.webdriver.chrome.options import Options
import csv
import urllib
import urllib.request
import requests

dhcp=0

driver=webdriver.Chrome("chromedriver path")
driver.get("https://earth.ic.peplink.com/o/48Pmn4/overview")
driver.find_element_by_css_selector("#username").send_keys("")
driver.find_element_by_css_selector("#next").click()
time.sleep(1)
driver.find_element_by_css_selector("#password").send_keys("")
driver.find_element_by_css_selector("#form-login > div.sign-up.col-12.mb-3 > div > button").click()
time.sleep(2)

with open("internal csv path",newline='') as csvfile:
    csvr=csv.reader(csvfile,dialect='excel')
    x=0
    for row in csvr:
        if x==0:
            x+=1
            continue
        driver.get(row[-1])
        time.sleep(2)
        links=[x.get_attribute('href') for x in driver.find_elements_by_xpath("/html/body/div[1]/div[2]/div[3]/div/div[4]/div[1]/div[1]/div[5]/div[3]/div/div[1]/table/tbody/tr/td[2]/div/a")]
        for link in links:
            driver.get(link)
            time.sleep(2)
            try:
                if "DHCP" in driver.find_element_by_css_selector("#iface_1_conn_method").get_attribute("textContent"):
                    dhcp+=1
            except:
                pass
            print(dhcp)
