import time
import store
import settings as set
from SuperNode.query_handler import  coefficients as k
from SuperNode.query_handler import leave
import logging


loggerCont = logging.getLogger('Controller')

def controller():

    global loggerCont
    loggerCont.info("Checks the database at %s" %time.time())

    db = store.call_db().get_db()
    for id in db:
        tempDoc = db[id]
        ## if credit less than zero leave all resources
        if tempDoc['info']['credit'] <= set.TOLERANT:
            loggerCont.info("The ON: %s  does not have enough credit to hold the resources. Will leave all", tempDoc['_id'])
            leave.Leave(id, 11)
        else:
            check_credit(id,db[id])



def check_credit(id,doc):

    global loggerCont

    credit = doc['info']['credit']
    for key in doc['suppliedFrom'].keys():
        for i in range(len(doc['suppliedFrom'][key])):
            if time.time() - doc['suppliedFrom'][key][i]['timestamp'] >=  set.PERIOD:

                doc['suppliedFrom'][key][i]['timestamp'] = time.time()
                trans_cost = doc['suppliedFrom'][key][i]['amount'] * k.dur

                store.call_db().update_credit(key,1*trans_cost)
                credit -= trans_cost
                loggerCont.info("the node:%s is gained %s credit from node:%s" %(key,trans_cost,id))


    loggerCont.info("The node: %s is charged %s in total" %(id,doc['info']['credit']  - credit))
    doc['info']['credit'] = credit
    doc['info']['effort'] = float(credit * k.res) / \
                                (doc['info']['capacity'] * k.cap )
    if doc['info']['effort'] > 1 : doc['info']['effort'] = 1
    store.call_db().update_document(id,doc)



if __name__ == "__main__":

    i = 0
    while i < 1000:
        controller()
        #print "CONTROLLED at time: " , time.time()
        time.sleep(set.SLEEP)
        db = store.call_db().get_db()
        print "\t -------------SLEEP:",i
        loggerCont.info("************** after controlled ************** ")
        for j in db:
            #print "\t", db[j]
            loggerCont.info("\t %s" %db[j])
        print "\t -------------SLEEP:",i
        i += 1
        loggerCont.info("************** ************** **************")