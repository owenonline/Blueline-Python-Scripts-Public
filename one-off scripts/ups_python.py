from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import pyautogui as pya
from tika import parser

driver=webdriver.Chrome("chromedriver filepath")
driver.get("speedship url")
time.sleep(1)
driver.find_element_by_css_selector("#P101_USERNAME").send_keys("")
driver.find_element_by_css_selector("#P101_PASSWORD").send_keys("")
driver.find_element_by_css_selector("#P101_LOGIN").click()
time.sleep(1)

def check_div():
    z=1
    if range(len(driver.find_elements_by_xpath("/html/body/div["+str(z)+"]/form/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td/div[1]/div[2]/div[2]/div[2]/div[4]/table/tbody/tr[2]/td/table/tbody/tr")))[1:]==range(0, 0):
        z=2
    return str(z)

driver.get(driver.find_element_by_css_selector("#qm0 > div:nth-child(2) > div > a:nth-child(1)").get_attribute('href'))
driver.find_element_by_xpath("/html/body/div["+check_div()+"]/form/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td/div[1]/div[2]/div[1]/div[1]/div/div[6]/select/option[14]").click()
driver.find_element_by_xpath("/html/body/div["+check_div()+"]/form/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td/div[1]/div[2]/div[1]/div[1]/div/div[3]/button/span").click()
time.sleep(2)
shipments=[]

for x in range(len(driver.find_elements_by_xpath("/html/body/div["+check_div()+"]/form/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td/div[1]/div[2]/div[2]/div[2]/div[4]/table/tbody/tr[2]/td/table/tbody/tr")))[1:]:
    driver.find_element_by_xpath("/html/body/div["+check_div()+"]/form/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td/div[1]/div[2]/div[2]/div[2]/div[4]/table/tbody/tr[2]/td/table/tbody/tr["+str(x+1)+"]/td[6]/table/tbody/tr[2]/td/a").click()
    time.sleep(1)
    tracking_num=driver.find_element_by_xpath("/html/body/div[1]/form/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[2]/div/div[1]/table[2]/tbody/tr[2]/td/div/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]").text
    entered_weight=driver.find_element_by_xpath("/html/body/div[1]/form/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[2]/div/div[1]/table[2]/tbody/tr[2]/td/div/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]").text
    billable_weight=driver.find_element_by_xpath("/html/body/div[1]/form/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[2]/div/div[1]/table[2]/tbody/tr[2]/td/div/table/tbody/tr[2]/td/table/tbody/tr[4]/td[2]").text
    dimensions=str.split(str.split(driver.find_element_by_xpath("/html/body/div[1]/form/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[2]/div/div[1]/table[2]/tbody/tr[3]/td/div/table/tbody/tr[3]/td[4]").text,'\n')[0],'x')
    estimated_cost=driver.find_element_by_xpath("/html/body/div[1]/form/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[2]/div/div[1]/table[2]/tbody/tr[5]/td/div/table/tbody/tr[3]/td/table/tbody/tr/td[2]/b").text
    shipments.append([tracking_num,entered_weight,billable_weight,dimensions,estimated_cost])
    driver.back()
    time.sleep(1)
    driver.find_element_by_xpath("/html/body/div["+check_div()+"]/form/table[1]/tbody/tr/td/table/tbody/tr[2]/td/table[2]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td/div[1]/div[2]/div[1]/div[1]/div/div[3]/button/span").click()
    time.sleep(2)


print("enter filepath of invoice pdf")
raw = parser.from_file(input())
pdf=str.split(str.split(raw['content'],"Original Charges")[1],"UPS No: ")[1:]

invoice_listings=[]
for x in pdf:
    tracking_num=str.split(x[0:18],'\n')[0]
    weight=str.split(x,"Payer")[1][2:4]
    try:
        weight=int(weight)
    except:
        weight="null"
    [list_price,discount_price]=str.split(str.split(str.split(x,"Total ")[1],"\n")[0],' ')
    invoice_listings.append([tracking_num,weight,list_price,discount_price])

common_orders=[x for x in shipments if x[0] in [y[0] for y in invoice_listings]]
for x in common_orders:
    [list_price,discount_price]=invoice_listings[[y[0] for y in invoice_listings].index(x[0])][2:4]
    print(x[0]+": ")
    if list_price>x[4]:
        print("\tList Price is greater than estimated cost")
    else:
        print("\tList Price is lower than estimated cost")
    if discount_price>x[4]:
        print("\tDiscount Price is greater than estimated cost")
    else:
        print("\tDiscount Price is lower than estimated cost")
    print("\n")
