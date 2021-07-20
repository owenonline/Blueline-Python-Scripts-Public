from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from mimetypes import MimeTypes
import base64
from base64 import urlsafe_b64encode

SCOPES = ['https://mail.google.com/','https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.compose']

def main():
    global SCOPES
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials file path', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    return service

def send_mail(destination,sender,subject,text,attachment_filepath):
    global service
    #service=main()

    message=MIMEMultipart()
    message['to']=destination
    message['from']=sender
    message['subject']=subject

    msg=MIMEText(text)
    message.attach(msg)

    if attachment_filepath != '':
        mimetypes = MimeTypes()
        content_type, encoding = mimetypes.guess_type(attachment_filepath)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)

        fp=open(attachment_filepath,'rb')
        msg=MIMEBase(main_type,sub_type)
        msg.set_payload(fp.read())
        fp.close()
        filename=os.path.basename(attachment_filepath)
        msg.add_header('Content-Disposition','attachment',filename=filename)
        message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_bytes())
    raw = raw.decode()
    body = {'raw': raw}

    message=(service.users().messages().send(userId=sender,body=body).execute())

    print(message)

def get_messages():
    global service
    try:
        return service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    except Exception as error:
        print('An error occurred: %s' % error)

def get_content(msgID):
    global service
    try:
        return base64.urlsafe_b64decode(service.users().messages().get(userId='me',id=msgID,format='raw').execute()['raw'].encode("utf-8")).decode("utf-8")
    except Exception as error:
        print('An error occurred: %s' % error)

def file_message(method,msgID):
    global service
    try:
        if method=='d':
            service.users().messages().delete(userId='me',id=msgID).execute()
        else:
            post_data={"removeLabelIds": ["INBOX"]}
            service.users().messages().modify(userId="me", id=msgID, body=post_data).execute()
    except Exception as error:
        print('An error occurred: s' % error)
        

service=main()
