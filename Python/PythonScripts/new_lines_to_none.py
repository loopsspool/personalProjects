import pyperclip

text = pyperclip.paste()

lines = text.split('\n')
realLines = []
realRealLines = []

# Removes white space
for i in range(len(lines)):
    if lines[i] == '\r':
        continue
    elif lines[i].endswith('\r') :
        realLines.append(lines[i].strip('\r'))
    else:
        realLines.append(lines[i])

# Combines character keys and their description, removing strange extra \
for i in range(0,len(realLines)-1,2):
    realRealLines.append('# ' + realLines[i] + ' -- ' + realLines[i+1])

text = '\n'.join(realRealLines)

pyperclip.copy(text)