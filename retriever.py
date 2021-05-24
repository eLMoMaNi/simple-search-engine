import json
import math
import operator
from indexer import Indexer


class Retriever:
    def __init__(self, schema_file) -> None:
        self.__schema_file = schema_file
        self.schema = json.load(open(schema_file, "r"))

    def __create_query_vector(self, query_list):
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

    def __create_doc_vector(self, doc_id, query_list):
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

    def __cos_similarity(self, a, b):

        if len(a) != len(b):
            print(a, b)
            raise Exception("a and b must have the same lenght")
        sum = 0
        for i in range(len(a)):
            sum += a[i]*b[i]

        return sum

    def query(self, text, k=100, get_bench=False, relevance_docs=[]):
        """make a query from plain text and return top `k` relevant docs.
        `get_bench` returns the benchmarks as dict: `Accuracy, F1 , Precision, Recall`

        Args:
            text (str): plain text query
            k (int, optional): how many docs to retriev. Defaults to 100.
            get_bench (bool, optional): a flag to print benchmarks. Defaults to False.
            relevance_docs (list, optional): relevance docs to calculate benchmarks, must be passed 
            when `get_bench` is true
        """

        # preprocess plain text
        tokens = Indexer.preprocess(text)

        tokens = [token for token in tokens if token in self.schema]
        query_vector = self.__create_query_vector(tokens)

        doc_vectors = {}  # {doc_id:[<vector>]}

        for token in tokens:
            for doc in self.schema[token]:
                if doc in doc_vectors or doc == "idf":  # if vector already calculated
                    continue
                else:
                    doc_vectors[doc] = self.__create_doc_vector(doc, tokens)

        doc_scores = {}
        for doc in doc_vectors:
            doc_scores[doc] = self.__cos_similarity(
                query_vector, doc_vectors[doc])

        # sort docs by thier scores
        sorted_docs = sorted(doc_scores.items(), key=operator.itemgetter(1))
        ret = [i[0] for i in sorted_docs[-k:]]

        if get_bench:
            if not relevance_docs:
                raise Exception(
                    "print_bench is true but relevance_docs is empty")

            tp, fp, fn, tn = 0, 0, 0, 0
            for ret_doc in ret:
                if ret_doc in relevance_docs:
                    tp += 1
                else:
                    fp += 1
            for rel_doc in relevance_docs:
                if rel_doc not in ret:
                    fn += 1
            # TODO change this to getter value
            tn = 1400-(tp+fp+fn)
            accuracy = (tp+tn)/(tp+tn+fp+fn)
            precision = tp/(tp+fp)
            recall = tp/(tp+fn)
            f1_score = 0 if precision + \
                recall == 0 else (2*precision*recall)/(precision+recall)
            return [ret, {
                "accuracy": round(accuracy,4),
                "precision": round(precision,4),
                "recall": round(recall,4),
                "f1_score": round(f1_score,4)
            }
            ]

        return ret
