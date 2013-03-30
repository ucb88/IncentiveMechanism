import sys
from SuperNode.conn import conn_run
from couchdatabase import  store

def main():
        store.call_db()  ##create db

        conn_run.start() ##run the server

if __name__ == "__main__":
    main()