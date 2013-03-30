import time
import store
import settings as set
from SuperNode.query_handler import  coefficients as k
from SuperNode.query_handler import leave

def controller():
    db = store.call_db().get_db()

    for id in db:
        tempDoc = db[id]

        ## if credit less than zero leave all resources
        if tempDoc['info']['credit'] <= 0:
            leave.Leave(id, 11)
        else:
            tempDoc = check_credit(db[id])
            store.call_db().update_document(id,tempDoc)

def check_credit(doc):

    credit = doc['info']['credit']
    for key in doc['suppliedFrom'].keys():
        for i in range(len(doc['suppliedFrom'][key])):
            if time.time() - doc['suppliedFrom'][key][i]['timestamp'] >=  set.PERIOD:

                print "DEGISOOOOOOOO"
                doc['suppliedFrom'][key][i]['timestamp'] = time.time()
                trans_cost = doc['suppliedFrom'][key][i]['amount'] * k.dur

                store.call_db().update_credit(key,trans_cost)
                #tempSupplierDoc = store.call_db().get_document(key)
                #tempSupplierDoc['info']['credit'] += trans_cost
                #tempSupplierDoc['info']['effort'] = float(tempSupplierDoc['info']['credit'] * k.res) / \
                #                        (tempSupplierDoc['info']['capacity'] * k.cap )
                #store.call_db().update_document(key,tempSupplierDoc)

                credit -= trans_cost

    doc['info']['credit'] = credit
    doc['info']['effort'] = float(doc['info']['credit'] * k.res) / \
                                        (doc['info']['capacity'] * k.cap )

    return doc

if __name__ == "__main__":
    i = 0
    while i < 5:
        controller()
        time.sleep(set.SLEEP)
        db = store.call_db().get_db()
        print "\t -------------SLEEP:",i
        for j in db:
            print "\t", db[j]
        print "\t -------------SLEEP:",i
        i += 1