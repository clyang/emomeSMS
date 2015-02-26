# -*- coding: utf-8 -*-
import requests
import re

def checkWordCount(msg):
    aChr = 0
    eChr = 0
    for c in msg:
        if ord(c) > 0x3000:
            aChr = aChr + 1
        else:
            eChr = eChr + 1
    return aChr, eChr

def emomeSendSMS(s, recipients, msg):
    sendSMSUrl = "http://websms1.emome.net/sms/sendsms/send.jsp"

    # Check message length
    aChr, eChr = checkWordCount(msg)
    if aChr == 0 and eChr > 160:
        print "Pure English message should shorter than 160 characters"
        return False
    elif aChr > 0 and (aChr+eChr) > 70:
        print "Mixed Chinese/English message should shorter than 70 characters"
        return False
    else:
        langCode = 2 if aChr == 0 else 7

    # Process the phone number list
    tmpList = []
    recvList = []
    recipients = recipients.replace(" ", "")
    if recipients.find(",") < 0: # Only one number
        tmpList.append(recipients)
    else:
        tmpList = recipients.split(",")

    # verify phone number format. This script only allows TW numbers
    for number in tmpList:
        match = re.search("^(\+8869\d{8}$|09\d{8}$)", number)
        if match:
            recvList.append(number.replace("+886", "09"))

    # build recipients list
    if len(recvList) == 0 or len(recvList) > 200:
        print "Number of recipients should between 1 to 200."
        return False
    else:
        recvList = list(set(recvList)) # remove duplicate number.
        recipients = ','.join(recvList)

    # sned the message
    postfield = {
                  "nextURL": "0",
                  "resend": "1", # 1: resend 0: otherwise
                  "language": langCode,
                  "phonelist": recipients,
                  "data": msg,
                  "rad": "0", # 0: send instantly 1: scheduled
                  "selsec": "00"
                }
    r = s.post(sendSMSUrl, data = postfield)
    if r.status_code == 200:
        print "SMS is sent successfully!!!"

def emomeLogin(username, password):
    url = "http://websms1.emome.net/sms/sendsms/new.jsp?msg="
    authUrl = "https://member.cht.com.tw/HiReg/multiauthentication"
    confirmUrl = "https://member.cht.com.tw/HiReg/redirect?m=logininfo"

    s = requests.Session()
    r = s.get(url)

    if r.history:
        content = r.text
        match = re.search(".*checksum.*value=\"(?P<checksum>[a-f0-9]+)\"/>", content)
        if match:
            checksum = match.group("checksum")
            postfield = {
                          "version": "1.0",
                          "curl": "http://auth.emome.net/emome/membersvc/AuthServlet",
                          "siteid": "76",
                          "sessionid": "",
                          "channelurl": "http://auth.emome.net/emome/",
                          "others": "5235",
                          "checksum": checksum,
                          "cp_reg_info": "",
                          "reg_url": "",
                          "service_type": "",
                          "finish_channelurl": "",
                          "formtype": "",
                          "sso": "yes",
                          "uid": username,
                          "pw": password
                        }
            r = s.post(authUrl, data = postfield)
            r = s.get(confirmUrl)
            r = s.get(url)
            if r.text.find(u"訊息內容") > 0:
                print "Login Successfully! We can send SMS now"
                return s
            else:
                print "Unable to retrieve Emome WebSMS interface"
                return "False"
        else:
            print "Something wrong with Emome authentication!"
            return "False"
    else:
        print "Unable to open Emome website"
        return False
