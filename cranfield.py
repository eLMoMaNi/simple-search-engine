"""This script uses cranfield dataset to evalute the search engine
"""

import csv
from indexer import Indexer
from retriever import Retriever

if __name__ == "__main__":
    indexer = Indexer('./cranfield_data.json')
    indexer.create_schema_file("schema.json")
    indexer.print()

    # create retriever object
    retriever = Retriever("schema.json")

    # load small queries from csv file
    squeries = [i[0] for i in (list(csv.reader(open("smallqueries.csv")))[1:])]

    # load relevent docs from csv file
    srel = list(csv.reader(open("smallrelevance.csv")))[1:]

    # convert list of pairs to {query_id:[<relevent docs>],...}
    sreldict = {}
    [sreldict.setdefault(i, []).append(j.strip()) for i, j in srel]

    # loop over diffrent `k` tests
    for k in 10, 50, 100:
        print("=======================================================")
        print("Searching for top ", k, " documents")

        avg = {"accuracy": 0, "precision": 0, "recall": 0, "f1_score": 0}

        # retrieve top `k` docs for each small query, and get benchmarks
        for i in range(len(squeries)):
            docs, bench = \
                retriever.query(
                    squeries[i], k,
                    get_bench=True, relevance_docs=sreldict[str(i+1)]
                )

            print("query", i+1, ":\t", bench)

            # calculate average benchmarks for each test
            for b in bench:
                avg[b] += bench[b]/10
                avg[b] = round(avg[b], 4)

        print("\nAVERAGE:\t", avg, "\n\n")
