# -*- coding: utf-8
import sys
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

sys.path.append("cephQeInfra")
from datetime import datetime
import pytz

from cephQeInfra import docOnQa
from cephQeInfra import htmlPrep
from cephQeInfra import needInfo_class
from cephQeInfra import testOnQa
from cephQeInfra import qaAck
from cephQeInfra import unspecified_severity


htmlPrep_obj= htmlPrep.htmlPrep()
docOnQa_Obj= docOnQa.DocOnQaCls()
needInfo_Obj=needInfo_class.needInfoCls()
testOnQa_Obj= testOnQa.TestOnQaCls()
qaAck_Obj = qaAck.QaAckCls()
unspec_sev_obj = unspecified_severity.unspecified_severity_cls()

UTC = pytz.utc
IST = pytz.timezone('Asia/Kolkata')
datetime_ist = datetime.now(IST)
start_time=datetime_ist.strftime("%d %b %Y %H:%M")


needInfoBugs=needInfo_Obj.get_NeedInfo_bugs()
doc_OnQA_bugs=docOnQa_Obj.get_Doc_bugs()
testOnQa_bugs=testOnQa_Obj.get_test_OnQa_bugs()
qaAck_bugs = qaAck_Obj.get_QaAck_bugs()
unspec_sev_bugs=unspec_sev_obj.get_unspecified_severity_bugs()




sender = "ceph-qe-infra@redhat.com"
recipients = ["ceph-qe@redhat.com"]

#sender = "skanta@redhat.com"
#recipients = ["skanta@redhat.com"]


msg = MIMEMultipart('mixed')
msg["Subject"] = "Bugzilla action items on QE -Auto generated at "\
                    + start_time +"[IST]"
msg["From"] = sender
msg["To"] = ", ".join(recipients)
table1 = MIMEText(needInfoBugs, "html")
table2 = MIMEText(doc_OnQA_bugs, "html")
table3 = MIMEText(testOnQa_bugs, "html")
table4 = MIMEText(qaAck_bugs, "html")
if (unspec_sev_bugs != None):
    table5 = MIMEText(unspec_sev_bugs, "html")


msg.attach(table1)
msg.attach(table2)
msg.attach(table4)
if (unspec_sev_bugs != None):
    msg.attach(table5)
msg.attach(table3)

        

try:
    s = smtplib.SMTP("localhost")
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()
    print(
        "Results have been emailed to {recipients}".format(
         recipients=recipients
         )
        )

except Exception as e:
            print("\n")
            #log.exception(e)
