import flask
from flask import request, jsonify
import sqlite3
from sqlite3 import Error
import sys

app=flask.Flask(__name__)
stored_data=None

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

@app.route('/post_file',methods=['POST'])
def post_file():
    global stored_data
    file=request.files['file']
    file.save('received file filepath'+file.filename)
    stored_data='received file filepath'+file.filename
    print('data posted')
    return "complete"

@app.route('/run_script',methods=['GET'])
def run_script():
    global stored_data
    #add to path
    try:
        path=str(request.args['path'])
        sys.path.append(path)
    except:
        pass
    #module name
    name=str(request.args['name'])
    #get module
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    #run module with args if necessary
    result=''
    
    #this code works but isn't being used for testing
    #if stored_data!=None:
    #    result=mod(stored_data)
    #    print(result)
    #else:
    #    result=mod()
    result=mod('C:\\Users\\rdp\\Pictures\\label.jpg')
    
    #reset what needs to be reset
    stored_data=None
    sys.path.remove(path)
    return jsonify(result)

@app.route('/run_sql',methods=['GET'])
def run_sql():
    #remotely execute read queries
    command=str(request.args['command'])
    cmdtype=str(request.args['cmdtype'])
    if cmdtype=='read':
        results=execute_read_query(command)
        return jsonify(results)
    if cmdtype=='write':
        execute_query(command)
        return "complete"


api()
