#! python3

#this origram says hello & asks for your name

print('Hello world!')
print('What is your name?')
myName = input()
while myName == '' or myName == ' ':
    print('Enter a name, silly!')
    print('What is your name?')
    myName = input()
print('It is good to meet you, ' + myName)
print('The length of your name is: ')
print(len(myName))
print('What is your age?')
myAge = input()
print('You will be ' + str(int(myAge) + 1) + ' in a year!')
