import SimpleXMLRPCServer
import  conn_dispatcher as dis
import conn_settings as conn
from SuperNode.log import log_config as log


loggerConn = log.logging.getLogger('Connection')

def start():

    global  loggerConn
   # loggerConn.info("Listening on port %s..." %(conn.SN_PORT))
    server = SimpleXMLRPCServer.SimpleXMLRPCServer((conn.SN_IP,conn.SN_PORT), dis.LoggingSimpleXMLRPCRequestHandler, allow_none=True)
    print "Listening on port %s..." % (conn.SN_PORT)
    server.register_instance(dis.Queries())
    server.serve_forever()