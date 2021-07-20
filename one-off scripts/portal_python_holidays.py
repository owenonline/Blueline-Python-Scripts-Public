from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

driver=webdriver.Chrome("C:\\Users\\rdp\\Documents\\GitHub\\\Blueline-Python-Scripts\\chromedriver.exe")
driver.get("https://voip.bluelinetelecom.com/login")
driver.find_element_by_name("username").send_keys("")
driver.find_element_by_name("password").send_keys("")
driver.find_element_by_name("password").send_keys(Keys.RETURN)
print(".")
driver.get("https://voip.bluelinetelecom.com/customer/customer")
print(".")
driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/form/div[1]/div[1]/div[2]/span/button[4]").click()
driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[1]/div/div[1]/ul/li[5]/label/input").click()
driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[2]/span/button[2]").click()
print(".")
raw_elements=driver.find_elements_by_tag_name("a")
del raw_elements[0:69]
new_elements=[''.join([str(raw_elements[i].get_attribute("href"))[:len(str(raw_elements[i].get_attribute("href")))-9],"holiday"]) for i in range(len(raw_elements)) if "/service/extension" in str(raw_elements[i].get_attribute("href"))]
print(".")
driver.execute_script('window.open();');
driver.switch_to.window(driver.window_handles[1])
print(".")
correct_holidays=["January 1", "July 4", "November 11", "December 25"]

for x in new_elements:
    driver.get(x)
    wrong_dates=[]
    if driver.find_element_by_css_selector("#content-wrapper > div > div.box > div.box-content.box-no-padding.no-border > table > tbody > tr > td").text != "No Records Found":
        trs=[driver.find_elements_by_css_selector("#content-wrapper > div > div.box > div.box-content.box-no-padding.no-border > table > tbody > tr")]
        wrong_dates=["-".join([str(trs[0][i].find_element_by_xpath("./td[3]").text),str(trs[0][i].find_element_by_xpath("./td[2]/a").text)]) for i in range(len(trs[0])) if str(trs[0][i].find_element_by_xpath("./td[3]").text) not in correct_holidays]
        if len(wrong_dates) !=0:
            print(str(driver.find_element_by_xpath('/html/body/header/div[1]/div[4]/ul/li[2]/a/span').text))
            print(wrong_dates)
