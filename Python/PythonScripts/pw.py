#! python3

# pw.py -- An insecure password manager program

import sys
import pyperclip

PASSWORDS = {'email': 'yabbadabbadoo',
             'yt': 'iswearthisaintmine',
             'blog': 'l1vedanger0usly'}

if len(sys.argv) < 2:
    print('Try again with somethin to check, bud')
    sys.exit()

account = sys.argv[1]

if account in PASSWORDS:
    pyperclip.copy(PASSWORDS[account])
    print('Password for ' + account + ' copied to clipboard')
else:
    print('Account not found.. Would ur dumbass like to add a password for ' + account +'?')
    print('Type Y/y or N/n')
    Qresponse = input().upper()
    if(Qresponse == 'Y'):
        print('Please enter password, dumbass:')
        password = input()
        PASSWORDS[account] = password
        print('password added, thank. program now exit')
    else:
        print('fine, fuck u too')
