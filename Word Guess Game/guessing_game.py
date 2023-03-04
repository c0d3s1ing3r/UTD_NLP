import nltk
import sys
import random

def preprocess_text(text: str) -> tuple[list, list]:
    # convert to lower case
    text = text.lower()
    # tokenize
    tokens = nltk.word_tokenize(text)
    # alpha only
    words = [word for word in tokens if word.isalpha()]
    # not stop words
    words = [word for word in words if word not in nltk.corpus.stopwords.words('english')]
    # not too short
    words = [word for word in words if len(word) > 5]

    # lemmatize tokens
    lemmatizer = nltk.stem.WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(word) for word in words]
    unique_lemmas = set(lemmas)
    # pos tag unique lemmas and print first 20
    pos_tags = nltk.pos_tag(unique_lemmas)
    print(pos_tags[:20])

    # create list of lemmas that are nouns
    nouns = [lemma for lemma, pos in pos_tags if pos.startswith('N')]
    
    print(f'Number of tokens: {len(words)}')
    print(f'Number of nouns: {len(nouns)}')
    return words, nouns

def guessing_game(top_nouns: list[str]) -> None:
    cheat = True
    points = 5
    # randomly select a noun from the top 50 nouns
    noun = random.choice(top_nouns)
    guessed_letters = []
    remaining_letters = list(set(list(noun)))
    print('Let\'s play a word guessing game!')
    print(f'You have {points} points. Guess the noun.')
    print('Type ! to quit.')
    while points > 0:
        # print an underscore for each letter in the noun. If the letter has been guessed, print the letter
        print(' '.join([letter if letter in guessed_letters else '_' for letter in noun]))
        if cheat:
            print(f'The word is {noun}')
        # get user input
        guess = input('Guess a letter: ')
        guess = guess.lower().strip()
        guess = guess[0]

        if guess == '!':
            print('Thanks for playing!')
            print(f'The word was {noun}')
            print(f'Your final score is {points} points.')
            return

        while guess in guessed_letters:
            print('You already guessed that letter.')
            guess = input('Guess a letter: ')
            guess = guess.lower().strip()
        
        if guess in remaining_letters:
            print('Right!')
            guessed_letters.append(guess)
            remaining_letters.remove(guess)
            points += 1
        else:
            print('Sorry, guess again.')
            guessed_letters.append(guess)
            points -= 1
        
        if len(remaining_letters) == 0:
            print('You guessed the word!')
            print(f'The word was {noun}')
            print(f'You have {points} points.')
            print('Guess another word!')
            noun = random.choice(top_nouns)
            guessed_letters = []
            remaining_letters = list(set(list(noun)))
        
    print('GAME OVER')
    print(f'The word was {noun}')
    print('Thanks for playing. Better luck next time!')




if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python guessing_game.py <text_file>')
        sys.exit(1)
    in_text = sys.argv[1]

    in_text = open(in_text, 'r').read()

    # calculate lexical diversity of raw text to two decimal places
    tokens = nltk.word_tokenize(in_text)
    print(f'Lexical diversity: {len(set(tokens)) / len(tokens):.2f}')

    # preprocess text
    words, nouns = preprocess_text(in_text)

    # create dictionary of nouns and their counts
    noun_counts = {}
    for noun in nouns:
        if noun in noun_counts:
            noun_counts[noun] += 1
        else:
            noun_counts[noun] = 1
    
    # start guessing game with top 50 nouns
    top_nouns = sorted(noun_counts, key=noun_counts.get, reverse=True)[:50]
    guessing_game(top_nouns)
    
