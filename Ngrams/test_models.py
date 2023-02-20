import pickle
import os
import argparse
import nltk




if __name__ == '__main__':
    
    # take the test and solution files as an argument
    parser = argparse.ArgumentParser()
    parser.add_argument('test_file', help='Test file to test language model on.')
    parser.add_argument('solution_file', help='Solution file to compare test file to.')
    args = parser.parse_args()

    # load in each language's bigram and unigram dictionaries
    bigram_dictionaries = {}
    unigram_dictionaries = {}
    for f in os.listdir('./'):
        if f.endswith('.bigram.pickle'):
            with open(os.path.join('./', f), 'rb') as bigram_file:
                bigram_dictionaries[f.split('.')[0]] = pickle.load(bigram_file)
        elif f.endswith('.unigram.pickle'):
            with open(os.path.join('./', f), 'rb') as unigram_file:
                unigram_dictionaries[f.split('.')[0]] = pickle.load(unigram_file)

    # print out the top 10 bigrams and unigrams for each language
    for language in bigram_dictionaries:
        print(f'Top 10 bigrams for {language}:')
        for b in sorted(bigram_dictionaries[language], key=bigram_dictionaries[language].get, reverse=True)[:10]:
            print(f'{b}: {bigram_dictionaries[language][b]}')
        print(f'Top 10 unigrams for {language}:')
        for u in sorted(unigram_dictionaries[language], key=unigram_dictionaries[language].get, reverse=True)[:10]:
            print(f'{u}: {unigram_dictionaries[language][u]}')
    
    print('Successfully loaded language models.')

    # iterate through test and solution files simultaneously
    with open(args.test_file, 'r', encoding='utf-8') as test_file, open(args.solution_file, 'r', encoding='utf-8') as solution_file:
        test_lines = test_file.readlines()
        solution_lines = solution_file.readlines()
        results = []
        for test_line, solution_line in zip(test_lines, solution_lines):
            # get the language of the solution line
            solution_language = solution_line.split()[1]
            test_number = solution_line.split()[0]
            # get the bigrams and unigrams of the test line
            test_unigrams = nltk.word_tokenize(test_line)
            test_bigrams = list(nltk.bigrams(test_unigrams))
            # calculate the probability of the test line for each language using laplace smoothing
            # (b + 1) / (u + v) where b is the bigram count, u is the unigram count
            # of the first word in the bigram, and v is the total vocabulary size 
            # (add the lengths of the 3 unigram dictionaries). 
            probabilities = {}
            for language in bigram_dictionaries:
                bigram_count = 0
                unigram_count = 0
                for bigram in test_bigrams:
                    if bigram in bigram_dictionaries[language]:
                        bigram_count += bigram_dictionaries[language][bigram]
                    if bigram[0] in unigram_dictionaries[language]:
                        unigram_count += unigram_dictionaries[language][bigram[0]]
                probabilities[language] = (bigram_count + 1) / (unigram_count + len(unigram_dictionaries['English']) + len(unigram_dictionaries['French']) + len(unigram_dictionaries['Italian']))
            
            print(probabilities)

            # get the language with the highest probability
            predicted_language = max(probabilities, key=probabilities.get)
            print(f'Test {test_number} predicted language: {predicted_language}')
            print(f'Test {test_number} actual language: {solution_language}')
            print()

            # add the result to the results list
            # true if the predicted language is the same as the solution language
            results.append(predicted_language == solution_language)
        
        print('Completed testing.')
        print(f'Number of tests: {len(results)}')
        print('Results...')

        # print out the accuracy of the language model
        accuracy = sum(results) / len(results)
        print(f'Accuracy: {accuracy}')

        # print all incorrect predictions
        for i, result in enumerate(results):
            if not result:
                print(f'Test {i+1} was incorrect.')
                


            
