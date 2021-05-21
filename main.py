from indexer import Indexer

if __name__ == "__main__":
    indexer = Indexer('./cranfield_data.json')
    indexer.create_schema_file()
    indexer.print()

