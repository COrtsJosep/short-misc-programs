import math
import time
import random
import smtplib
import imaplib
import itertools

username = '' # email address
password = '' # secret

conn = smtplib.SMTP('smtp.gmail.com', 587)
conn.ehlo()
conn.starttls()
conn.login(username, password)

def permute(l: list) -> list:
    ### Extremely ineficient. Never use irl
    ### returns a random permutation of a list
    p =  random.randint(1, math.factorial(len(l))) - 1
    return list(itertools.permutations(l))[p]

def is_bad_arrangement(arrangement: dict) -> bool:
    ### checks if the secret santa arrangement is OK
    for santa, santee in arrangement.items():
        if santa == santee or arrangement[santee] == santa:
            return True

    return False

mails = {
    'name': 'email'
}

names = list(mails.keys())

workers = [] # list of people who have to work
tasks = [] # list of tasks
roles = {worker: role for worker, role in zip(workers, tasks))}

arrangement = {santa: santee for santa, santee in zip(names, permute(names))}
while is_bad_arrangement(arrangement):
    arrangement = {santa: santee for santa, santee in zip(names, permute(names))}    

for name in names:
    mail = mails[name]
    role = roles[name]
    santee = arrangement[name]
    
    role_submessage = ''
    if role == 'host':
        role_submessage = 'Since you are hosting, there is no need for you to hussle - just relax and let others work!'
    elif role == 'cook':
        role_submessage = "You will be a cook. The kitchen will be your artist's studio, pan and ladle your canvas and brush. We cannot wait to taste your work of art!"
    else:
        role_submessage = "You will be a cleaner. We have heard wonders of your cleanliness and attention to detail. We are confindent that no kitchen bateria will find shelter under your watch!"

    role_submessage = role_submessage + '\n\n' 

    message = (
        'Subject: Your Secret Santa + Supper Details\n\n'
                  + 'Dear '
                  + name
                  + ',\nYou might be wondering to whom you will be getting a Christmas present? Well, that special person is '
                  + santee
                  + ' -- you got a tricky one, huh?'
                  + '\nHave fun looking for a present! '
                  + 'Just as a reminder, the present should not cost you more than CHF 15. Besides that, there are no other rules, you can set your imagination free.\n\n'
                  + 'To make it easier for everyone, we have decided to split the attendees into three groups: Cooks, cleaners and hostess. '
                  + role_submessage
                  + "We will be pleased to have you at place (address) for an evening of Christmas merriness and Swiss cheeseness."
                  + "\n\nYours truly,\nThe Secret Santa Organization Comitee"
        )

    conn.sendmail(username,
                  mail,
                  message.encode('utf-8'))

conn.quit()

print('Messages sent')
time.sleep(10)

### Delete sent messages
imap = imaplib.IMAP4_SSL('imap.gmail.com')
imap.login(username, password)
imap.select('[Gmail]/Enviats')
status, messages = imap.search(None, 'SUBJECT "Your Secret Santa"')
messages = messages[0].split(b' ')
for mail in messages:
    imap.store(mail, '+FLAGS', '\\Deleted')
imap.expunge()
imap.close()

print('Messages deleted')
imap.logout()
