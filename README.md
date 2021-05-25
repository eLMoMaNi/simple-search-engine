# simple-search-engine
This repo is a simple study of **Information Retrieval** (IR), it's a simple search engine tool implemented using Python3. It uses [Cranfield experiments](https://en.wikipedia.org/wiki/Cranfield_experiments) [dataset](http://ir.dcs.gla.ac.uk/resources/test_collections/cran/) to evaluate retrieved results.

# Table of contents
- [Installing](#installing)
- [Usage](#usage)
  * [Using the Indexer](#using-the-indexer)
    + [Creating the Indexer](#creating-the-indexer)
    + [Creating schema file](#creating-schema-file)
    + [Printing indexed documents statics](#printing-indexed-documents-statics)
  * [Creating and using the Retriever](#creating-and-using-the-retriever)
    + [Make a query](#make-a-query)
    + [Getting benchmarks](#getting-benchmarks)
- [Credits](#credits)

# Installing 

```sh
git clone https://github.com/eLMoMaNi/simple-search-engine
cd ./simple-search-engine
pip install -r requirements.txt
#copy files to site-packages or create your files in same directory
```

# Usage
## Using the Indexer
### Creating the Indexer 

```python
from indexer import Indexer
indexer = Indexer('/path/to/cranfield_data.json')
```
Cranfield collection must be converted to a json file.
### Creating schema file

```python
indexer.create_schema_file("schema.json")
```
### Printing indexed documents statics

```python
indexer.print()
```
this will print some info like this:

```dart
Number of tokens: 140979
The number of unique words: 4500
The number of words that occur only once: 1488
The 10 most frequent words: flow, pressur, number, boundari \...
```
## Creating and using the Retriever

```python
retriever = Retriever("schema.json")
```
once the Retriever is created. we can use it to seach documents (make queries).
### Make a query
this shows how to get top `100` documents for a query.

```python
docs, = retriever.query("how to hack NASA using HTML",100)
```
### Getting benchmarks

```python
docs, = retriever.query("how to hack NASA using HTML",100\
                        ,get_bench=True, relevance_docs=[<doc IDs>])
```
relevance_docs gets a list of IDs of the relevent documents to evalute the `Accuracy, F1 , Precision and Recall`.


# Credits

 - [tqdm](https://github.com/tqdm/tqdm) for the porgress bar
 - [Dr. Malak  Abdullah](https://sites.google.com/view/malak-abdullah/home) for the course project
 - Cranfield University for the dataset
 - [me @_@](https://github.com/eLMoMaNi) as the creator of the repo
