import csv
from indexer import Indexer
from retriever import Retriever

if __name__ == "__main__":
    indexer = Indexer('./cranfield_data.json')
    indexer.create_schema_file()
    indexer.print()
    retriever = Retriever("schema.json")

    squeries = [i[0] for i in (list(csv.reader(open("smallqueries.csv")))[1:])]
    srel = list(csv.reader(open("smallrelevance.csv")))[1:]
    sreldict = {}
    for i in srel:
        if i[0] in sreldict:
            sreldict[i[0]].append(i[1].strip())
        else:
            sreldict[i[0]] = [i[1].strip()]
    for k in 10, 50, 100:
        print("=======================================================")
        print("Searching for top ",k, " documents")
        avg = {"accuracy": 0,
               "precision": 0,
               "recall": 0,
               "f1_score": 0}
        for i in range(len(squeries)):
            docs, bench = retriever.query(
                squeries[i], k, get_bench=True, relevance_docs=sreldict[str(i+1)])
            print("query", i+1, ": ", bench)
            for b in bench:
                avg[b]+=bench[b]/10
                avg[b]=round(avg[b],4)
        print("AVERAGE:  ",avg,"\n\n")
