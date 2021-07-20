from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from time import sleep
driver=webdriver.Chrome("")
driver.get("https://voip.bluelinetelecom.com/login")
time.sleep(1)
driver.find_element_by_name("username").send_keys("")
driver.find_element_by_name("password").send_keys("")
driver.find_element_by_name("password").send_keys(Keys.RETURN)
time.sleep(1)
driver.get("https://voip.bluelinetelecom.com/customer/76551/service/extension")
time.sleep(2)

links=['https://voip.bluelinetelecom.com/customer/76551/service/extension/852261', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852262', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852263', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852267', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852268', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852264', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852266', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852265', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852270', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852269', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851789', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851899', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851903', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851907', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851912', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851918', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851920', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851922', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851923', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851924', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851925', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851927', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851928', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851951', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851952', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851953', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851954', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851955', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851956', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851931', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851932', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851936', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851935', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851933', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851934', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851938', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851937', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851939', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851942', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851941', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851940', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851943', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851944', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851948', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851945', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851946', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851947', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851949', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851950', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851958', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851979', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851980', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851981', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851982', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851983', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851984', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852010', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852011', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852013', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852014', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852015', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852016', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852017', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852018', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852019', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852021', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852022', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852023', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852024', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851959', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851960', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851962', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851963', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851964', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851961', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851965', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851966', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851967', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851968', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851969', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851972', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851970', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851973', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851974', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851971', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851976', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851978', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851975', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851977', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852025', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852026', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852027', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852040', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852047', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852051', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852057', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852059', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852060', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852062', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852075', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852078', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852079', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852081', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852086', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852092', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852105', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852108', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852110', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852112', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851987', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851988', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851989', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851991', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851992', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851990', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851993', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851994', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851996', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851995', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851997', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851998', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/851999', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852002', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852000', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852001', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852003', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852005', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852004', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852006', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852180', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852181', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852178', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852179', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852182', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852183', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852184', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852185', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852186', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852188', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852187', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852191', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852189', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852190', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852192', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852193', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852194', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852195', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852196', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852197', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852028', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852064', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852031', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852029', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852033', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852030', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852065', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852044', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852045', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852046', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852066', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852067', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852038', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852068', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852069', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852070', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852072', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852074', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852073', 'https://voip.bluelinetelecom.com/customer/76551/service/extension/852039']

def error_wrap(func):
    unsuccessful=True
    while unsuccessful:
        try:
            func
            unsuccessful=False
        except:
            time.sleep(1)
            pass
for x in links[159:]:
    driver.get(x)
    time.sleep(10)
    driver.find_element_by_css_selector("#endpoint_tab_link").click()
    lines=len(driver.find_elements_by_xpath("/html/body/div[3]/div/div/div[2]/div/div/section/div/div/div/form/div[4]/div[2]/div/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr"))
    print(lines)
    for x in range(lines):
        try:
            driver.find_element_by_css_selector("#delete_line_2").click()
        except:
            break


    #blank
    driver.find_element_by_css_selector("#add_line_key").click()
    driver.find_element_by_css_selector("#line_type_2 > option:nth-child(4)").click()

    #blank
    driver.find_element_by_css_selector("#add_line_key").click()
    driver.find_element_by_css_selector("#line_type_3 > option:nth-child(4)").click()

    #blank
    driver.find_element_by_css_selector("#add_line_key").click()
    driver.find_element_by_css_selector("#line_type_4 > option:nth-child(4)").click()

    #blank
    driver.find_element_by_css_selector("#add_line_key").click()
    driver.find_element_by_css_selector("#line_type_5 > option:nth-child(4)").click()

    #extension blf
    driver.find_element_by_css_selector("#add_line_key").click()
    driver.find_element_by_css_selector("#line_type_6 > option:nth-child(2)").click()
    driver.find_element_by_css_selector("#line_value_6 > option:nth-child(12)").click()
    driver.find_element_by_css_selector("#line_label_6").send_keys("Front Desk")

    #extension blf
    driver.find_element_by_css_selector("#add_line_key").click()
    driver.find_element_by_css_selector("#line_type_7 > option:nth-child(2)").click()
    driver.find_element_by_css_selector("#line_value_7 > option:nth-child(12)").click()
    driver.find_element_by_css_selector("#line_label_7").send_keys("Restaurant")

    #blank
    driver.find_element_by_css_selector("#add_line_key").click()
    driver.find_element_by_css_selector("#line_type_8 > option:nth-child(4)").click()

    #blank
    driver.find_element_by_css_selector("#add_line_key").click()
    driver.find_element_by_css_selector("#line_type_9 > option:nth-child(4)").click()

    #speed dial
    driver.find_element_by_css_selector("#add_line_key").click()
    driver.find_element_by_css_selector("#line_type_10 > option:nth-child(5)").click()
    driver.find_element_by_css_selector("#line_value_10").send_keys("911")
    driver.find_element_by_css_selector("#line_label_10").send_keys("EMERGENCY")

    driver.find_element_by_css_selector("#extForm > div:nth-child(12) > div > div > div > button").click()
    time.sleep(2)
