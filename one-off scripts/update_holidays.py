from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

driver=webdriver.Chrome("chromedriver path")
driver.get("https://voip.bluelinetelecom.com/login")
driver.find_element_by_name("username").send_keys("")
driver.find_element_by_name("password").send_keys("")
driver.find_element_by_name("password").send_keys(Keys.RETURN)

driver.get("https://voip.bluelinetelecom.com/customer/customer")

driver.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/form/div[1]/div[1]/div[2]/span/button[4]").click()
driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[1]/div/div[1]/ul/li[5]/label/input").click()
driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[2]/span/button[2]").click()

raw_elements=driver.find_elements_by_tag_name("a")
del raw_elements[0:69]
new_elements=[''.join([str(raw_elements[i].get_attribute("href"))[:len(str(raw_elements[i].get_attribute("href")))-9],"holiday"]) for i in range(len(raw_elements)) if "/service/extension" in str(raw_elements[i].get_attribute("href"))]

driver.execute_script('window.open();')
driver.switch_to.window(driver.window_handles[1])

correct_holidays=["January 1", "July 4", "November 11", "December 25"]

###this list should be updated to have the correct holiday dates for that year in the order Thanksgiving, Labor Day, Memorial Day
current_dates=[["November",25],["September",6],["May",31]]
###

for x in new_elements:
    driver.get(x)
    wrong_dates=[]
    if driver.find_element_by_css_selector("#content-wrapper > div > div.box > div.box-content.box-no-padding.no-border > table > tbody > tr > td").text != "No Records Found":
        trs=[driver.find_elements_by_css_selector("#content-wrapper > div > div.box > div.box-content.box-no-padding.no-border > table > tbody > tr")]
        wrong_dates=[[str(trs[0][i].find_element_by_xpath("./td[2]/a").get_attribute('href')),str(trs[0][i].find_element_by_xpath("./td[2]/a").text)] for i in range(len(trs[0])) if str(trs[0][i].find_element_by_xpath("./td[3]").text) not in correct_holidays]
        for x in wrong_dates:
            if "thanksgiving" in x[1].lower():
                driver.get(x[0])
                
                month=Select(driver.find_element_by_id("month"))
                month.select_by_visible_text(current_dates[0][0])
                
                day=Select(driver.find_element_by_id("day"))
                day.select_by_visible_text(str(current_dates[0][1]))

                driver.find_element_by_css_selector("#content-wrapper > div > form > div:nth-child(6) > div > div > div > button").click()
            if "labor day" in x[1].lower():
                driver.get(x[0])
                
                month=Select(driver.find_element_by_id("month"))
                month.select_by_visible_text(current_dates[1][0])
                
                day=Select(driver.find_element_by_id("day"))
                day.select_by_visible_text(str(current_dates[1][1]))
                
                driver.find_element_by_css_selector("#content-wrapper > div > form > div:nth-child(6) > div > div > div > button").click()
            if "memorial day" in x[1].lower():
                driver.get(x[0])
                
                month=Select(driver.find_element_by_id("month"))
                month.select_by_visible_text(current_dates[2][0])
                
                day=Select(driver.find_element_by_id("day"))
                day.select_by_visible_text(str(current_dates[2][1]))

                driver.find_element_by_css_selector("#content-wrapper > div > form > div:nth-child(6) > div > div > div > button").click()

        print(wrong_dates)
        
            
