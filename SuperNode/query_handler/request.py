import math
import time
from SuperNode.couchdatabase import store
from SuperNode.couchdatabase.views import generate_views as view
import coefficients as k
import logging
import threading

sem = threading.Semaphore(value=1)
loggerReq = logging.getLogger('Request')

def Request(ON_IP, ON_PORT, amount, duration):

    global  loggerReq

    print "ON_IP", ON_IP, \
        "ON_PORT", ON_PORT, \
        "amount", amount, \
        "duration", duration

    doc = store.call_db().get_document(ON_IP)
    totalAvailResInTheSystem = view.total_availablity()
    rmax = math.ceil(doc['info']['effort'] * totalAvailResInTheSystem)   #max number of resource that a node can request

    loggerReq.info("The Node:%s asks for %s amount of resource, its RMAX:%s"%(ON_IP,amount,rmax))

    if(rmax >= amount):
        if((totalAvailResInTheSystem-doc['info']['avail']) >= amount):
            return decision(doc, amount, duration)
        else:
            loggerReq.warning("There is not enough resource:%s to meet your:%s request:%s" %(totalAvailResInTheSystem,ON_IP ,amount))
            return "There is not enough resource to meet your request."
    else:
        loggerReq.warning("The Node:%s has less RMAX:%s to get %s amount resources" %(ON_IP,rmax,amount))
        return "You don't have enough credit for requesting that amount of resource"


def decision(doc, amount, duration):

    global sem
    sem.acquire()

    global loggerReq
    isFullySupplied = 0
    requestor_id = doc['_id']
    provider_list = view.sorted_list()

    for n in provider_list:
        provider_id = n.keys()[0]

        if provider_id == requestor_id :
            pass
        else:
            supplierDoc = store.call_db().get_document(provider_id)
            res = supplierDoc['info']['avail']
            if res <= 0:
                continue

            tempDoc = doc
            tempSupplierDoc = supplierDoc

            if res >= amount:
                res = res - amount
                tempSharedAmount = amount
                isFullySupplied = 1
            else:
                amount = amount - res
                tempSharedAmount = res


            trans_cost = tempSharedAmount * k.res # coeff_res
            tempDoc = requestor(provider_id, trans_cost, tempSharedAmount, tempDoc)
            tempSupplierDoc = supplier(requestor_id, trans_cost, tempSharedAmount, tempSupplierDoc)
            store.call_db().update_document(requestor_id, tempDoc)
            store.call_db().update_document(provider_id, tempSupplierDoc)

            loggerReq.info("The node:%s supplied %s amount resource to %s" %(provider_id,amount,requestor_id))

        if isFullySupplied == 1:
            break

    sem.release()
    return "REQUESTED"


def requestor(provider_id, trans_cost, amount, tempDoc):
    global loggerReq

    if not (tempDoc['suppliedFrom'].has_key(provider_id)):
        tempDoc['suppliedFrom'][provider_id] = []
    else:
        pass

    tempDoc['suppliedFrom'][provider_id].append({'amount':amount, 'timestamp':time.time()})
    tempDoc['info']['credit'] -= trans_cost
    tempDoc['info']['effort'] = float(tempDoc['info']['credit'] * k.res) / \
                                (tempDoc['info']['capacity'] * k.cap)
    if tempDoc['info']['effort'] > 1 : tempDoc['info']['effort'] = 1
    loggerReq.info("The node: %s is charged %s from the node:%s" %(tempDoc['_id'],trans_cost, provider_id))

    return tempDoc


def supplier(requestor_id, trans_cost, amount, tempSupplierDoc ):
    global  loggerReq

    if tempSupplierDoc['providedTo'].has_key(requestor_id):
        tempSupplierDoc['providedTo'][requestor_id] += amount
    else:
        tempSupplierDoc['providedTo'][requestor_id] = amount

    tempSupplierDoc['info']['avail'] -= amount
    tempSupplierDoc['info']['credit'] += trans_cost
    tempSupplierDoc['info']['effort'] = float(tempSupplierDoc['info']['credit'] * k.res) / \
                                        (tempSupplierDoc['info']['capacity'] * k.cap )
    if tempSupplierDoc['info']['effort'] > 1 : tempSupplierDoc['info']['effort'] = 1

    loggerReq.info("The node:%s is gained %s credit from node:%s" %(tempSupplierDoc['_id'],trans_cost,requestor_id))
    return tempSupplierDoc


if __name__ == "__main__":
    print Request('222', '1', 10, 1)
    #print Request('111', '1', 5, 1)