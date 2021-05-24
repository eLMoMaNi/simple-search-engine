import json
import math
import operator
from indexer import Indexer


class Retriever:
    """ This class used to search throw index schema and make queries.
    It calculate cosine similarity for all documents in schema 
    sequntially for each query.
    """

    def __init__(self, schema_file) -> None:

        self.__schema_file = schema_file
        self.schema = json.load(open(schema_file, "r"))

    def __normalize_vector(self, raw_vector):
        """Normalize a vector by converting it to its unit vector.

        Args:
            raw_vector (list[float]): the vector to be normalized

        Returns:
            list[float]: the normalized unit vector
        """
        norm = math.sqrt(sum(i*i for i in raw_vector))
        normalized_vector = [i/norm for i in raw_vector]
        return normalized_vector

    def __create_query_vector(self, query_list):
        """creates a normalized query vector using `ltc` weighting.

        Args:
            query_list (list[str]): query terms.
        Returns:
            list[float]: normalized query vector
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

        normalized_vector = self.__normalize_vector(query_vector)
        return normalized_vector

    def __create_doc_vector(self, doc_id, query_list):
        """creates a normalized doc vector using `lnc` weighting for
        query terms only.

        Args:
            doc_id (str): document id
            query_list (list[str]): query terms.
        Returns:
            list[float]: normalized doc vector from query terms
        """

        doc_vector = []
        for term in query_list:
            if doc_id in self.schema[term]:
                tf = self.schema[term][doc_id]

                l = 1+math.log10(tf)
                doc_vector.append(l)
            else:
                doc_vector.append(0)

        normalized_vector = self.__normalize_vector(doc_vector)

        return normalized_vector

    def __cos_similarity(self, a, b):
        """calculates the cosine similarity between two vectors

        Args:
            a (list[float]): the first vector
            b (list[float]): the second vector

        Raises:
            Exception: raised when two vectors (list) have different length

        Returns:
            float: cosine similarity
        """

        if len(a) != len(b):
            print(a, b)
            raise Exception("a and b must have the same lenght")
        sum = 0
        for i in range(len(a)):
            sum += a[i]*b[i]

        return sum

    def __benchmark(self, top_docs, relevance_docs, decimal_points):
        """calculates the benchmarks `Accuracy, F1 , Precision, Recall`.

        Args:
            top_docs (list[str]): ids of top retrieved docs
            relevance_docs (list[str]): the actual relevent docs
            decimal_points (int): number of decimal points to round to

        Returns:
            dict[str,float]: values for each benchmark 
        """
        tp, fp, fn, tn = 0, 0, 0, 0

        for top_doc in top_docs:
            if top_doc in relevance_docs:
                tp += 1
            else:
                fp += 1

        for rel_doc in relevance_docs:
            if rel_doc not in top_docs:
                fn += 1

        tn = 1400-(tp+fp+fn)  # TODO change this to getter value
        accuracy = (tp+tn)/(tp+tn+fp+fn)
        precision = tp/(tp+fp)
        recall = tp/(tp+fn)
        f1_score = 0 if precision + \
            recall == 0 else (2*precision*recall)/(precision+recall)

        return {
            "accuracy": round(accuracy, decimal_points),
            "precision": round(precision, decimal_points),
            "recall": round(recall, decimal_points),
            "f1_score": round(f1_score, decimal_points)
        }

    def query(self, text, k=100, get_bench=False, relevance_docs=[], decimal_points=4):
        """make a query from plain text and return top `k` relevant docs.
        `get_bench` returns the benchmarks as dict: `Accuracy, F1 , Precision, Recall`

        Args:
            text (str): plain text query
            k (int, optional): how many docs to retriev. Defaults to 100.
            get_bench (bool, optional): a flag to print benchmarks. Defaults to False.
            relevance_docs (list, optional): relevance docs to calculate benchmarks, must be passed 
            when `get_bench` is true
        Returns:
            list[srt]: list of top docs ids
            list[object]: a list contain list of top docs ids, and a 
            dictionary for benchmarks
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
            doc_scores[doc] = \
                self.__cos_similarity(query_vector, doc_vectors[doc])

        # sort docs by thier scores
        sorted_docs = sorted(doc_scores.items(), key=operator.itemgetter(1))
        # get only top `k` docs ids
        top_docs = [i[0] for i in sorted_docs[-k:][::-1]]

        if get_bench:
            if not relevance_docs:
                raise Exception(
                    "print_bench is true but relevance_docs is empty")
            return \
                [
                    top_docs,
                    self.__benchmark(top_docs, relevance_docs, decimal_points)
                ]

        return [top_docs]
