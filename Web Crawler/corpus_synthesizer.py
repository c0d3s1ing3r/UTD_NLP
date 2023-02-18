import nltk
import os
import pickle

def clean_files(filename: str) -> None:
    '''Reads a text file and preprocesses the text, then writes the preprocessed text to a new file in the cleaned_pages directory'''
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    # remove newlines, tabs, and other strange characters
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')

    # extract sentences using nltk
    sentences = nltk.sent_tokenize(text)
    
    # write the sentences to a new file
    with open('./cleaned_pages/{}'.format(os.path.basename(filename)), 'w', encoding='utf-8') as f:
        for sentence in sentences:
            f.write(sentence)

def read_and_rank(head: int = 40) -> None:
    '''Reads all of the cleaned files and ranks them based on the number of times a word appears in the file'''
    
    # read all of the files in the cleaned_pages directory into a list
    files = []
    for filename in os.listdir('./cleaned_pages'):
        if filename.endswith('.txt'):
            with open('./cleaned_pages/{}'.format(filename), 'r', encoding='utf-8') as f:
                files.append(f.read())
    
    # remove punctuation and lowercase all words
    # also remove stopwords
    stopwords = nltk.corpus.stopwords.words('english')
    files = [[word.lower() for word in nltk.word_tokenize(file) if word.isalnum() and word.lower() not in stopwords] for file in files]

    # create a ranking of words based on tf
    # first create a dictionary of words and their frequencies
    word_freq = {}
    for file in files:
        for word in file:
            if word not in word_freq:
                word_freq[word] = 1
            else:
                word_freq[word] += 1
    
    # create a dictionary of words and their term frequencies
    term_freq = {}
    for word in word_freq:
        term_freq[word] = word_freq[word] / sum(word_freq.values())

    
    # sort the words by their scores
    sorted_words = sorted(term_freq, key=term_freq.get, reverse=True)

    # print the top N words
    for word in sorted_words[:head]:
        print(word, term_freq[word])
    
    # allow the user to choose 10 words to use as keywords
    keywords = []
    for i in range(10):
        keywords.append(input('Enter keyword {}: '.format(i+1)))
    
    # generate a knowledge base from the keywords and the complete corpus
    knowledge_base = {}
    for keyword in keywords:
        knowledge_base[keyword] = []
        for file in files:
            if keyword in file:
                knowledge_base[keyword].append(file)
    
    # save the knowledge base to a pickle file
    with open('./knowledge_base.pickle', 'wb') as f:
        pickle.dump(knowledge_base, f)
    

def main():
    # clear the cleaned pages directory of all txt files
    for file in os.listdir('./cleaned_pages'):
        if file.endswith('.txt'):
            os.remove('./cleaned_pages/{}'.format(file))
    # go through every file in the visited_pages directory and clean them
    for filename in os.listdir('./visited_pages'):
        if filename.endswith('.txt'):
            clean_files('./visited_pages/{}'.format(filename))
    
    # read and rank the cleaned files
    read_and_rank()

if __name__ == '__main__':
    main()