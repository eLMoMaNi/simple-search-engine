import json
import math
from indexer import preprocess


class Retriever:
    def __init__(self, schema_file) -> None:
        self.__schema_file = schema_file
        self.schema = json.load(schema_file)

    def create_query_vector(self, query_list):
        """creates a normalized query vector using `ltc` weighting.

        Args:
            query_list (list): the query as list of strings.
        """
        query_vector = []

        for term in query_list:
            tf = query_list.count(term)
            idf = self.schema[term]["idf"]

            # using ltc weighting
            l = 1+math.log10(tf)
            t = math.log10(idf)

            tf_idf = l*t
            query_vector.append(tf_idf)

        norm = math.sqrt(sum(i*i for i in query_vector))

        normalized_vector = [i/norm for i in query_vector]
        return normalized_vector

    def create_doc_vector(self, doc_id, query_list):
        """creates a normalized doc vector using `lnc` weighting.

        Args:
            doc_id (str): document id
            query_list (list): the doc as list of strings.
        """

        doc_vector = []
        for term in query_list:
            if doc_id in self.schema[term]:
                tf = self.schema[term][doc_id]

                l = 1+math.log10(tf)
                doc_vector.append(l)
            else:
                doc_vector.append(0)
        
        norm = math.sqrt(sum(i*i for i in doc_vector))

        normalized_vector = [i/norm for i in doc_vector]
        return normalized_vector
        

    def cos_similarity(self):
        raise NotImplementedError

    def query(self, text, k=100, print_bench=False):
        """make a query from plain text and return top `k` relevant docs.
        `print_bench` prints the benchmarks: `Accuracy, F1 , Precision, Recall`

        Args:
            text (str): plain text query
            k (int, optional): how many docs to retriev. Defaults to 100.
            print_bench (bool, optional): a flag to print benchmarks. Defaults to False.
        """
        raise NotImplementedError
