import random

def get_random_word(filename):
    try:
        with open(filename, 'r') as file:
            words = file.readlines()
        words = [word.strip() for word in words if word.strip()]
        if not words:
            raise ValueError("The word file is empty.")
        return random.choice(words)
    except FileNotFoundError:
        print(f"File {filename} not found.")
        raise
    except Exception as e:
        print(str(e))
        raise

def get_hangman_stages(filename):
    try:
        with open(filename, 'r') as file:
            stages = file.read().split('###')
        stages = [stage.strip() for stage in stages if stage.strip()]
        if not stages:
            raise ValueError("The stages file is empty or incorrectly formatted.")
        return stages
    except FileNotFoundError:
        print(f"File {filename} not found.")
        raise
    except Exception as e:
        print(str(e))
        raise

def display_hangman(stages, tries):
    if 0 <= tries < len(stages):
        return stages[tries]
    else:
        return stages[-1]  # Display the last stage if tries are out of bounds

def play_game(words_file, stages_file):
    word = get_random_word(words_file)
    stages = get_hangman_stages(stages_file)
    word_letters = set(word)  # Letters in the word
    guessed_letters = set()  # Letters guessed by the user
    correct_letters = set()  # Correctly guessed letters
    tries = 6  # Number of tries

    print("Let's play Hangman!")

    while tries > 0:
        # Display the hangman stage and the current state of the word
        print(display_hangman(stages, tries))
        current_word = [letter if letter in correct_letters else '_' for letter in word]
        print(" ".join(current_word))

        if correct_letters == word_letters:
            print(f"Congratulations! You've guessed the word '{word}' correctly.")
            return

        guess = input("Guess a letter: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please guess a single letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.add(guess)

        if guess in word_letters:
            correct_letters.add(guess)
            print(f"Good job! '{guess}' is in the word.")
        else:
            tries -= 1
            print(f"Sorry, '{guess}' is not in the word. You have {tries} tries left.")

    print(f"Game over! The word was '{word}'.")

if __name__ == "__main__":
    words_file = 'words.txt'  # Replace with the correct path to your words file
    stages_file = 'stages.txt'  # Replace with the correct path to your stages file
    play_game(words_file, stages_file)
