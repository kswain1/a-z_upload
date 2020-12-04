import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

#use application default credentials 
cred = credentials.Certificate('/Users/kehlinswain/Documents/software_projects/a-z_upload/network/service-account-file.json')


default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'athletes')
athletes_ref = db.collection(u'athletes')
test_ref = db.collection(u'test')

## create write function 
def writeDocs(doc_ref, payload):
    doc_ref.document().set(payload)

def productTestNames(): 
    productTestResults = test_ref.stream()
    namesList = []
    for name in productTestResults:
        if name.to_dict().get('productTestName'):
            productTestName = name.to_dict()["productTestName"]
            print(productTestName)
            if productTestName in namesList:
                break
            namesList.append(productTestName)
    return namesList

#I can use the cloud functions as an alternative or use a javascript app
def readTestDocs():
    test_docs = test_ref.where(u'productTestName', u'==', u'Walmart Slip Study').stream()
    productTestName = test_ref.order_by(u'productTestName',direction=firestore.Query.DESCENDING)
    results = productTestName.stream()
    
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

def readTestDocsNew(testName):
    test_docs = test_ref.where(u'productTestName', u'==', testName).stream()
    productTestName = test_ref.order_by(u'productTestName',direction=firestore.Query.DESCENDING)
    results = productTestName.stream()
    
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


## create read function
def readDocs(doc_ref):
    object_docs = doc_ref.stream()
    hxObjects = []
    for docs in object_docs:
        print(docs.id, " =>", docs.to_dict())
        hxObjects.append(docs.to_dict())

print(default_app.name)
readTestDocs()
print('----------------')
readTestDocsNew(testName=u'Walmart Slip Study')