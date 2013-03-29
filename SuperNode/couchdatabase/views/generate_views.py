from SuperNode.couchdatabase import store

## views are in memory, not in couchdb,,
## if they are gonna be in db, use design :

def sorted_list():
    map_func_for_sorted = """function(doc) { \
                                if(doc['info'].credit > 0) \
                                    emit(doc['info'].credit, doc._id); \
                    }"""

    sort_results = store.call_db().get_db().query(map_func_for_sorted)
    sorted_list =  []

    ## key-value is exchange to make the works easier. for performance should be same!
    for row in sort_results:
        sorted_list.append({row.value:row.key})

    return sorted_list

def total_availablity():

    map_func_for_avail = """function(doc) { \
                                if(doc['info'].capacity) \
                                  emit(doc._id, doc['info'].avail); \
                    }"""

    avail_results = store.call_db().get_db().query(map_func_for_avail)
    avail_total = 0
    for row in avail_results:
        avail_total += row.value

    return avail_total


if __name__ == "__main__":
    list = sorted_list()
    for i in list:
        print i

    print "total avail:", total_availablity()