#!/usr/bin/env python
# md5: c0221f6df0709c828a76c375dcf20a03
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







import arrow
import email.utils
import time
import datetime

def email_date_to_local_arrow(email_date):
  date_tuple = email.utils.parsedate_tz(email_date)
  return arrow.get(email.utils.mktime_tz(date_tuple)).to('America/Los_Angeles')

def decode_header(header):
  decoded,charset = email.header.decode_header(str(header))[0]
  if charset == None:
    return header
    return decoded.decode('utf-8')
  return decoded.decode(charset)



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
  uid_list = data[0].split()
  for x,latest_email_uid in enumerate(uid_list):
    result, email_data = connection.uid('fetch', latest_email_uid, '(RFC822)')
    # fetch the email body (RFC822) for the given ID
    raw_email = email_data[0][1]
    email_message = email.message_from_bytes(raw_email)
    message = []
    message.append('From: ' + decode_header(email_message['From']))
    message.append('Subject: ' + decode_header(email_message['Subject']))
    message.append('Date: ' + str(email_date_to_local_arrow(email_message['Date'])))
    #raw_email_string = raw_email.decode('utf-8')
    #print(raw_email_string)
    #email_message = email.message_from_string(raw_email_string)
    # this will loop through all the available multiparts in mail
    for part in email_message.walk():
     if part.get_content_type() == "text/plain": # ignore attachments/html
      body = part.get_payload(decode=True).decode(part.get_content_charset())
      #body = part.get_payload()
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
  return '<br><br>'.join(reversed(messages))

print(get_emails_cs377u())




if __name__ == '__main__':
  app.run()





