import random

def guess_number():
    number = random.randint(1, 20)
    attempts = 0
    print("Guess a number between 1 and 20!")
    while True:
        guess = int(input("Your guess: "))
        attempts += 1
        if guess == number:
            print(f"Correct! You guessed it in {attempts} tries.")
            break
        elif guess < number:
            print("Go higher!")
        else:
            print("Go lower!")

guess_number()