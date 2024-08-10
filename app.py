from flask import Flask, request, jsonify, render_template
import random

app = Flask(__name__)

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
            stages = file.read().strip().split('###')
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

def initialize_game():
    word = get_random_word('words.txt')
    stages = get_hangman_stages('stages.txt')
    return {
        'word': word,
        'stages': stages,
        'word_letters': set(word),
        'guessed_letters': set(),
        'correct_letters': set(),
        'tries': 6
    }

game_state = initialize_game()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game_state')
def get_game_state():
    current_word = [letter if letter in game_state['correct_letters'] else '_' for letter in game_state['word']]
    stage = display_hangman(game_state['stages'], game_state['tries'])
    return jsonify({
        'word': ' '.join(current_word),
        'stage': stage,
        'message': f'You have {game_state["tries"]} tries left.'
    })

@app.route('/submit_guess', methods=['POST'])
def submit_guess():
    global game_state
    guess = request.json.get('letter').lower()

    if len(guess) != 1 or not guess.isalpha():
        return jsonify({'message': 'Invalid input. Please guess a single letter.'})

    if guess in game_state['guessed_letters']:
        stage = display_hangman(game_state['stages'], game_state['tries'])
        current_word = [letter if letter in game_state['correct_letters'] else '_' for letter in game_state['word']]
        return jsonify({'word': ' '.join(current_word), 'stage': stage, 'message': 'You already guessed that letter.'})

    game_state['guessed_letters'].add(guess)

    if guess in game_state['word_letters']:
        game_state['correct_letters'].add(guess)
        message = f"Good job! '{guess}' is in the word."
    else:
        game_state['tries'] -= 1
        message = f"Sorry, '{guess}' is not in the word. You have {game_state['tries']} tries left."

    current_word = [letter if letter in game_state['correct_letters'] else '_' for letter in game_state['word']]
    stage = display_hangman(game_state['stages'], game_state['tries'])

    if game_state['correct_letters'] == game_state['word_letters']:
        message = f"Congratulations! You've guessed the word '{game_state['word']}' correctly."
        game_state = initialize_game()  # Reset the game after win

    if game_state['tries'] <= 0:
        message = f"Game over! The word was '{game_state['word']}'."
        game_state = initialize_game()  # Reset the game after loss

    return jsonify({
        'word': ' '.join(current_word),
        'stage': stage,
        'message': message
    })

@app.route('/reset_game')
def reset_game():
    global game_state
    game_state = initialize_game()
    current_word = [letter if letter in game_state['correct_letters'] else '_' for letter in game_state['word']]
    stage = display_hangman(game_state['stages'], game_state['tries'])
    return jsonify({
        'word': ' '.join(current_word),
        'stage': stage,
        'message': 'Game has been reset. You have 6 tries left.'
    })

if __name__ == "__main__":
    app.run(debug=True)
