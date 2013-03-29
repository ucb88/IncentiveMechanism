import SimpleXMLRPCServer
import  conn_dispatcher as dis
import conn_settings as conn


def start():
    # A simple server with simple arithmetic functions
    server = SimpleXMLRPCServer.SimpleXMLRPCServer((conn.SN_IP,conn.SN_PORT), dis.LoggingSimpleXMLRPCRequestHandler, allow_none=True)
    print "Listening on port %s..." % (conn.SN_PORT)
    server.register_instance(dis.Queries())
    server.serve_forever()