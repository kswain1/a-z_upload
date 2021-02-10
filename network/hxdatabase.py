import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
#use application default credentials 
#cred = credentials.Certificate('/Users/kehlinswain/Documents/software_projects/a-z_upload/network/service-account-file.json')
cred = credentials.Certificate(os.path.join('network','service-account-file.json'))


default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'athletes')
athletes_ref = db.collection(u'athletes')
test_ref = db.collection(u'test')
user_ref = db.collection(u'users')

## create write function 
def writeDocs(doc_ref, payload):
    doc_ref.document().set(payload)

def productTestNames(): 
    namesList = []

    productTest = test_ref.order_by(u'productTestName',direction=firestore.Query.DESCENDING)
    results = productTest.stream()
    for name in results: 
        productTestName = name.to_dict()['productTestName']
        if productTestName not in namesList: 
            namesList.append(productTestName)
         
    return namesList

#I can use the cloud functions as an alternative or use a javascript app
def readTestDocs():
    test_docs = test_ref.where(u'productTestName', u'==', u'Walmart Slip Study').stream()
    productTestName = test_ref.order_by(u'productTestName',direction=firestore.Query.DESCENDING)
    results = productTestName.stream()
    for docs in results: 
        print(docs.to_dict(), "----/n")
    productNames = []
    fatigueScores = []
    comfortScores = []
    fatigueScores = []
    htScores = []
    test_results =[]
    for docs in test_docs: 
        productNames.append(docs.to_dict()['shoeName'])
        comfortScores.append(docs.to_dict()['comfort'])
        fatigueScores.append(docs.to_dict()['fatigue'])
        htScores.append(docs.to_dict()['htScore'])
        test_results.append(docs.to_dict())
    #print(test_results, "hello")
    return test_results
    #query_ref = cities_ref.where(u'state', u'==', u'CA')
    #https://firebase.google.com/docs/firestore/query-data/queries

def readUserProductList(uid):
    user_docs = user_ref.document(uid).get()
    # print("user   -->>>> ", user_docs.get('products'))
    # print(user_docs)
    return user_docs.get('products')
    

def readTestDocsNew(testName):
    test_docs = test_ref.where(u'productTestName', u'==', testName).stream()
    productTestName = test_ref.order_by(u'productTestName',direction=firestore.Query.DESCENDING)
    results = productTestName.stream()
    # for docs in results: 
    #     print(docs.to_dict())
    productNames = []
    fatigueScores = []
    comfortScores = []
    fatigueScores = []
    htScores = []
    test_results =[]
    for docs in test_docs: 
        productNames.append(docs.to_dict()['shoeName'])
        comfortScores.append(docs.to_dict()['comfort'])
        fatigueScores.append(docs.to_dict()['fatigue'])
        htScores.append(docs.to_dict()['htScore'])
        test_results.append(docs.to_dict())
    print(test_results, "hello")
    return test_results


## create read function
def readDocs(doc_ref):
    object_docs = doc_ref.stream()
    hxObjects = []
    for docs in object_docs:
        print(docs.id, " =>", docs.to_dict())
        hxObjects.append(docs.to_dict())


def deleteRepeatedTestDocs():
    results = test_ref.order_by(u'shoeName',direction=firestore.Query.DESCENDING)
    results = results.stream()
    name = []
    for doc in results: 
        productName = doc.to_dict()['shoeName']
        if productName not in name: 
            name.append(productName)
        else: 
            #delete document
            #print(doc.id)
            test_ref.document(doc.id).delete()
print(default_app.name)
#readTestDocs()
#print('----------------')
#readTestDocsNew(testName=u'Walmart Slip Study')
#print(productTestNames())
#deleteRepeatedTestDocs()