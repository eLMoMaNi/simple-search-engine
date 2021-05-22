from indexer import preprocess 

class Retriever:
    def __init__(self, schema_file) -> None:
        self.__schema_file = schema_file

    def create_query_vector(self, query_list):
        raise NotImplementedError

    def create_doc_vector(self, doc_id, query_list):
        raise NotImplementedError

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
