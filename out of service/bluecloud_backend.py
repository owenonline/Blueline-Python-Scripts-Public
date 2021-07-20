from selenium import webdriver
import time
from time import sleep
import os
from selenium.webdriver.chrome.options import Options
import csv
import string
import random
import flask
from flask import request, jsonify
import asyncio
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import sqlite3
from sqlite3 import Error
import sys
sys.path.insert(1, 'email automation folder filepath')
from gmail_auto import send_mail
from gmail_auto import get_messages
from gmail_auto import get_content
from gmail_auto import file_message
import bs4
from bs4 import BeautifulSoup

app=flask.Flask(__name__)
active_eventkeys={
    "events":[],
    "incontrol_bandwidth":[],
    "incontrol_offline":[]
}
options = Options()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
driver=webdriver.Chrome("chromedriver filepath",options=options)



################################################################
#  _____  ____  _        __  __      _   _               _     #
# / ____|/ __ \| |      |  \/  |    | | | |             | |    #
#| (___ | |  | | |      | \  / | ___| |_| |__   ___   __| |___ #
# \___ \| |  | | |      | |\/| |/ _ \ __| '_ \ / _ \ / _` / __|#
# ____) | |__| | |____  | |  | |  __/ |_| | | | (_) | (_| \__ \#
#|_____/ \___\_\______| |_|  |_|\___|\__|_| |_|\___/ \__,_|___/#
################################################################

def create_connection(path):
    #creates the initial connection to the SQL server
    connection=None
    try:
        connection=sqlite3.connect(path)
        print("done")
    except Error as e:
        print(f"The error '{e}' has occurred")
    return connection

def execute_query(query):
    #sends an action query to the SQL server
    connection=create_connection("database filepath")
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        #connection.close()
        print("done")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(query):
    #sends a read only query to the SQL server
    connection=create_connection("database filepath")
    cursor=connection.cursor()
    result=None
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        #connection.close()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def id_file(table='',status='',name='',change=''):
    #creates an eventkey for the alert and puts it in the correct table, then adds the whole event to the correct sql table
    eventkey=''.join(random.choice(string.ascii_letters) for i in range(20))
    while eventkey in active_eventkeys[table]:
        eventkey=''.join(random.choice(string.ascii_letters) for i in range(20))
    active_eventkeys[table].append(eventkey)
    if name=='':
        add="""
        INSERT INTO
            events (status, readout, id)
        VALUES
            ('{status}','{readout}','{key}');
        """.format(status=status,readout=change,key=eventkey)
        execute_query(add)
    else:
        add="""
        INSERT INTO
            '{table}' (status, name, readout, id)
        VALUES
            ('{status}','{name}','{readout}','{key}');
        """.format(table=table,status=status,name=name,readout=change,key=eventkey)
        execute_query(add)

#################################################
#          _____ _____    _____          _      #
#    /\   |  __ \_   _|  / ____|        | |     #
#   /  \  | |__) || |   | |     ___   __| | ___ #
#  / /\ \ |  ___/ | |   | |    / _ \ / _` |/ _ \#
# / ____ \| |    _| |_  | |___| (_) | (_| |  __/#
#/_/    \_\_|   |_____|  \_____\___/ \__,_|\___|#
#################################################

def api():
    #app.config["DEBUG"]=True
    app.run(host="0.0.0.0",port=5000)

#API communication methods
@app.route('/remove',methods=['GET'])
def remove_resolved():
    #removes the requested id from the sql server since it has been marked as cleared by the user
    cache=[]
    table=str(request.args['db'])
    key=str(request.args['id'])
    if key in active_eventkeys[table]:
        delete_key="DELETE FROM "+table+" WHERE id = '{key}'".format(key=key)
        execute_query(delete_key)
        active_eventkeys[table].remove(key)
    return "complete"

@app.route('/get_all',methods=['GET'])
def get_all():
    #gets all events from the SQL server and turns them into a json message to be sent to the requesting app
    cache=[]
    table=str(request.args['db'])
    select="SELECT * FROM "+table
    results=execute_read_query(select)
    if table=="events":
        for x in results:
            cache.append({"Status":x[0],"Name":"","Change":x[1],"EventKey":x[2]})
    else:
        for x in results:
            cache.append({"Status":x[0],"Name":x[1],"Change":x[2],"EventKey":x[3]})
    return jsonify(cache)

###################################################################
# _   _      _       _                 _    _____          _      #
#| \ | |    | |     | |               | |  / ____|        | |     #
#|  \| | ___| |_ ___| | ___  _   _  __| | | |     ___   __| | ___ #
#| . ` |/ _ \ __/ __| |/ _ \| | | |/ _` | | |    / _ \ / _` |/ _ \#
#| |\  |  __/ || (__| | (_) | |_| | (_| | | |___| (_) | (_| |  __/#
#|_| \_|\___|\__\___|_|\___/ \__,_|\__,_|  \_____\___/ \__,_|\___|#
###################################################################

def web_crawler():
    connection=create_connection("database filepath")
    for x in execute_read_query("SELECT events.id FROM events"):
        active_eventkeys['events'].append(x[0])
    #main loop, connects to the webpage
    driver.get("https://www.cradlepointecm.com/ecm.html#devices/routers")
    driver.find_element_by_css_selector("#ember5").send_keys("")
    driver.find_element_by_css_selector("#ember8").send_keys("")
    driver.find_element_by_css_selector("#ember10").click()
    time.sleep(3)
    driver.execute_script('window.open();')
    driver.switch_to.window(driver.window_handles[0])

    #closes the alert window that sometimes shows up on a new day of running
    try:
        for x in driver.find_elements_by_css_selector("button"):
            if "pendo-close-guide-" in x.get_attribute("id"):
                x.click()
                print('nice')
    except:
        pass

    #same as above, closes an alert window
    try:
        driver.find_element_by_css_selector("#pendo-close-guide-ee900bc0").click()
    except:
        print('')
    time.sleep(2)
    device_statuses=get_device_statuses()
    #device_statuses=[x.get_attribute("class")[:-5] for x in driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/div/div[5]/div/div[1]/div[3]/div/table/tbody/tr/td[2]/div/a/span")]

    while True:
        driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div/div[5]/div/div[1]/div[2]/div/div/div[1]/div/span").click()
        time.sleep(1)
        driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div/div[5]/div/div[1]/div[2]/div/div/div[1]/div/span").click()
        old_status=[y for y in device_statuses]
        z=False
        #sometimes there's webpage lag that messes up grabbing the statuses, so we run it until they are grabbed successfully
        while z==False:
            try:
                device_statuses=get_device_statuses()
                z=True
            except:
                continue
        #handles when a new device is added to prevent an out of range error, and ensures the ids of the compared devices are the same so a device is only compared to itself
        try:
            for x in range(len(device_statuses)):
                if device_statuses[x][0] != old_status[x][0] and device_statuses[x][1] == old_status[x][1]:
                    id_file('events',device_statuses[x][0],change=get_device_change(device_statuses[x][1]))
        except:
            continue
        time.sleep(35)

def get_device_statuses():
    #grabs devices statuses and ids and combines them
    statuses=[x.get_attribute("class")[:-5] for x in driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/div/div[5]/div/div[1]/div[3]/div/table/tbody/tr/td[2]/div/a/span")]
    ids=[x.get_attribute("onclick").split("'id=")[1].split("', '")[0] for x in driver.find_elements_by_xpath("/html/body/div[2]/div/div[2]/div/div/div[5]/div/div[1]/div[3]/div/table/tbody/tr/td[6]/div/div/div[1]/a")]
    device_statuses=[[statuses[x],ids[x]] for x in range(len(statuses))]
    return device_statuses

def get_device_change(device_id):
    #navigates to the device information page and grabs the event text for the latest event concerning the device of the id in question
    driver.get('https://www.cradlepointecm.com/ecm.html#logs/alert_log?search=router_id=%22'+str(device_id)+'%22')
    run=False
    text_super=[]
    while run==False:
        try:
            text=[]
            recent=driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[3]/div/table/tbody/tr[1]")
            for x in range(len(recent.find_elements_by_tag_name('div'))):
                if recent.find_elements_by_tag_name('div')[x].get_attribute("class")=="x-grid-cell-inner ":
                    text.append(recent.find_elements_by_tag_name('div')[x].text)
            run=True
            text_super=text
        except:
            continue

    #filters out whitespace and formats text
    text_super=list(filter(None,text_super))
    info=[]
    for x in text_super:
        if x!=' ':
            info.append(x)
    message=""
    for x in info:
        message=message+x+"\n"
    #returns to main status page
    driver.get("https://www.cradlepointecm.com/ecm.html#devices/routers")
    return message

########################################################################
# _____                       _             _    _____          _      #
#|_   _|                     | |           | |  / ____|        | |     #
#  | |  _ __   ___ ___  _ __ | |_ _ __ ___ | | | |     ___   __| | ___ #
#  | | | '_ \ / __/ _ \| '_ \| __| '__/ _ \| | | |    / _ \ / _` |/ _ \#
# _| |_| | | | (_| (_) | | | | |_| | | (_) | | | |___| (_) | (_| |  __/#
#|_____|_| |_|\___\___/|_| |_|\__|_|  \___/|_|  \_____\___/ \__,_|\___|#
########################################################################

def incontrol_crawler():
    #load current event keys into dictionary
    connection=create_connection("database filepath")
    for x in execute_read_query("SELECT incontrol_bandwidth.id FROM incontrol_bandwidth"):
        active_eventkeys['incontrol_bandwidth'].append(x[0])
    for x in execute_read_query("SELECT incontrol_offline.id FROM incontrol_offline"):
        active_eventkeys['incontrol_offline'].append(x[0])
    #get currently active readouts
    old=[x[0] for x in execute_read_query("SELECT incontrol_bandwidth.readout FROM incontrol_bandwidth")]+[x[0] for x in execute_read_query("SELECT incontrol_offline.readout FROM incontrol_offline")]
    latest=''
    latest_id=''
    while True:
        #get latest message raw content. If there aren't any messages and an error gets thrown, just try again
        try:
            latest_id=get_messages()['messages'][0]['id']
            latest=get_content(latest_id)
        except:
            continue
        
        #if valid alert, check if it's new and then cut to content if it is. If it's not an alert, archive, and if it's not new, delete it.
        if "Offline alert" in latest or "Online alert" in latest or "Bandwidth usage alert" in latest or "WAN up alert" in latest or "WAN down alert" in latest:
            if any([x in latest for x in old]):
                file_message('d',latest_id)
                continue
            else:
                latest="From: "+latest.partition("From: ")[2]
        else:
            file_message('a',latest_id)
            continue

        #if it's for sure a new message and of the right type, file it
        readout=BeautifulSoup(latest.split('<li>')[1].split('</li>')[0]).get_text().strip().replace("  ","").replace("\n","")
        if "Offline alert" in latest:
            name=latest.split('Offline alert: ')[1].split('in ')[0]
            id_file('incontrol_offline','offline',name,readout)
        elif "WAN down alert" in latest:
            name=latest.split('WAN down alert: ')[1].split('in ')[0]
            id_file('incontrol_offline','offline',name,readout)
        elif "Online alert" in latest:
            name=latest.split('Online alert: ')[1].split('in ')[0]
            id_file('incontrol_offline','online',name,readout)
        elif "WAN up alert" in latest:
            name=latest.split('WAN up alert: ')[1].split('in ')[0]
            id_file('incontrol_offline','offline',name,readout)
        elif "Bandwidth usage alert" in latest:
            name=latest.split('Bandwidth usage alert: ')[1].split('in ')[0]
            #watch for errors here; not tested on direct incontrol email
            status=latest.split('hits ')[1].split(' ')[0]
            id_file('incontrol_bandwidth',status,name,readout)
        file_message('d',latest_id)
        old=[x[0] for x in execute_read_query("SELECT incontrol_bandwidth.readout FROM incontrol_bandwidth")]+[x[0] for x in execute_read_query("SELECT incontrol_offline.readout FROM incontrol_offline")]        

###########################################
# _______        _      _____       _ _   #
#|__   __|      | |    |_   _|     (_) |  #
#   | | __ _ ___| | __   | |  _ __  _| |_ #
#   | |/ _` / __| |/ /   | | | '_ \| | __|#
#   | | (_| \__ \   <   _| |_| | | | | |_ #
#   |_|\__,_|___/_|\_\ |_____|_| |_|_|\__|#
###########################################

task1=Thread(target=api)
task2=Thread(target=web_crawler)
task3=Thread(target=incontrol_crawler)
task1.start()
task2.start()
task3.start()
