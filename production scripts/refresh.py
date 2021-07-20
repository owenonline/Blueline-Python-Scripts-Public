import sys
sys.path.insert(1, 'C:\\Users\\rdp\\Documents\\GitHub\\Blueline-Python-Scripts\\email automation')
from gmail_auto import send_mail

def refresh():
    send_mail("my personal email address","company automated email address","test","test","")
