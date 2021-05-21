* Ahmad Momani
* 134081

# Part A
the code will first load JSON file that contain all docs, then it will loop over each doc.
in each loop, it will tokenize the whole text then it will update the `words` dictionary, which contain each token with its occurnce.

after that, we can get all requiered details from words dictionary or from the variable `tokens_count`.

# Part B
we will make an Inverted Index schema called `dictionary`. it will have this structure : 
```
{
    "word": {docId : tf,
             docId : tf}
}
```
