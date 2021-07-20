from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

driver=webdriver.Chrome("chromedriver path")
driver.get("https://voip.bluelinetelecom.com/login")
driver.find_element_by_name("username").send_keys("")
driver.find_element_by_name("password").send_keys("")
driver.find_element_by_name("password").send_keys(Keys.RETURN)

driver.get("customer url")

time.sleep(3)

raw_elements=[driver.find_elements_by_tag_name("a")[x].get_attribute("href") for x in range(len(driver.find_elements_by_tag_name("a")))]
elements=[str(raw_elements[x]) for x in range(len(raw_elements)) if "/extension/" in str(raw_elements[x])]
elements=[str(elements[x]) for x in range(len(elements)) if "/standard" not in str(elements[x])]
elements=[str(elements[x]) for x in range(len(elements)) if "/cloud" not in str(elements[x])]
elements=[str(elements[x]) for x in range(len(elements)) if "/import-export" not in str(elements[x])]
elements=[str(elements[x]) for x in range(len(elements)) if "?" not in str(elements[x])]
elements=list(set(elements))

del elements[:118]
del elements[:23]
for x in elements:
    driver.get(x)
    time.sleep(2)
    driver.find_element_by_css_selector("#endpoint_tab_link").click()
    time.sleep(2)
    for x in range(len(driver.find_elements_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/form/div[4]/div[2]/div/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr/td[4]/input"))):
        if "erica" in driver.find_elements_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/form/div[4]/div[2]/div/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr/td[4]/input")[x].get_attribute("value").lower():
            driver.find_elements_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/form/div[4]/div[2]/div/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr/td[4]/input")[x].send_keys("Dagmar")
        elif "dagmar" in driver.find_elements_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/form/div[4]/div[2]/div/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr/td[4]/input")[x].get_attribute("value").lower():
            driver.find_elements_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/form/div[4]/div[2]/div/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr/td[4]/input")[x].send_keys("Erica")
    driver.find_element_by_css_selector("#extForm > div:nth-child(12) > div > div > div > button").click()
    time.sleep(3)
