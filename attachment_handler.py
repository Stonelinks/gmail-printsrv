#!/usr/bin/env python
#
#       Author: Lucas Doyle (lucas@lucasdoyle.com)
#       Date: 11/26/2010
#
#       Lots of inspiration taken from here:
#       http://sites.google.com/site/ikonsnotebook/notebook/python/gmail-imap-attachment-downloader

import email, imaplib, os, time
from email.header import decode_header
import subprocess
import string
import sys
import math
import os
import time

usr = '<username here>'
pwd = '<password>'
attachments = 'attach' # directory where to save attachments.

def beep(frequency, delay, length):
    p = subprocess.Popen(['beep', '-f', str(frequency), '-d', str(delay), '-l', str(length)], stdout=subprocess.PIPE)
    return

# beep like crazy!
def awesomebeep():
    a = 30;  # "stretch" factor for sin and cosine
    t = 0;    # time value
    
    while (a < 50) :
        t+=1
        if (t % 4 == 0) : a+=.02
        beep(2500 + a * math.degrees(math.sin(math.radians(t))), 1, 1)
        time.sleep(.0001 + (.001*a - (a*.002 - .001*a)))
    return

# Universal print function. Uses openoffice to print some
# extensions and lpr to print anything else (pdfs, images, etc).
def awesomeprint(path):
    oo_ext = 'odt', 'doc', 'docx', 'xls', 'xlsx', 'ods', 'odp', 'ppt', 'pptx'
    for ext in oo_ext:
        if path.endswith(ext):
            os.system('ooffice -p ' + path)
            return
    os.system('lpr ' + path)

def decodeme(t):
    v = email.header.decode_header(t)
    if v[0][1] != None:
        return str(v[0][0]).decode(v[0][1])
    else:
        return str(v[0][0])

# connect to the gmail imap server
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(usr, pwd)
m.select('Printer') # You a can choose a mail box like INBOX instead
                    # Here I have set up a label called Printer

resp, items = m.search(None, 'ALL') # you could filter using the IMAP rules here (check http://www.example-code.com/csharp/imap-search-critera.asp)
items = items[0].split() # getting the mails id
emailid = items[len(items)-1] # only want the most recent email
resp, data = m.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
email_body = data[0][1] # getting the mail content
mail = email.message_from_string(email_body) # parsing the mail content to get a mail object

if mail.get_content_maintype() == 'multipart': # Check if any attachments
    print "["+decodeme(mail["From"])+"] :" + decodeme(mail["Subject"])
    # we use walk to create a generator so we can iterate on the parts and forget about the recursive headache
    for part in mail.walk():
        # multipart are just containers, so we skip them
        if part.get_content_maintype() == 'multipart':
            continue

        # is this part an attachment ?
        if part.get('Content-Disposition') is None:
            continue

        filename = decodeme(part.get_filename())
        counter = 1

        # if there is no filename, we create one with a counter to avoid duplicates
        if not filename:
            ext = mimetypes.guess_extension(part.get_content_type())
            if not ext:
                # Use a generic bag-of-bits extension
                ext = '.bin'
            filename = 'part-%03d%s' % (counter, ext)

        att_path = os.path.join(attachments, filename)

        # Check if its already there. This means that if you want something
        # reprinted, it better have a unique file name.
        if not os.path.isfile(att_path) :
            # finally write the stuff
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()

            # print
            awesomebeep()
            awesomeprint(att_path)
