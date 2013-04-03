
from SuperNode.conn import conn_run
from couchdatabase import  store
from couchdatabase import controller
import time
from SuperNode.log import log_config as log


loggerMain = log.logging.getLogger('Main')

def main():
        global loggerMain
        loggerMain.info("The application is starting")
        store.call_db()  ##create db
        time.sleep(1)
        conn_run.start() ##run the server
        #controller.start)##run controller for checking the credits

if __name__ == "__main__":
    main()
