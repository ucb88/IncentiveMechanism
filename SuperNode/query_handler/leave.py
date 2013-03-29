from SuperNode.couchdatabase import store

def Leave(ON_IP,ON_PORT):

    tempDoc = store.call_db().get_document(ON_IP)
    for id in tempDoc['suppliedFrom'].keys():
        tempSupplierDoc = store.call_db().get_document(id)
        tempSupplierDoc = regain(ON_IP,tempSupplierDoc)
        tempDoc = reallocate(id,tempDoc)
        store.call_db().update_document(id, tempSupplierDoc)
        store.call_db().update_document(ON_IP, tempDoc)



def regain(allocaterId, tempSupplierDoc):

    allocated = tempSupplierDoc['providedTo'][allocaterId]
    tempSupplierDoc['info']['avail'] += allocated
    del tempSupplierDoc['providedTo'][allocaterId]
    return tempSupplierDoc


def reallocate(providerId,tempDoc):

    provided = tempDoc['suppliedFrom'][providerId]
    del tempDoc['suppliedFrom'][providerId]
    return tempDoc


if __name__ == "__main__":

    print Leave('111', '1')
    print Leave('222', '1')