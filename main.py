import json
import operator
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *

# PART A


def preprocess(text):
    # pre-process the text then tokenize it

    def clean(text):
        # removes stopwords, stemm words, remove small words[less than 2 letters]

        # creating Porter stemmer
        stemmer = PorterStemmer()

        # stemming all words in the text
        stemmed = [stemmer.stem(word) for word in text]

        # load stop words as set
        stop_words = set(stopwords.words('english'))

        # remove stopwords from stemmed words
        filtered = [w for w in stemmed if not w in stop_words]

        # remove words with less than 2 letters
        longwords = [w for w in filtered if len(w) > 2]

        return longwords

    # create tokenizer that accept only words (no punctuations or numbers)
    tokenizer = nltk.RegexpTokenizer(r"\w+")

    tokenized = tokenizer.tokenize(text)

    # clean the text
    return clean(tokenized)


def getDocs(json_file='./cranfield_data.json'):
    return json.load(open(json_file))


def print_info(docs):
    
    # initilize variables
    tokens_count = 0    # tokens count
    words = {}      # a dictionary to store all words with their occurrence count

    # load documents
    docs = getDocs()

    for doc in docs:

        tokens = preprocess(doc["body"])

        tokens_count += len(tokens)

        for token in tokens:
            if token in words:
                words[token] += 1
            else:
                words[token] = 1

    # sort the words list by their occurrence count
    sorted_words = sorted(words.items(), key=operator.itemgetter(1))
    # words that appeared only once
    once = []
    for i, j in sorted_words:
        if j > 1:
            break
        once.append(i)

    # printing part 1:
    print("Number of tokens:", tokens_count)
    print("The number of unique words:", len(words))
    print("The number of words that occur only once:", len(once))
    print("The 30 most frequent words:\n", sorted_words[-30:])
    print("The average number of word tokens per document:", tokens_count/1400)


# PART B
def create_schema():

    dictionary = {}   # I will use Inverted Index dictionary
    # I used this structure : {"word": {docId:tf}}
    for doc in docs:
        tokens = preprocess(doc["body"])
        for token in tokens:

            if token in dictionary:
                if doc["id"] in dictionary[token]:
                    dictionary[token][doc["id"]] += 1
                else:
                    dictionary[token][doc["id"]] = 1
            else:
                dictionary[token] = {doc["id"]: 1}

    json.dump(dictionary, open("./dictionary.json", "w"))
