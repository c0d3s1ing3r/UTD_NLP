import sys
import os
import argparse
import nltk
from typing import Tuple, Dict
import pickle


def build_language_model(filename: str) -> Tuple[Dict, Dict]:
    '''Builds a language model from a file of text. Returns a tuple of two dictionaries, one for bigrams and one for unigrams.'''
    try:
        text = open(filename, 'r', encoding='utf-8').read()
    except UnicodeDecodeError:
        text = open(filename, 'r', encoding='latin-1').read()
    text = text.replace('\n', '')

    unigrams = nltk.word_tokenize(text)
    bigrams = list(nltk.bigrams(unigrams))

    # create bigram and unigram dictionaries
    unigram_dict = {u:unigrams.count(u) for u in set(unigrams)}
    bigram_dict = {b:bigrams.count(b) for b in set(bigrams)}

    return bigram_dict, unigram_dict

    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='Directory of LangId.train files to build language model from.')
    args = parser.parse_args()
    
    # grab all LangId.train files in the directory
    files = [os.path.join(args.directory, f) for f in os.listdir(args.directory) if f.startswith('LangId.train')]

    # build language model for each file
    for f in files:
        bigram_dict, unigram_dict = build_language_model(f)
        f = f.split('\\')[-1]
        f = f.split('.')[2]
        print(f'Building language model for {f}...')
        # print out the top 10 bigrams and unigrams
        print('Top 10 bigrams:')
        for b in sorted(bigram_dict, key=bigram_dict.get, reverse=True)[:10]:
            print(f'{b}: {bigram_dict[b]}')
        print('Top 10 unigrams:')
        for u in sorted(unigram_dict, key=unigram_dict.get, reverse=True)[:10]:
            print(f'{u}: {unigram_dict[u]}')
        
        # save the bigram and unigram dictionaries to pickle files
        with open(f'{f}.bigram.pickle', 'wb') as bigram_file:
            pickle.dump(bigram_dict, bigram_file)
        with open(f'{f}.unigram.pickle', 'wb') as unigram_file:
            pickle.dump(unigram_dict, unigram_file)
