from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

driver=webdriver.Chrome("chromedriver path")
driver.get("https://incontrol2.peplink.com/login?origin=https%3A%2F%2Fearth.ic.peplink.com%2Fo%2F48Pmn4%2Foverview")
driver.find_element_by_name("email").send_keys("")
driver.find_element_by_name("password").send_keys("")
driver.find_element_by_id("loginBtn").click()


driver2=webdriver.Chrome("C:\\Users\\rdp\\Documents\\GitHub\\\Blueline-Python-Scripts\\chromedriver.exe")
driver2.get("https://voip.bluelinetelecom.com/login")
driver2.find_element_by_name("username").send_key=("")
driver2.find_element_by_name("password").send_keys("")
driver2.find_element_by_name("password").send_keys(Keys.RETURN)

driver2.get("https://voip.bluelinetelecom.com/customer/customer")
driver.get("https://earth.ic.peplink.com/o/48Pmn4/n/1/overview")

driver.get("https://earth.ic.peplink.com/o/48Pmn4/n/1/overview")

for y in range(10): 
    
    time.sleep(1)
    raw_elements=driver.find_elements_by_tag_name("a")

    elements=[]
    z="/o/48Pmn4/n/1/d/"
    for x in raw_elements:
        if z in str(x.get_attribute("href")):
            elements.append(str(x.get_attribute("href")))
            
    driver.execute_script('window.open();');
    driver.switch_to.window(driver.window_handles[1])
    for row in elements:
        driver.get(row)
        time.sleep(1)

        driver2.find_element_by_name("searchTerms").clear()
        driver2.find_element_by_name("searchTerms").send_keys(driver.find_element_by_id("device_name").text)
        driver2.find_element_by_name("searchTerms").send_keys(Keys.RETURN)

        time.sleep(1)
    
        if not "No Records Found" in driver2.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/form/div[1]/div[2]/div/div[1]/div[2]/table/tbody/tr/td").text:
        
            portal_link=str(driver2.find_element_by_id("standard").find_element_by_xpath('/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/form/div[1]/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[2]/a').get_attribute('href'))

            driver.find_element_by_id("edit_devinfo_button").click()
            time.sleep(5)
            textbox=driver.find_element_by_tag_name("textarea")
            textbox.click()
            for z in range(10):
                textbox.send_keys(Keys.PAGE_DOWN)
            textbox.send_keys(Keys.RETURN)
            textbox.send_keys(str("Customer Portal: "+portal_link))
        
            driver.find_element_by_id("save_devinfo_button").click()
            print(portal_link)

        driver2.get("https://voip.bluelinetelecom.com/customer/customer")

    driver.switch_to.window(driver.window_handles[0])
    if y < 10:
        driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div/div[4]/div[1]/div[1]/div[5]/div[3]/div/div[2]/div/a[3]").click()
