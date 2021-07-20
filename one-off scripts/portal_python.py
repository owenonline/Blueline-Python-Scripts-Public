from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import csv

with open('staff csv filepath', 'w', newline='') as csvfile:
    
    csvwriter=csv.writer(csvfile, dialect='excel')

    driver2=webdriver.Chrome("chromedriver filepath")
    driver2.get("https://voip.bluelinetelecom.com/login")
    driver2.find_element_by_name("username").send_keys("")
    driver2.find_element_by_name("password").send_keys("")
    driver2.find_element_by_name("password").send_keys(Keys.RETURN)

    driver2.get("https://voip.bluelinetelecom.com/customer/11288/setting/manage-users/user")
    driver2.execute_script("window.open('https://voip.bluelinetelecom.com/customer/11288/service/extension/standard')")
    driver2.execute_script("window.open('https://voip.bluelinetelecom.com/customer/11288/service/phone-number/standard?pageNumber=1&recordsPerPage=100')")
    csvwriter.writerow(["name","extension","did"])
    for x in driver2.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/div[2]/div[2]/table/tbody").find_elements_by_xpath('./tr'):
        name=""
        extension=""
        DID=""
        driver2.switch_to.window(driver2.window_handles[0])
        name=x.find_element_by_xpath('//td[4]').text
        driver2.switch_to.window(driver2.window_handles[2])
        for y in driver2.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/div[9]/div[2]/div[1]/div[1]/div[2]/table/tbody").find_elements_by_xpath('./tr'):
            if y.find_element_by_xpath('//td[3]').text == name:
                extension=y.find_element_by_xpath('//td[3]/a[0]').text
                driver2.switch_to.window(driver2.window_handles[1])
                for z in driver2.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/div[3]/div[2]/table/tbody").find_elements_by_xpath('./tr'):
                    if extension in z.find_element_by_xpath('//td[4]/a[0]').text:
                        DID=z.find_element_by_xpath('//td[2]/a').text
        csvwriter.writerow([name,extension,DID])
        
                        
        
