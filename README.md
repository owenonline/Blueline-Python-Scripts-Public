# Blueline Python Scripts
Private repository of scripts written for Blueline Telecom

Contents:

    -email automation
        =folder that contains scripts required for email automation
        +credentials.json
            =Google authentication file
        +token.json
            =Google authentication file
        +quickstart.py
            =Quickstart file to enable authentication of new email addresses and change auth scope
        +gmail_auto.py
            =script containing method to automatically send an email from bluelinetelecom.python@gmail.com
        +refresh_token.bat
            =batch file that deletes the auth token and runs the quickstart file to generate a new one
    -production scripts
        =folder that contains scripts currently in a production run
        +general_api.py
            =general API script that allows a remote user to run SQL commands and python modules on the server.
        +image_processor.py
            =a script that takes a filepath as input and then outputs all the text and processed barcodes and their locations
        +cps_script.bat
            =BATCH script that opens a cmd window and runs the cps_script.py script
        +cps_script.py
            =Script written for CPS Products to constantly monitor the ACD queue and send an email alert when an agent logs in or out. Runs 24/7
        +daily_call_logs.bat
            =BATCH script referenced by TaskScheduler to run weekly_call_logs.py at the specified time
        +daily_call_logs.py   
            =script for Crown Wine & Spirits to send a processed csv file of all calls that occurred during the preceding week every Monday. The decided run time is 6:00 am EST
        +token.json
            =Google authentication file
        +refresh.py
            =requests an email through the Gmail api and in doing generates a new token when the old one expires
        +TMAS script.py
            =Checks the Blueline TMAS for negative variances and compiles them into a spreadsheet which is sent to Liz every Monday
        +TMAS script.bat
            =BATCH script referenced by TaskScheduler to run TMAS script.py at the specified time
        +ISP Billing Script.py
            =script that goes into TMAS and for every bill in the current month collects the provider, amount, date, and customer name and compares it with the charges ostensibly for the same customer in Coredial and sends the result to Gwen every monday
        +ISP Billing Script.bat
            =BATCH script referenced by TaskScheduler to run ISP Billing Script.py at the specified time
    -one-off scripts
        =folder that contains one-off projects never intended for continuous service, hence "one-off". Unless stated otherwise, each script completed its task successfully
	+sql_backlog_check.py
	    =generates a list of entries in the inventory csv file that aren't in the SQL server in order to discover why certain records didn't get uploaded
	+sql_backlog_upload.py
	    =uploads the contents of the inventory csv file (a compiled csv file of all the various inventory spreadsheets) to the new inventory SQL database
        +shoreham_blfs.py
            =set up the blfs for all 169 phone that needed Gabe's blank-blank-blank-blank-blf-blf-blank-blank-speed dial setup
        +ansaarie_holiday_removal.py
            =removes all holidays from Ansaarie's portal except Jan 1, Jul 4, Jul 3, Sep 7, Nov 26, Nov 27, Dec 24, Dec 25, and Dec 31
        +blf_swap_gabe.py
            =goes through all Blueline extensions in the portal and swaps Erica and Dagmar's names for all of their extensions since Gabe swapped their extension numbers
        +incontrol_devices.py
            =goes through incontrol and checks all devices for some attribute requested by Desmond, then writes it all to a csv file
        +incontrol_python.py
            =goes through incontrol and adds a portal link to every customer device for which a corresponding portal link can be found. Never had production run because development time was outweighing benefit.
        +portal_python.py
            =goes through all Blueline extensions in the portal and creates a csv containing every [name,extension,DID] pair
        +portal_python_holidays.py
            =goes through all portal customers and prints a list of every holiday that isn't New Years, July 4, Thanksgiving, or Christmas.
        +update_holidays.py
            =goes through all portal customers and updates all holidays to just New Years, July 4, Thanksgiving, and Christmas. Never had production run since it would take away custom holidays that are actually intentional.
        +ups_python.py
            =goes through a given UPS invoice and checks the UPS portal to create a comparison of estimated costs at time of purchase and the costs on the invoice to locate instances of overcharging
        +invoice_python.py
            =script written for Erica that takes a customer invoice and breaks down charges by location, then puts that in an easy to read csv file
        +private_ips.py
            =script that goes through incontrol 2 based on an already downloaded file of device group urls (accessible through the incontrol2 homepage) and counts the number of devices with a connection method of DHCP
    -out of service
        =folder that contains scripts that were once production scripts but are no longer in service
        +check_running.bat
            =BATCH Script referenced by TaskScheduler to check if any perpetual tasks have stopped running (currently the CPS script and Bluecloud backend) and run them if they have. No longer needed as there is only one remaining 24/7 script.
        +netcloud_script.bat
            =BATCH script referenced by check_running.bat that opens a cmd window and runs the netcloud_script.py script
        +netcloud_script.py
            =script for Desmond that checks for when netcloud devices go on/offline and creates an audiovisual update on one of the chromecasts and sends him an email containing all the information for the change in status
        +bluecloud_backend.bat
            =BATCH script referenced by check_running.bat that opens a cmd window and runs the bluecloud_backend.py script
        +bluecloud_backend.py
            =script that serves the same function as netcloud_script.py, but instead of updating a chromecast makes the information accessible by HTTP GET requests executed by an app. It also stores a list of unresolved events so the information displayed is consistent across all instances of the app, and does this with an SQL server. Recently this has been expanded into an all-encompassing backend for the expanding Bluecloud alert platform, which groups alerts from multiple platforms into one location for the IT team
        +Netcloud App
            =compressed folder which contains all solution files for the Xamarin.Forms project used to build the app referenced in the description of netcloud_api.py. This app displays a list of color coded unresolved events, constantly updating to check for new events. When an event is deleted in the app a command is sent to delete it from the master SQL table, and when a new event appears a sound is played signalling whether it is an online or an offline event. The app has been deployed in Android and has not been tested on iOS.
        +Netcloud App v2
            =compressed folder containing all solution files... same as Netcloud app, but contains the code for the updpated version of the app which now accounts for netcloud events
    +.gitattributes
        =Git attributes file
    +chromedriver.exe
        =required chrome driver file for Selenium. Current supported version of Chrome is 8.9
    +README.md
        =file containing location and description for all repository contents
