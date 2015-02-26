# -*- coding: utf-8 -*-
from emomeSMS import *

EMOME_USERNAME = ""
EMOME_PASSWORD = ""
# 收件人清單, 必須使用半形逗號(,)隔開, 最多200組
recipients = "0912345678,0987654321,+886934567890"
# 傳送訊息. 單一則訊息純英文數字為160字，中英文及數字混合為70字
msg = u"kerkerker 測試~!! test!! ニュース123"

session = emomeLogin(EMOME_USERNAME, EMOME_PASSWORD)
if session:
    emomeSendSMS(session, recipients, msg)
