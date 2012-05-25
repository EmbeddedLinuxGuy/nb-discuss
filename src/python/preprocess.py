"""
Created by Jared Dunne on 2012-05-19.
Modified by Mike Schachter (mschachter@eigenminds.com)
"""
import os
from mailbox import mbox
import re

class MBMessage(object):

    def __init__(self):
        self.from_value = None
        self.message_id = None
        self.in_reply_to_id = None
        self.subject = None
        self.body = None
        self.sent_date = None
        self.received_date = None


def read_mbox(mbox_path):
    if not os.path.exists(mbox_path):
        print 'No such mbox file: %s' % mbox_path
        return

    return mbox(mbox_path)

def get_messages(mb):

    email_expr = re.compile('([\w\-\.+]+@(\w[\w\-]+\.)+[\w\-]+)') #parses out email addresses

    all_msgs = []
    for msg in mb:

        mb_msg = MBMessage()

        #get from field
        m = email_expr.search(msg['from'])
        if m is not None:
            mb_msg.from_value = m.group(0)

        #get message id
        mb_msg.id = msg['message-id']
        mb_msg.in_reply_to_id = msg['in-reply-to']
        mb_msg.subject = msg['subject']
        mb_msg.sent_date = msg['sent-date']
        mb_msg.received_date = msg['x-list-received-date']
        mb_msg.body = get_plain_body(msg)

        if mb_msg.body is not None:
            all_msgs.append(mb_msg)

    return all_msgs

def get_plain_body(msg):
    if msg.is_multipart():
        for sub_msg in msg.get_payload():
            mb = get_plain_body(sub_msg)
            if mb is not None:
                return mb

    if msg.get_content_type() == 'text/plain':
        return msg.get_payload()



def create_database(mb):

    pass


def get_senders(messages):

    senders = {}
    email_expr = re.compile('([\w\-\.+]+@(\w[\w\-]+\.)+[\w\-]+)') #parses out email addresses

    num_messages = 0
    for msg in messages:
        m = email_expr.search(msg['from'])
        if m is not None:
            email_address = m.group(0)
            if email_address not in senders:
                senders[email_address] = 0
            senders[email_address] += 1
        else:
            print 'No match: %s' % msg['from']
        num_messages += 1
    print '# of messages: %d' % num_messages
    print '# of senders: %d' % len(senders)
    return senders



"""
def sortDictionaryByValues(dict,reverse=True):
    result=[]          
    for w in sorted(dict, key=keys.get, reverse=reverse):
        result.append([w, dict[w]])
    return result

def showPayloadSample(msg):
    payload = msg.get_payload()
    if msg.is_multipart():
        div = ''
        for subMsg in payload:
            print div
            showPayloadSample(subMsg)
            div = '------------------------------'
    else:
        print msg.get_content_type()
        print payload[:200]

def getPayload(msg, content_type):
    payload = msg.get_payload()
    out = "";
    if msg.is_multipart():
        div = ''
        for subMsg in payload:
            subOut = getPayload(subMsg, content_type)
            if subOut:
                out = out + div + subOut
                div = ' '
    else:
        if msg.get_content_type() == content_type:
            out = payload
    return out

def getTextPayload(msg):
    return getPayload(msg,"text/plain")

def getHtmlPayload(msg):
    return getPayload(msg,"text/html")

from mailbox import *
mb = mbox('/Users/jareddunne/noisebridge/ml-noisebridge/drama-mbox/noisebridge-discuss.mbox')
#messages=mb.items()
#print len(messages)

count=0
for message in mb:
    subject = message['subject']       # Could possibly be None.
    if subject and 'drama' in subject.lower():
        print subject
        count=count+1
        last=message

content_types={}
neither=''
html_only=''
for message in mb:
    text=getTextPayload(message)
    html=getHtmlPayload(message)
    if text and html:
        #print "got both"
        foo=[]
    elif text:
        #print "got text only"
        foo=[]
    elif html:
        print "--------------------------- got html only --------------------------- "
        #showPayloadSample(message)
        html_only=message
    else:
        print "--------------------------- got neither --------------------------- "
        #showPayloadSample(message)
        neither=message

keys={}
for message in mb:
    for key in message.keys():
        key=key.lower()
        if key in keys:
            keys[key]=keys[key]+1
        else:
            keys[key]=1


sorted_keys = sortDictionaryByValues(keys)
sorted_content_types = sortDictionaryByValues(content_types)

getTextPayload(last)
getHtmlPayload(last)

showPayloadSample(html_only)
showPayloadSample(neither)


#message['message-id']
#message['in-reply-to']
#message['references']
#message['date']
#message['x-list-received-date']
#message['subject']
#message['from']
#message['return-path']
#message['to']
#message['cc']
"""
