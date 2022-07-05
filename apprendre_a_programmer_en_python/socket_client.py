
import json
import socket, sys, threading

class ThreedReception(threading.Thread):
    '''L'objet thread gérant la réception des messages'''
    def __init__(self,conn,parent):
        self.parent = parent
        threading.Thread.__init__(self)
        self.connection = conn 


    def run(self):
        while 1:
            message_recu = self.connection.recv(1024).decode("utf-8")

            if(message_recu.startswith("r")):
                self.parent.send_message(self.parent.get_value_for_protocol())

            if(message_recu.startswith("s--")):
                # Le parent se fait set le value
                self.parent.set_value(
                    message_recu.strip("s--").strip("--s")
                )

            if not message_recu or  message_recu.upper() =="FIN":
                break 

        # Le threade <récption> se termine ici
        # On fonce la fermeture du thread <émission>

        self.parent.th_E.stop()
        print("Client arrêté. Connexion interrompue.")
        self.connection.close()

class TheadEmission(threading.Thread):
    """Objet thread gérant l'émission des messages"""
    def __init__(self,conn,parent):
        threading.Thread.__init__(self)
        self.parent = parent
        self.connexion = conn 
        self.message = ""
        self.send = False 
    def run(self):
        while 1:
            if(self.send):
                message_emis = self.message
                self.connexion.send(message_emis.encode("utf-8"))
                self.send = False

    def send_message(self,message):
        #print("oklm")
        self.send = True 
        self.message = message 




class SocketClient(threading.Thread):
    def __init__(self,ip_adress,port_number,label,type_,value):
        threading.Thread.__init__(self)
        self.ip_adress = ip_adress
        self.port_number = port_number
        self.label = label 
        self.type_ = type_
        self.value = value

        self.init()
    def init(self):

        # Programme principale - Etablissement de la connexion
        self.connexion = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            self.connect()

        except socket.error:
            print("La connexion a échoué")
            
        print("Connexion établie avec le serveur.")

        # Dialoge qvec le serveur : on lance deu threads pour géer
        # indépendamment l'émission et la réception des messages :

    def connect(self):
        self.connexion.connect((self.ip_adress,self.port_number))
        self.th_E = TheadEmission(self.connexion,self)
        self.th_R = ThreedReception(self.connexion,self)   
        self.th_E.start()
        self.th_R.start()
        
    def get_socket_info(self):
        
        return self.connexion.getsockname()


    def send_message(self,message):
        self.th_E.send_message(message)

    def set_value(self,data):
        self.value = data
        print("new-value-- {}".format(self.label),self.value)

    def get_value(self):
        return self.value

    def get_value_for_protocol(self):
        """Cette methode renvoie la valeur du client selon le protocole
        
        --v : Au commencement pour dire que la valeur va venir
        --b : Pour dire qu'on renvoie un boulean car on est dans le cas d'un capteur TOR
        --i : Pour dire qu'on renvoie un nombre entier
        --f : Pour dire qu'on renvoie un nombre flottant
        --s : Pour dire qu'on renvoie une chaîne de caractère"""
    
        if(self.type_ == "Coils" or self.type_ == "Discrete Inputs"):
            return "v--"+str(self.value)+"--b"

        elif (self.type_ =="Input Registers" or self.type_ == "Holding Registers"):
            return "v--"+str(self.value)+ "--int"

    def get_label(self):
        return self.label


