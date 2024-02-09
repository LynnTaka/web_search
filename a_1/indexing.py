# -------------------------------------------------------------------------
# AUTHOR: Lynn Takahashi
# FILENAME: indexing.py
# SPECIFICATION: indexing.py will read the file collection.csv and output the tf-idf document-term matrix
# FOR: CS 4250- Assignment #1
# TIME SPENT: 1.5 hours
# -----------------------------------------------------------*/

# IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

# Importing some Python libraries
import csv
import math
from collections import Counter

documents = []

# Reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i, row in enumerate(reader):
        if i > 0:  # skipping the header
            documents.append(row[0])

# Conducting stopword removal. Hint: use a set to define your stopwords.
stopWords = {'i', 'and', 'she', 'her', 'they', 'their'}

# Conducting stemming. Hint: use a dictionary to map word variations to their stem.
# --> add your Python code here
steeming = {'love': 'love', 'loves': 'love', 'cat': 'cat', 'cats': 'cat', 'dog': 'dog', 'dogs': 'dog'}

# Identifying the index terms.
terms = []
for document in documents:
    row = []
    words = document.lower().split() #everything to lowercase
    for word in words:
        if word not in stopWords:
            stemmed_word = steeming[word] #dictionary
            row.append(stemmed_word)
    terms.append(row)

print(terms)

# Building the document-term matrix by using the tf-idf weights.
docTermMatrix = []
for term in terms:
    #count number of terms
    term_frequency = Counter(term)
    tfidf = []
    for word in term:
        tf = term_frequency[word]/len(term)
        print(term)
        print("term frequency: ", word, ' ', tf)

        # counter for how many documents words appears
        counter = 0
        for row in terms:
            if word in row:
                counter += 1

        idf = math.log10(len(documents) / counter)

        print("idf:", idf)
        temp = "{:.3f}".format(tf * idf)
        print(temp)
        tfidf.append(temp)

    docTermMatrix.append(tfidf)
# Printing the document-term matrix.
for row in docTermMatrix:
    print(row)
