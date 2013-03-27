import couchdb
import settings as set

db = None

class Database:

    def __init__(self, name = set.DB_NAME):
        couch = couchdb.Server(set.DB_SERVER_IP+':'+set.DB_SERVER_PORT)

        try:
            db = couch.create(name)
        except:
            db = couch[name]

        self.db = db

    def store_document (self, doc):
        self.db.save(doc)

    def update_document(self, doc_id, updatedDoc):
        self.db[doc_id] = updatedDoc

    def delete_document(self, doc_id):
        del self.db[doc_id]

    def get_document(self, doc_id):
        return self.db[doc_id]

    def is_exist (self, doc_id):
        return self.db.__contains__(doc_id)

    def update_credit(self, doc_id, newCredit) :
        if self.is_exist(doc_id):
            if self.db[doc_id].has_key('credit'):
                tempdoc = self.get_document(doc_id)
                tempdoc['credit'] = newCredit
            else :
                print "There is no credit key in the client doc"
                print "Client doc should be proper"
        else:
            print "non-exist document"

        self.update_document(doc_id, tempdoc)
    #def updateEffort ..
    #

    def get_db(self):
        return self.db

    def delete_gb(self):
        del self.db

    def print_db(self):
        print "------- DB -----------"
        for doc in self.db:
            print self.db[doc]
        print "\n"


def create_database():
    db = Database()
    return db


if __name__ == "__main__":
    myDB = create_database()
    myDB.store_document({'_id':'first', 'credit':34, 'capacity':100})
    myDB.store_document({'_id':'second', 'credit':14, 'capacity':120})
    myDB.store_document({'_id':'third', 'credit':4, 'capacity':130})
    myDB.print_db()

    doc = myDB.get_document('third')
    doc['capacity'] = 1155
    myDB.update_document('third', doc)
    myDB.print_db()

    myDB.update_credit('first',14567)
    myDB.print_db()

