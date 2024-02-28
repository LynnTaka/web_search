# -------------------------------------------------------------------------
# AUTHOR: lynn takahashi
# FILENAME: db_connection.py
# SPECIFICATION: description of the program
# FOR: CS 4250- Assignment #1
# TIME SPENT: 3 hrs
# -----------------------------------------------------------*/
# IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

# importing some Python libraries
import psycopg2
from datetime import datetime
date_format = "%Y-%m-%d"
date = datetime(2024,2,27)

def connectDataBase():
    # Create a database connection object using psycopg2
    DB_NAME = 'assignment2'
    DB_USER = 'postgres'
    DB_PASS = 'password'
    DB_HOST = 'localhost'
    DB_PORT = 5432
    try:
        conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST,
                                port=DB_PORT)
        print('database connected')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return conn


def createCategory(cur, catId, catName):
    # Insert a category in the database
    length = len(catName)
    cur.execute('INSERT INTO public."Categories" (id_cat, name, num_chars, date) VALUES (%s, %s, %s, %s)', (int(catId), catName,
                                                                                                   length, date))


def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    # 1 Get the category id based on the informed category name
    cur.execute('SELECT id_cat FROM public."Categories" WHERE name =%s', (docCat,))
    id_cat = cur.fetchone()[0]
    # print(id_cat)

    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # count number of alphanumeric characters
    num_chars = sum(c.isalnum() for c in docText)
    cur.execute('INSERT INTO public."Documents" (doc, text, title, num_chars, date, id_cat) VALUES (%s, %s, %s, %s, %s, %s)',
                (int(docId), docText, docTitle, int(num_chars), datetime.strptime(docDate, date_format), int(id_cat)))

    # 3 Update the potential new terms.
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    terms = [term.lower().strip('.,!?') for term in docText.split()]

    # 3.2 For each term identified, check if the term already exists in the database
    for term in set(terms):
        cur.execute('SELECT COUNT(*) FROM public."Terms" WHERE term = %s', (term,))
        count = cur.fetchone()[0]
        # print(count)

        # 3.3 In case the term does not exist, insert it into the database
        if count <= 0:
            cur.execute('INSERT INTO public."Terms" (term, num_chars) VALUES (%s, %s)', (term, len(term)))

    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    index = {}
    for term in set(terms):
        count = terms.count(term)
        index[term] = count

    # 4.3 Insert the term and its corresponding count into the database
    for term in index:
        count = int(index[term])
        cur.execute('INSERT INTO public."Term" (term, doc, term_count) VALUES (%s, %s, %s)', (term, int(docId), count))


def deleteDocument(cur, docId):
    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # in term index
    cur.execute('SELECT term FROM public."Term" WHERE doc = %s', (docId,))
    terms = cur.fetchall()

    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # if not in term delete terms
    for term in terms:
        term = term[0]
        cur.execute('DELETE FROM public."Term" WHERE doc = %s AND term = %s', (docId, term))
        cur.execute('SELECT COUNT(*) FROM public."Term" WHERE term = %s', (term,))
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute('DELETE FROM public."Terms" WHERE term = %s', (term,))

    # 2 Delete the document from the database
    cur.execute('DELETE FROM public."Documents" WHERE doc = %s', (docId,))


def updateDocument(cur, docId, docText, docTitle, docDate, docCat):
    # 1 Delete the document
    deleteDocument(cur, docId)

    # 2 Create the document with the same id
    createDocument(cur, docId, docText, docTitle, docDate, docCat)


def getIndex(cur):
    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # get from term
    cur.execute('SELECT term, title, term_count FROM public."Term" t INNER JOIN public."Documents" d ON d.doc = t.doc')
    rows = cur.fetchall()

    index = {}
    for term, doc, term_count in rows:
        if term not in index:
            index[term] = ''

        if index[term]:
            index[term] += ','
        index[term] += f'{doc}:{term_count}'

    print(index)
