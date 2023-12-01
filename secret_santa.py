import math
import time
import random
import smtplib
import imaplib
import itertools

username = ''
password = ''

conn = smtplib.SMTP('', 587)
conn.ehlo()
conn.starttls()
conn.login(username, password)

def is_bad_permutation(from_list, to_list):
    for i in range(len(from_list)):
        if from_list[i] == to_list[i]:
            return True
        
    return False

names_from = ()
surnames_from = ()
mail_addresses = ()

roles = ['cook']*number_cooks + ['cleaner']*number_cleaners

names_to = names_from

while is_bad_permutation(names_from, names_to):
    permutation_number_names = random.randint(1, math.factorial(len(names_from))) - 1
    names_to = list(itertools.permutations(names_from))[permutation_number_names]
    surnames_to = list(itertools.permutations(surnames_from))[permutation_number_names]

    permutation_number_roles = random.randint(1, math.factorial(len(roles))) - 1
    roles = list(list(itertools.permutations(roles))[permutation_number_roles])

for i, name_from in enumerate(names_from):
    name_to = names_to[i]
    surname_to = surnames_to[i]
    mail_address = mail_addresses[i]
    role = roles.pop()
    
    role_submessage = ''
    if name_from == 'host_name':
        role_submessage = role_submessage + 'Since you are hosting, there is no need for you to hussle - just relax and let others work!'
    else:
        role = roles.pop()
        if role == 'cook':
            role_submessage = role_submessage + "You will be a cook. The kitchen will be your artist's studio, pan and ladle your canvas and brush. We cannot wait to taste your work of art!"
        else:
            role_submessage = role_submessage + "You will be a cleaner. We have heard wonders of your cleanliness and attention to detail. We are confindent that no kitchen bateria will find shelter under your watch!"

    role_submessage = role_submessage + '\n\n'  

    message = (
        'Subject: Your Secret Santa + Supper Details\n\n'
                  + 'Dear '
                  + name_from
                  + ',\nYou might be wondering to whom you will be getting a Christmas present? Well, that special person is '
                  + name_to + ('' if name_to != 'Repeated Name' else (' (' + surname_to + ')'))
                  + ' - you got a tricky one, huh?'
                  + '\nHave fun looking for a present! '
                  + 'Just as a reminder, the present should not cost you more than CHF 15. Besides that, there are no other rules, you can set your imagination free.\n\n'
                  + 'To make easier for everyone, we have decided to split the attendees into three groups: Cooks, cleaners and hostess. '
                  + role_submessage
                  + "We will be pleased to have you at time on day at host's place (address) for an evening of Christmass merriness and Swiss cheeseness."
                  + "\n\nYours truly,\nThe Coolname Society"
        )
    
    conn.sendmail(username,
                  mail_address,
                  message.encode('utf-8'))

conn.quit()

print('Messages sent')
time.sleep(10)

### Delete sent messages
imap = imaplib.IMAP4_SSL("")
imap.login(username, password)
imap.select("")
status, messages = imap.search(None, 'SUBJECT "Your Secret Santa"')
messages = messages[0].split(b' ')
for mail in messages:
    imap.store(mail, "+FLAGS", "\\Deleted")
imap.expunge()
imap.close()

print('Messages deleted')
imap.logout()
