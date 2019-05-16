#!/usr/bin/env python
# md5: 240552f6ad16386caded4f93fbba18da
#!/usr/bin/env python
# coding: utf-8



import imaplib, email, os
from getsecret import getsecret
user = getsecret('email_address')
password = getsecret('email_password')
imap_url = getsecret('email_server')
connection = imaplib.IMAP4_SSL(imap_url)
connection.login(user, password)
connection.select()



from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Nothing to see here'

@app.route('/get_emails_cs377u')
def get_emails_cs377u():
  messages = []
  result, data = connection.uid('search', None, "ALL")
  # search and return uids instead
  i = len(data[0].split()) # data[0] is a space separate string
  for x in range(i):
    latest_email_uid = data[0].split()[x] # unique ids wrt label selected
    result, email_data = connection.uid('fetch', latest_email_uid, '(RFC822)')
    # fetch the email body (RFC822) for the given ID
    raw_email = email_data[0][1]
    email_message = email.message_from_bytes(raw_email)
    message = []
    message.append('From: ' + email_message['From'])
    message.append('Subject: ' + email_message['Subject'])
    message.append('Date: ' + email_message['Date'])
    #raw_email_string = raw_email.decode('utf-8')
    #print(raw_email_string)
    #email_message = email.message_from_string(raw_email_string)
    # this will loop through all the available multiparts in mail
    for part in email_message.walk():
     if part.get_content_type() == "text/plain": # ignore attachments/html
      body = part.get_payload()
      message.append(body)
      #print(body.decode('utf-8'))
      #save_string = str("D:Dumpgmailemail_" + str(x) + ".eml")
      # location on disk
      #myfile = open(save_string, 'a')
      #myfile.write(body.decode('utf-8'))
      # body is again a byte literal
      #myfile.close()
     else:
      continue
    messages.append('<br>'.join(message))
  return '<br><br>'.join(messages)

if __name__ == '__main__':
  app.run()





