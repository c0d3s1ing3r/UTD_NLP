import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import pickle
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

class Address:

    def __init__(self):
        self.year = 0
        self.president = ""
        self.original_text = ""
        self.token_length = 0
        self.tokens = []
        self.top_25_tokens = []
        self.readability_score = 0
        self.readability_rating = ""
        self.sentiment_score = {}
    
    def compute_readability(self) -> None:
        # Compute the readability score and rating
        # based on the the Lasbarhetsindex (LIX)
        # readability = W / S + (L * 100)/W
        # W = The total number of words
        # S = The total number of sentences
        # L = The total number of long words (over 6 characters)
        
        # Count the number of sentences
        sentences = self.original_text.split('.')
        sentences = [sentence for sentence in sentences if len(sentence) > 0]
        sentence_count = len(sentences)

        # Count the number of words
        word_count = len(self.tokens)

        # Count the number of long words
        long_words = [word for word in self.tokens if len(word) > 6]
        long_word_count = len(long_words)

        # Compute the readability score
        self.readability_score = word_count / sentence_count + (long_word_count * 100) / word_count

        # Compute the readability rating
        # <25 Children
        # 25-30 Simple 
        # 30-40 Normal 
        # 40-50 Factual 
        # 50-60 Technical
        # >60 Difficult
        if self.readability_score < 25:
            self.readability_rating = 'Children'
        elif self.readability_score < 30:
            self.readability_rating = 'Simple'
        elif self.readability_score < 40:
            self.readability_rating = 'Normal'
        elif self.readability_score < 50:
            self.readability_rating = 'Factual'
        elif self.readability_score < 60:
            self.readability_rating = 'Technical'
        else:
            self.readability_rating = 'Difficult'


    def compute_sentiment(self) -> None:
        # Compute the sentiment score
        # based on the VADER sentiment analysis
        self.sentiment_score = analyzer.polarity_scores(self.original_text)

        

    def __str__(self) -> str:
        # Return a string representation of the Address object
        # print all attributes, but only first few lines of original text
        ret = f'''
Year: {self.year}
President: {self.president}
Readability Score: {self.readability_score}
Readability Rating: {self.readability_rating}
Sentiment Score: {self.sentiment_score}
Top 25 Tokens: {self.top_25_tokens}
Tokens: {self.tokens}
Token Length: {self.token_length}
Original Text: {self.original_text[:100]}...
'''
        return ret


    def __repr__(self) -> str:
        return self.__str__()


def main():
    # go through every file in the inagurals corpus
    # create an Address object for each file
    # compute the readability and sentiment scores
    # print the results
    addresses = {}
    for filename in os.listdir('./inaugural'):
        if filename.endswith('.txt'):
            year, president = filename.split('-')
            address = Address()
            address.year = int(year)
            address.president = president[:-4]
            with open(os.path.join('./inaugural', filename), 'r') as f:
                address.original_text = f.read()
            text = address.original_text.lower()
            address.tokens = word_tokenize(text)
            address.tokens = [token for token in address.tokens if token.isalpha()]
            address.tokens = [token for token in address.tokens if token not in stopwords.words('english')]
            address.top_25_tokens = [token for token, count in nltk.FreqDist(address.tokens).most_common(25)]
            address.token_length = len(address.tokens)
            address.compute_readability()
            address.compute_sentiment()
            addresses[address.president+'-'+str(address.year)] = address
            print(address)
    
    # save the addresses to a pickle file
    with open('addresses.pickle', 'wb') as f:
        pickle.dump(addresses, f)
    

if __name__ == "__main__":
    main()