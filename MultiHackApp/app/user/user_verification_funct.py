import pyperclip
import requests
import random
import string
import time
import sys
import re
import os

API = 'https://www.1secmail.com/api/v1/'
domainList = ['1secmail.com', '1secmail.net', '1secmail.org']
domain = random.choice(domainList)
processedMails = {}  # Diccionario para almacenar correos procesados


def banner():
    print(r'''
                         ''~``
                        ( o o )
+------------------.oooO--(_)--Oooo.------------------+
|                                                     |
|                    Mail Swipe                       |
|               [by Sameera Madushan]                 |
|                                                     |
|                    .oooO                            |
|                    (   )   Oooo.                    |
+---------------------\ (----(   )--------------------+
                       \_)    ) /
                             (_/
    ''')


def get_email(email):
    return email


def gen_random_code():
    code = ''.join(random.choices('0123456789', k=6))
    return code


def generateUserName():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    return username


def extract():
    getUserName = re.search(r'login=(.*)&', newMail).group(1)
    getDomain = re.search(r'domain=(.*)', newMail).group(1)
    return [getUserName, getDomain]


def print_statusline(msg: str):
    last_msg_length = len(print_statusline.last_msg) if hasattr(print_statusline, 'last_msg') else 0
    print(' ' * last_msg_length, end='\r')
    print(msg, end='\r')
    sys.stdout.flush()
    print_statusline.last_msg = msg


def deleteMail():
    url = 'https://www.1secmail.com/mailbox'
    data = {
        'action': 'deleteMailbox',
        'login': f'{extract()[0]}',
        'domain': f'{extract()[1]}'
    }

    print_statusline("Disposing your email address - " + mail + '\n')
    req = requests.post(url, data=data)


def checkMails():
    sender = None
    subject = None
    content = None
    reqLink = f'{API}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
    req = requests.get(reqLink).json()
    length = len(req)
    if length == 0:
        print_statusline("Your mailbox is empty. Hold tight. Mailbox is refreshed automatically every 5 seconds.")
    else:
        idList = []
        for i in req:
            for k, v in i.items():
                if k == 'id':
                    mailId = v
                    idList.append(mailId)

        x = 'mails' if length > 1 else 'mail'
        print_statusline(f"You received {length} {x}. (Mailbox is refreshed automatically every 5 seconds.)")

        for i in idList:
            if i not in processedMails:  # Verifica si el correo ya ha sido procesado
                msgRead = f'{API}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={i}'
                req = requests.get(msgRead).json()
                for k, v in req.items():
                    if k == 'from':
                        sender = v
                    if k == 'subject':
                        subject = v
                    if k == 'textBody':
                        content = v

                print(f"\nSender: {sender}\nSubject: {subject}\nContent: {content}\n")
                processedMails[i] = {'sender': sender, 'subject': subject,
                                     'content': content}  # Almacena el correo procesado en el diccionario
    return sender, content


def check_code():
    random_code = gen_random_code()
    code = checkMails()[1]
    if random_code == code:
        return True
    else:
        return False


banner()
# userInput1 = input("Do you wish to use to a custom domain name (Y/N): ").capitalize()

try:
    newMail = f"{API}?login={generateUserName()}&domain={domain}"
    reqMail = requests.get(newMail)
    mail = f"{extract()[0]}@{extract()[1]}"
    pyperclip.copy(mail)
    print("\nYour temporary email is " + mail + " (Email address copied to clipboard.)" + "\n")
    print(f"---------------------------- | Inbox of {mail} | ----------------------------\n")
    get_email(mail)
    while True:
        checkMails()
        time.sleep(5)

except(KeyboardInterrupt):
    deleteMail()
    print("\nProgramme Interrupted")
    os.system('cls' if os.name == 'nt' else 'clear')
