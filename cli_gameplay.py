from helper import *

def main():

    countries = create_countries_list()

    print_countries(countries) # <-- uncomment for cheat sheet

    streak = 0

    for name, description, answer_set in countries:

        streak_message(streak)
        
        chances = 5
        guess_num = 1
        
        print(description)
        print()
        print("What country does this flag belong to?\n")

        while chances > 0:
            print(f"You have {chances} chances remaining!")
            guess = input(f"Guess #{guess_num}: ")

            if normalize(guess) not in answer_set:
                chances -= 1
                guess_num += 1

                if chances != 0:
                    print(f"\nSorry, {guess} is not correct! Try again.")
                    streak = 0

                if chances == 0:
                    print(f"\nYou lose! The correct answer was {name}")
                    streak = 0

            else:
                print(f"\nYou win! It was {name}")
                streak += 1
                break

        while True:
            print("\nWould you like to keep playing?")
            keep_playing = input("Input (y/n): ").lower()

            if keep_playing == "y" or keep_playing == "":
                print()
                break
            elif keep_playing == "n":
                print(f"\nThanks for playing! Your latest streak was {streak}")
                exit()
            else:
                print("Not a valid input!")

    print("Wow! You literally beat the entire game! I actually can't believe it... 197 in a row!")

def streak_message(s):
    if s > 1:
        print(f"You have a streak of {s}!")
    if s == 10:
        print("Keep it up! You are on fire")
    if s == 20:
        print("You're a pro!")

    if s>1:
        print()

if __name__ == "__main__":
    main()