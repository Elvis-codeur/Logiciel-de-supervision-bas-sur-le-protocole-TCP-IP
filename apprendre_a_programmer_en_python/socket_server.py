# Définition d'un serveur réseaux gérant un système de CHAT simplifié
# Utilise les threads pour gérer les connexions clientes en parallèle 



from email import message
import json
import socket, sys, threading
import select



class ThreadClient(threading.Thread):
    
    def __init__(self,conn,conn_client):
        threading.Thread.__init__(self)
        self.connexion = conn 
        self.conn_client = conn_client

        self.send = False 
        self.message = ""
        
    def send_message(self,message):
        self.send = True 
        self.message = message

    def run(self):
        nom = self.getName()
        while 1:
            msgClient = self.connexion.recv(1024).decode("utf-8")
            if not msgClient or msgClient.upper() =="FIN":
                break 

            message  = {"destinataire":nom,"value":34}

            message = json.dumps(message)
           
            if self.send:
                self.connexion.send(message.encode("utf-8"))

        self.connexion.close()
        del self.conn_client[nom]

        print("Client %s déconnecté " % nom)



class SocketServer(threading.Thread):
    def __init__(self,host,port):
        self.host = host 
        self.port = port 
        threading.Thread.__init__(self)

        self.cont = True
        self.send = False 
        self.message = ""
        # C'est l'adresse du client qui va recevoir le message
        self.target = ()

        self.current_client_value = ""

        self.mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            self.mySocket.bind((self.host,self.port))
        except:
            print("La liason socket à l'adresse choisie a échoué")
            sys.exit()

        server_info = self.mySocket.getsockname()
        self.host = server_info[0]
        self.port = server_info[1]


        print("Serveur prêt, en attente de requêtes ... sur l'adresse ip {} et le port {}".format(self.host,self.port))
        self.mySocket.listen(5)

        self.conn_client = {}
        self.client_value = {}
        self.clients_connectes = []

    def run(self):
        while self.cont:
            #print("Elvis est un enfant de Dieu")
            connexions_demandees,wlist,rlist = select.select([self.mySocket],[],[],0.05)

            for connexion in connexions_demandees:
                connexion_avec_client, infos_connexion = connexion.accept()

                # Dictionnaire des clients. L'addresse sert de clé
                self.conn_client[infos_connexion] = connexion_avec_client
             

                # Liste des clients connecté
                self.clients_connectes.append(connexion_avec_client)

            clients_a_lire = []
            try:
                clients_a_lire, wlist, xlist = select.select(self.clients_connectes,[],[],0.05)
            except select.error:
                pass 
            else:
                for client in clients_a_lire:
                    msg_recu = client.recv(1024)

                    msg_recu = msg_recu.decode()
                    #print("Recu {}".format(msg_recu))
                    #client.send(b"5 / 5")
                    if msg_recu.startswith("v--"):
                        # On enlève l'avant et le trailing et on convertie en int 
                        self.current_client_value  = int(msg_recu.strip("v--").strip("--b"))

                    
                    

                    if msg_recu == "fin":
                        self.cont = False 
         
            if self.send:
                self.conn_client[self.target].send(self.message.encode("utf-8"))
                self.send = False

        print("Fermeture des connexions")
        for client in self.clients_connectes:
            client.close()

        self.mySocket.close()
        """
            connexion, adresse = self.mySocket.accept()
            # Créer un nouvel objet thread pour gérerla connexion
            th = ThreadClient(connexion,self.conn_client)
            th.start()
            # Mémoriser la connexion pour le dictionnaire
            it = th.getName()
            self.conn_client[adresse] = connexion 
            print(it,adresse)
            print("Client %s connecté, adresse IP %s port %s" % (it, adresse[0], adresse[1]))
            
            if self.s_data:
                keys = [self.conn_client.keys()]

                self.conn_client[keys[0]].send_message("Elvis")

                self.s_data = False

        """
                

    def close(self):
        self.cont = False

    def get_client_value(self,address):
        self.send_data("r",address)
        return self.current_client_value 

    def set_client_value(self,address,value):
        self.send_data("s--{}--s".format(value),address)

    def send_data(self,data,client_address):
        self.target = client_address
        self.message = data 
        self.send = True

    
        

