#! python3

# Generalize for filepath and file types?
    # Also maybe check every file in folder and auto write ones that don't have the above specified

import sys
import os

save_dir = 'C:\\PythonScripts'

#if filename not included when called, asks for filename
if len(sys.argv) < 2:
    print('Please enter file name: ')
    file_name = str(input())
else:
    file_name = sys.argv[1]

complete_name = os.path.join(save_dir, file_name+'.bat')

#Checks if the file exists
exists = os.path.isfile(complete_name)
#if the file exists, don't do anything
if exists:
    print('This file already exists')
    sys.exit()
#if it doesn't exist, create and write it
else:
    file = open(complete_name, "w+")
    file.write('@py.exe C:\\PythonScripts\\' + file_name + '.py %*')
    file.close()
    print('Your batch file has been created and can now be executed from command line')
