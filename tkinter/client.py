import socket 

import threading

from sympy import continued_fraction 

"""s
hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

connexion_avec_serveur.connect((hote,port))

print("Connexion établie avec le serveur sur le port {}".format(port))

msg_a_envoyer = b""

transaction_number = 0x0;
id_protocole =0x0000;
data_lenght = 0x0;
ini_id = 0x0;
code_function = 0x0;
data = "";


while msg_a_envoyer != b"fin":
    msg_a_envoyer = input(">")

    msg_a_envoyer = msg_a_envoyer.encode()

    connexion_avec_serveur.send(msg_a_envoyer)

    msg_recu = connexion_avec_serveur.recv(1024)

    print(msg_recu.decode())


print("Fermeture de la connexion")
connexion_avec_serveur.close()
"""
class SocketClient():
    def __init__(self,ip_adress,port_number) -> None:
        self.ip_adress = ip_adress
        self.port_number = port_number
        #self.thread = threading.Thread(group=None,target=self.run_client,name="Client Thread")

        self.message = ""
        self.send = False
    def init(self):
       self.run_client()

    def run_client(self):
        self.connexion_avec_serveur = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.connexion_avec_serveur.connect((self.ip_adress,self.port_number))
        print("Connexion établie avec le serveur sur le port {}".format(self.port_number))

    def send_message(self,message):
 
        message = self.message.encode()
        self.connexion_avec_serveur.send(message)
        msg_recu = self.connexion_avec_serveur.recv(1024)
        print(msg_recu.decode())
 
    def close(self):
        self.connexion_avec_serveur.close()

if __name__ == "__main__":
    a = SocketClient("localhost",int("15845"))
    a.init()
    a.send_message("Elvis est un enfant de Dieu")
    a.send_message("Elvis est un enfant de Dieu")
    a.close()