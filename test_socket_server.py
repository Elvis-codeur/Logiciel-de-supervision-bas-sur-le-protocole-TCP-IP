
import socketserver 

server = socketserver.TCPServer(("localhost",12800),RequestHandlerClass=(()))
