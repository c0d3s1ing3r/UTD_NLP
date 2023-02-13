from address import Address
import pickle
import nltk

def menu() -> int:
    # Display a menu and get the user's choice
    # returns selection number
    print('''
    Main menu:
1. See a list of Presidents
2. Look up addresses by President
3. Look for collocations in the inaugural corpus
9. Quit
''')
    try:
        selection = int(input('Enter your selection: '))
    except ValueError:
        print('Invalid selection. Try again.')
        return menu()
    return selection

def collocations(addresses: dict, phrase: str) -> float:
    # Look for collocations in the inaugural corpus
    # prompt user for 2 word phrase to search for collocations in the corpus
    # returns the PMI for that phrase
    # get the tokens for each address
    tokens = [address.tokens for address in addresses.values()]
    # flatten the token list
    flat_tokens = [token for sublist in tokens for token in sublist]
    # get the PMI for the phrase
    pmi = nltk.collocations.BigramAssocMeasures().pmi(flat_tokens.index(phrase.split(' ')[0]), flat_tokens.index(phrase.split(' ')[1]), len(flat_tokens))
    # print the PMI
    print(f'The PMI for {phrase} is {pmi}')
    return pmi


def main():
    # read in the pickle file
    with open('addresses.pickle', 'rb') as f:
        addresses = pickle.load(f)
    
    while True:
        selection = menu()
        if selection == 1:
            # See a list of Presidents
            for address in addresses.keys():
                print(address)
        elif selection == 2:
            # Look up addresses by President
            entry = input('Enter the name of the President and Year: ')
            try:
                print(addresses[entry])
            except KeyError:
                print('Invalid entry. Try again.')
                continue
        elif selection == 3:
            # Look for collocations in the inaugural corpus
            # prompt user for 2 word phrase to search for collocations in the corpus
            phrase = input('Enter a 2 word phrase: ')
            pmi = collocations(addresses, phrase)
            print(f'The PMI for {phrase} is {pmi}')
            
        elif selection == 9:
            # Quit
            break
        else:
            print('Invalid selection. Try again.')
            continue


if __name__ == "__main__":
    main()