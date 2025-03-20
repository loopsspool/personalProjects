#! python3

def collatz():
    choice = 'Y'
    while(choice == 'Y'):
        print('Please enter any nonzero positive number: ')
        try:
            number = int(input())
        except ValueError:
            print('Invalid input')
            continue
        if(number <= 0):
            print('Invalid input')
            continue
        acc = 0
        while(number != 1):
            if(number%2 == 0):
                number = number//2
            elif(number%2 == 1):
                number *= 3
                number += 1
            acc += 1
            print(number)
        print('Congrats! Your number is now 1! It took ' + str(acc) + ' steps for this algorithm to reach this point.')
        print('Would you like to play again? Enter Y/y or N/n')
        choice = input().upper()
    print('Thanks for playing!')


collatz()