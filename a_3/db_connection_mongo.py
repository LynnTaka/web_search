#-------------------------------------------------------------------------
# AUTHOR: lynn takahashi
# FILENAME: db_connection_mongo.py
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #3
# TIME SPENT: 1.5
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
import pymongo


def connectDataBase():
    # Create a database connection object using pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["documents"]
    return db


def createDocument(col, docId, docText, docTitle, docDate, docCat):

    # create a dictionary indexed by term to count how many times each term appears in the document.
    term_count = {}
    terms = docText.lower().split(" ")
    for term in terms:
        term = term.strip()
        if term not in term_count:
            term_count[term] = 1
        else:
            term_count[term] += 1

    # create a list of objects to include full term objects. [{"term", count, num_char}]
    terms = []
    for term, count in term_count.items():
        terms.append({'term': term, 'count':count, 'num_char': len(term)})

    # produce a final document as a dictionary including all the required document fields
    document = {
        'docId': docId,
        'text': docText,
        'title': docTitle,
        'date': docDate,
        'category': docCat,
        'terms': terms
    }
    # insert the document
    col.insert_one(document)

def deleteDocument(col, docId):
    # Delete the document from the database
    col.delete_one({'docId': docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    deleteDocument(col, docId)

    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)

def getIndex(col):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    index = {}

    cursor = col.find({}, {"terms": 1})
    for doc in cursor:
        for term_obj in doc["terms"]:
            term = term_obj["term"]
            doc_id = doc["title"]
            if term not in index:
                index[term] = f"{doc_id}:{term_obj['count']}"
            else:
                index[term] += f",{doc_id}:{term_obj['count']}"
    return index

