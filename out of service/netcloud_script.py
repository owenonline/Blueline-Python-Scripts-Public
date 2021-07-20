from selenium import webdriver
import time
from time import sleep
import os
import pychromecast
from selenium.webdriver.chrome.options import Options
import random
import sys
sys.path.insert(1, 'email automation folder filepath')
from gmail_send import send_mail
#set up webdriver
options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
driver=webdriver.Chrome("chromedriver filepath",options=options)
#,options=options

imagename="default.png"

#set up chromecast
cast1=pychromecast.Chromecast('chromecast ip address')
cast1.wait()
mc1=cast1.media_controller

driver.get("https://www.cradlepointecm.com/ecm.html#devices/routers")
driver.find_element_by_css_selector("#ember5").send_keys("")
driver.find_element_by_css_selector("#ember8").send_keys("")
driver.find_element_by_css_selector("#ember10").click()
time.sleep(3)
driver.execute_script('window.open();')
driver.switch_to.window(driver.window_handles[0])

try:
    for x in driver.find_elements_by_css_selector("button"):
        if "pendo-close-guide-" in x.get_attribute("id"):
            x.click()
            print('nice')
except:
    pass

def alert(status):
    global imagename
    if status[0]=="online":
        mc1.play_media('server ip + filepath','video/mp4')
        print("green")
    else:
        mc1.play_media('server ip + filepath','video/mp4')
        time.sleep(3)
        print("red")
    mc1.play_media("server ip + port"+imagename,"image/png",autoplay=False)

    change=get_device_change(status[1])

    send_mail("customer email address","company automated email address","Device is now "+status[0],change,"")

    new_screenshot()

def get_device_statuses():
    statuses=[x.get_attribute("class")[:-5] for x in driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/div/div[5]/div/div[1]/div[3]/div/table/tbody/tr/td[2]/div/a/span")]
    ids=[x.get_attribute("onclick").split("'id=")[1].split("', '")[0] for x in driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/div/div[5]/div/div[1]/div[3]/div/table/tbody/tr/td[6]/div/div/div[1]/a")]
    device_statuses=[[statuses[x],ids[x]] for x in range(len(statuses))]
    return device_statuses

def new_screenshot():
    global imagename
    try:
        os.remove("C:\\inetpub\\wwwroot\\"+imagename)
    except:
        print('')
    x=random.randrange(0,1000000,1)
    imagename="count"+str(x)+".png"
    driver.save_screenshot("C:\\inetpub\\wwwroot\\"+imagename)

def get_device_change(device_id):
    driver.get('https://www.cradlepointecm.com/ecm.html#logs/alert_log?search=router_id%3D%22'+str(device_id)+'%22')
    run=False
    text_super=[]
    while run==False:
        try:
            text=[]
            for x in range(len(driver.find_elements_by_tag_name('div'))):
                if driver.find_elements_by_tag_name('div')[x].get_attribute("class")=="x-grid-cell-inner ":
                    text.append(driver.find_elements_by_tag_name('div')[x].text)
            run=True
            text_super=text
        except:
            continue
    
    text_super=list(filter(None,text_super))
    info=[]
    for x in text_super:
        if x!=' ':
            info.append(x)
    message=""
    for x in info:
        message=message+x+"\n"
    driver.get("https://www.cradlepointecm.com/ecm.html#devices/routers")
    return message
    

try:
    driver.find_element_by_css_selector("#pendo-close-guide-ee900bc0").click()
except:
    print('')
time.sleep(2)
device_statuses=get_device_statuses()
new_screenshot()
mc1.play_media("server ip address + port"+imagename,"image/png",autoplay=False)
while True:
    old_status=[y for y in device_statuses]
    z=False
    while z==False:
        try:
            device_statuses=get_device_statuses()
            z=True
        except:
            continue
    for x in range(len(device_statuses)):
        if device_statuses[x][0] != old_status[x][0]:
            alert(device_statuses[x])
    mc1.play_media("server ip address + port"+imagename,"image/png",autoplay=False)
    time.sleep(35)
    
