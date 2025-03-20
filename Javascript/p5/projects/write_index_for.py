#! python3

# Generalize for filepath and file types?
    # Also maybe check every file in folder and auto write ones that don't have the above specified

import sys
import os

save_dir = '..\Users\ejone\Desktop\Code\Javascript\p5\projects'

#if filename not included when called, asks for filename
if len(sys.argv) < 2:
    print('Please enter file name: ')
    file_name = str(input())
else:
    file_name = sys.argv[1]

complete_name = os.path.join(save_dir, file_name+'Index.html')

#Checks if the file exists
exists = os.path.isfile(complete_name)
#if the file exists, don't do anything
if exists:
    print('This file already exists')
    sys.exit()
#if it doesn't exist, create and write it
else:
    file = open(complete_name, "w+")
    file.write('''
        <html>
            <head>
                <script src="../libraries/p5.js" type="text/javascript"></script>
                <script src="../libraries/p5.dom.js" type="text/javascript"></script>
                <script src="../libraries/p5.sound.js" type="text/javascript"></script>
                <script src="../images"></script>
                <script src="../libraries/cook-js-master/b2.js"></script>
                <script src="../libraries/cook-js-master/box2d-html5.js"></script>
                <script src="../libraries/cook-js-master/p5.particle.js"></script>
                <script src="noiseDisplay.js"></script>
                <style> body{padding:0; margin:0;} </style>
            </head>
        </html>
    ''')
    file.close()
    print('Your index file has been created')
