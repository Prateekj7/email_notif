from __future__ import print_function
import base64
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import re 

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    email_list = service.users().messages().list(userId='me', q='OTP is:unread newer_than:1h').execute()
    for email in email_list['messages']:
        id_num = email['id']
        message = service.users().messages().get(userId='me', id=id_num).execute()
        content = message['payload']
        if('body' in content and 'data' in content['body']): 
            data = base64.urlsafe_b64decode(content['body']['data'])
            data = data.decode('utf-8')
            print(data)     
        if ('parts' in content):
            combined_data=""
            for part in content['parts']:
                if('data' in part['body']):
                    data2 = base64.urlsafe_b64decode(part['body']['data'])
                    data2 = data2.decode('utf-8')
                    combined_data = combined_data + data2
        print(re.findall(r'[0-9]{4,8}', combined_data)[0])
        


if __name__ == '__main__':
    main()