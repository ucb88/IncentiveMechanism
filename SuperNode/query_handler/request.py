from SuperNode.couchdatabase import store
from SuperNode.couchdatabase.views import generate_views as view

coeff_res = 1

def Request(ON_IP,ON_PORT,amount, duration):
    print "ON_IP",ON_IP, \
        "ON_PORT", ON_PORT, \
        "amount", amount, \
        "duration", duration

    doc = store.call_db().get_document(ON_IP)
    totalAvailResInTheSystem = view.total_availablity()

    print doc['info']['credit'], amount, doc['info']['credit'] >= amount, totalAvailResInTheSystem

    if(doc['info']['credit'] >= amount):
        if(totalAvailResInTheSystem >= amount):
            decision(doc, amount, duration)
        else:
            return "There is not enough resource to meet your request."
    else :
        return "You don't have enough credit for requesting that amount of resource"



def decision(doc, amount, duration) :
    global coeff_res
    isFullySupplied = 0
    requestor_id = doc['_id']
    provider_list = view.sorted_list()

    for n in provider_list:
        provider_id = n.keys()[0]
        if provider_id == requestor_id or isFullySupplied==1:
            pass
        else:
            supplierDoc = store.call_db().get_document(provider_id)
            res = supplierDoc['info']['avail']
            if res <= 0 :
                continue

            tempDoc = doc
            tempSupplierDoc = supplierDoc
            trans_cost = 0
            tempSharedAmount = 0
            print "RES:",res, " AMOUNT:",amount

            if res > amount:
                res = res - amount
                tempSharedAmount = amount
                isFullySupplied = 1
            else :
                print "DAHA VARRR"
                amount = amount - res
                tempSharedAmount = res

            trans_cost = tempSharedAmount * coeff_res # coeff_res
            print "TRANSCOST:",trans_cost

            tempDoc = requestor(provider_id,trans_cost,tempSharedAmount,tempDoc)
            tempSupplierDoc = supplier(requestor_id,trans_cost,tempSharedAmount,tempSupplierDoc )
            store.call_db().update_document(requestor_id, tempDoc)
            store.call_db().update_document(provider_id, tempSupplierDoc)

    return "REQUESTED"


def requestor(provider_id,trans_cost,amount, tempDoc):

    if tempDoc['suppliedFrom'].has_key(provider_id) :
        tempDoc['suppliedFrom'][provider_id] += amount
    else :
        tempDoc['suppliedFrom'][provider_id] = amount

    #print "\t requestor charging now  ",  tempDoc['info']['credit'], trans_cost
    tempDoc['info']['credit'] -= trans_cost
    return tempDoc

def  supplier(requestor_id,trans_cost,amount,tempSupplierDoc ):

    if tempSupplierDoc['providedTo'].has_key(requestor_id) :
        tempSupplierDoc['providedTo'][requestor_id] += amount
    else :
        tempSupplierDoc['providedTo'][requestor_id] = amount

    tempSupplierDoc['info']['avail'] -= amount
    tempSupplierDoc['info']['credit'] += trans_cost
    return tempSupplierDoc


if __name__ == "__main__":

    print Request('111', '1', 10, 1)
    print Request('222', '1', 5, 1)