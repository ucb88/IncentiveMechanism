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
        if tempDoc['info']['credit'] <= set.TOLERANT:
            leave.Leave(id, 11)
        else:
            check_credit(id,db[id])



def check_credit(id,doc):

    credit = doc['info']['credit']
    for key in doc['suppliedFrom'].keys():
        for i in range(len(doc['suppliedFrom'][key])):
            if time.time() - doc['suppliedFrom'][key][i]['timestamp'] >=  set.PERIOD:
                print ""
                doc['suppliedFrom'][key][i]['timestamp'] = time.time()
                trans_cost = doc['suppliedFrom'][key][i]['amount'] * k.dur

                store.call_db().update_credit(key,1*trans_cost,0) #type==0 , add/substract cerdit
                credit -= trans_cost

    store.call_db().update_credit(id, credit, 1)  #type==1 set new credit

def start():
    i = 0
    while i < True:
        controller()
        print "CONTROLLED at time: " , time.time()
        time.sleep(set.SLEEP)
        i+=1

if __name__ == "__main__":
    i = 0
    while i < 1000:
        controller()
        print "CONTROLLED at time: " , time.time()
        time.sleep(set.SLEEP)
        db = store.call_db().get_db()
        print "\t -------------SLEEP:",i
        for j in db:
            print "\t", db[j]
        print "\t -------------SLEEP:",i
        i += 1