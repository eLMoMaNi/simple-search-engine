import json
import operator

import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *


class Indexer:

    def __init__(self, json_docs) -> None:
        self.json_docs = json_docs
        self.__docs = self.__getDocs(json_docs)

    def __getDocs(self, json_file):
        return json.load(open(json_file))

    def update(self, json_docs=None):
        if json_docs == None:
            self.__init__(self.json_docs)
        else:
            self.__init__(json_docs)

    # ? change this paradigm to a better approach
    @classmethod
    def preprocess(cls, text):
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

    def print(self):

        # initilize variables
        tokens_count = 0    # tokens count
        words = {}      # a dictionary to store all words with their occurrence count

        # load documents

        for doc in self.__docs:

            tokens = self.preprocess(doc["body"]+doc["title"])

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

    def create_schema_file(self, output_filename="schema.json"):

        schema = {}   # I will use Inverted Index schema
        # I used this structure : {"word": {docId:tf}}
        for doc in self.__docs:
            tokens = self.preprocess(doc["body"]+" "+doc["title"])
            for token in tokens:

                if token in schema:
                    if doc["id"] in schema[token]:
                        schema[token][doc["id"]] += 1
                    else:
                        schema[token][doc["id"]] = 1
                else:
                    schema[token] = {doc["id"]: 1}
        for term in schema:
            schema[term]["idf"]=len(self.__docs)/len(schema[term])

        json.dump(schema, open(output_filename, "w"))
