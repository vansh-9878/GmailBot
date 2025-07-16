from imapclient import IMAPClient
import pyzmail
from pushbullet import Pushbullet
import time,os
from dotenv import load_dotenv
load_dotenv()

EMAIL = os.getenv("GMAIL2") 
APP_PASSWORD = os.getenv("PASSWORD2")
PB_ACCESS_TOKEN = os.getenv("TOKEN")

KEYWORDS = ['assignment', 'deadline', 'exam', 'urgent', 'submission','VIT','Dean','HOD','NPTEL','Course','Hostel','Hackathon','workshop','registration','placement','FFCS']

pb = Pushbullet(PB_ACCESS_TOKEN)

def contains_keyword(subject, body):
    text = (subject or "") + " " + (body or "")
    text = text.lower()
    return any(keyword.lower() in text for keyword in KEYWORDS)

def check_email():
    with IMAPClient('imap.gmail.com') as client:
        client.login(EMAIL, APP_PASSWORD)
        client.select_folder('INBOX')

        messages = client.search(['UNSEEN'])
        count=0
        if messages:
            for uid in messages:
                count+=1
                if(count>20):
                    break
                raw_message = client.fetch([uid], ['BODY[]', 'FLAGS'])
                message = pyzmail.PyzMessage.factory(raw_message[uid][b'BODY[]'])

                subject = message.get_subject()
                if message.text_part:
                    body = message.text_part.get_payload().decode(message.text_part.charset or 'utf-8', errors='ignore')
                else:
                    body = ""

                if contains_keyword(subject, body):
                    print(f"📩 Keyword match: {subject}")
                    pb.push_note("📬 Important Email", subject)
                else:
                    print(f"📭 Skipped (no keyword): {subject}")
        else:
            print("📭 No new unread emails.")

check_email()