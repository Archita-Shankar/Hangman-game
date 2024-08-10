# Hangman Game

This is a simple Hangman game implemented in Python. The game randomly selects a word from a list of words and allows the player to guess the letters in the word. The game provides visual feedback using hangman stages, showing the player's progress and how many tries are left.

## How to Play

- The game randomly selects a word from the `words.txt` file.
- The player guesses letters one by one.
- If the guessed letter is in the word, it is revealed in the correct positions.
- If the guessed letter is not in the word, a part of the hangman is drawn.
- The player has a limited number of tries (6 by default) to guess the word.
- The game ends when the player guesses the word correctly or runs out of tries.

![Screenshot 2024-08-10 235538](https://github.com/user-attachments/assets/6cd22112-0a99-4021-82c6-ae644c08582a)
![Screenshot 2024-08-10 235639](https://github.com/user-attachments/assets/eb6f0935-63d8-400b-9e37-3cd214924a3e)

## Files
- `app.py`: The main script to run the Hangman game.
- `words.txt`: A text file containing a list of words for the game.
- `stages.txt`: A text file containing the hangman stages, separated by `###`.

## Requirements

- Python 3.x

## Setup

1. Clone the repository or download the files.

2. Ensure you have Python 3.x installed on your system.

3. Run the `app.py` script to start the game.

