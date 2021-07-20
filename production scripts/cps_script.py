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

chrome_options = Options()
chrome_options.add_argument("--headless")

def refresh():
    send_mail("my personal email address","company automated email address","test","test","")

def alert(agent,status):
    send_mail("sales rep email address, customer email address","company automated email address",agent+" is now "+status,agent+" is now "+status,"")
    
driver=webdriver.Chrome("chromedriver filepath",options=chrome_options)
#,options=chrome_options
driver.get("https://voip.bluelinetelecom.com/login")
driver.find_element_by_name("username").send_keys("")
driver.find_element_by_name("password").send_keys("")
driver.find_element_by_name("password").send_keys(Keys.RETURN)
time.sleep(1)
driver.get("https://voip.bluelinetelecom.com/customer/11362/report/acd/real-time-console")
time.sleep(1)
agent_status_old=[[x.find_elements_by_css_selector("td")[0].text,x.find_elements_by_css_selector("td")[1].text] for x in driver.find_elements_by_css_selector("#content-wrapper > div > div:nth-child(7) > div.box-content.box-no-padding.no-border > div > div > table > tbody > tr")]
driver.execute_script('window.open();')
driver.switch_to.window(driver.window_handles[0])
while True:
    driver.get("https://voip.bluelinetelecom.com/customer/11362/report/acd/real-time-console")
    time.sleep(1)
    agent_status_new=[[x.find_elements_by_css_selector("td")[0].text,x.find_elements_by_css_selector("td")[1].text] for x in driver.find_elements_by_css_selector("#content-wrapper > div > div:nth-child(7) > div.box-content.box-no-padding.no-border > div > div > table > tbody > tr")]
    agent_status_new.sort(key=lambda x: x[0])
    agent_status_old.sort(key=lambda x: x[0])
    agent_status_new=[agent_status_new[[int(x[0].split('(')[1].split(')')[0]) for x in agent_status_new].index(y)] for y in [int(x[0].split('(')[1].split(')')[0]) for x in agent_status_new] if y in [139,143,158,313,114]]
    agent_status_old=[agent_status_old[[int(x[0].split('(')[1].split(')')[0]) for x in agent_status_old].index(y)] for y in [int(x[0].split('(')[1].split(')')[0]) for x in agent_status_old] if y in [139,143,158,313,114]]
    for x in range(len(agent_status_new)):
        if agent_status_new[x][1] != agent_status_old[x][1] and agent_status_new[x][0] == agent_status_old[x][0]:
            alert(agent_status_new[x][0],agent_status_new[x][1])
            print("alert sent")
        if agent_status_new[x][0] != agent_status_old[x][0]:
            print("list changed length")
            print(agent_status_old)
            print(agent_status_new)
    agent_status_old=agent_status_new
    time.sleep(5)
