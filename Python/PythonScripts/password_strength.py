import re 
import sys

if len(sys.argv) < 2:
    print('Please enter password: ')
    password = input()
else:
    password = sys.argv[1]

# A strong password is defined as one that is at least eight characters long, contains both uppercase and lowercase characters, and has at least one digit

lowerRegex = re.compile(r'[a-z]')
upperRegex = re.compile(r'[A-Z]')
digitRegex = re.compile(r'\d')

lower = lowerRegex.findall(password)
upper = upperRegex.findall(password)
digit = digitRegex.findall(password)



if( (lower != []) and (upper != []) and (digit != []) and len(password) >= 8):
    print("yaya! pass STRONG and THICC")
else:
    print("ur pass WEAK SON")