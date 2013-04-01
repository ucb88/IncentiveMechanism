from SuperNode.couchdatabase import store
import logging

loggerLev = logging.getLogger('Leave')


def Leave(ON_IP,ON_PORT):

    global loggerLev
    loggerLev.info("The node:%s is leaving all resources" %ON_IP)

    tempDoc = store.call_db().get_document(ON_IP)
    for id in tempDoc['suppliedFrom'].keys():
        tempSupplierDoc = store.call_db().get_document(id)
        tempSupplierDoc = regain(ON_IP,tempSupplierDoc)
        tempDoc = reallocate(id,tempDoc)
        store.call_db().update_document(id, tempSupplierDoc)
        store.call_db().update_document(ON_IP, tempDoc)

    return "ALL occupied resources are left"

def regain(allocaterId, tempSupplierDoc):

    global loggerLev

    allocated = tempSupplierDoc['providedTo'][allocaterId]
    tempSupplierDoc['info']['avail'] += allocated
    loggerLev.info("The node:%s got its resources:%s back from %s" %(tempSupplierDoc['_id'],allocated,allocaterId))
    del tempSupplierDoc['providedTo'][allocaterId]
    return tempSupplierDoc


def reallocate(providerId,tempDoc):

    provided = tempDoc['suppliedFrom'][providerId]
    del tempDoc['suppliedFrom'][providerId]
    loggerLev.info("The node:%s left the resources back to %s" %(tempDoc['_id'],providerId))
    return tempDoc


if __name__ == "__main__":

    print Leave('111', '1')
    print Leave('222', '1')