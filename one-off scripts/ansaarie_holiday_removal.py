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

driver=webdriver.Chrome("chromedriver path")
driver.get("https://voip.bluelinetelecom.com/login")
driver.find_element_by_name("username").send_keys("")
driver.find_element_by_name("password").send_keys("")
driver.find_element_by_name("password").send_keys(Keys.RETURN)
driver.get("customer url")
holidays=[[x.find_elements_by_css_selector("a")[0].get_attribute("href"),x.find_elements_by_css_selector("td")[2].text] for x in driver.find_elements_by_css_selector("#content-wrapper > div > div.box > div.box-content.box-no-padding.no-border > table > tbody > tr")]
for x in holidays:
    if x[1]!="January 1" and x[1]!="July 4" and x[1]!="July 3" and x[1]!="September 7" and x[1]!="November 26" and x[1]!="November 27" and x[1]!="December 24" and x[1]!="December 25" and x[1]!="December 31":
        driver.get(x[0])
        driver.find_element_by_css_selector("#content-wrapper > div > form > div:nth-child(4) > div > div > div > a.btn.btn-grey.btn-delete.js-delete.btn").click()
        time.sleep(1)
        driver.find_element_by_css_selector("#confirm-delete-button").click()
        time.sleep(1)
        
