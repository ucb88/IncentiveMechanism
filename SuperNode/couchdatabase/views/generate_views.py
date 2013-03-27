from SuperNode.couchdatabase import store

## views are in memory, not in couchdb,,
## if they are gonna be in db, use design :

def sorted_list():
    map_func_for_sorted = """function(doc) { \
                                if(doc.credit > 0) \
                                    emit(doc.credit, doc._id); \
                    }"""

    sort_results = store.create_database().get_db().query(map_func_for_sorted)
    sorted_list =  {}
    for row in sort_results:
        sorted_list[row.key] = row.value

    return sorted_list

def total_availablity():

    map_func_for_avail = """function(doc) { \
                                if(doc.capacity) \
                                  emit(doc._id, doc.capacity); \
                    }"""

    avail_results = store.create_database().get_db().query(map_func_for_avail)
    avail_total = 0
    for row in avail_results:
        avail_total += row.value

    return avail_total


if __name__ == "__main__":
    list = sorted_list()
    for i in list:
        print list[i]

    print "total avail:", total_availablity()