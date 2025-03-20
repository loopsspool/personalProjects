#! python3

#bullet_point_adder.py adds bullet points (well, *s) to the beginning of each new line of what is copied on the clipboard

import pyperclip

text = pyperclip.paste()

# Seperate lines & add asterisks
lines = text.split('\n')
for i in range(len(lines)):
    lines[i] = '* ' + lines[i]

text = '\n'.join(lines)

pyperclip.copy(text)

print(text)