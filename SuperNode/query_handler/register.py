from SuperNode.couchdatabase import store

def Register(ON_IP,ON_PORT,capacity,resource):
    print "ON_IP",ON_IP, \
        "ON_PORT", ON_PORT, \
        "capacity", capacity, \
        "resource", resource

    json_doc = {
                "_id" : ON_IP,
                "info" : {
                    "capacity": capacity, \
                    "resource" : resource, \
                    "avail" : resource, \
                    "credit" : resource, \
                },
                "providedTo" : {},
                "suppliedFrom" : {}
        }

    store.call_db().store_document(json_doc)

    ## TODO : record sliver info ##

    return "REGISTERED"