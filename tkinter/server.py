import socket
import select

"""
hote = ""
port = 12800

connexion_principale = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
connexion_principale.bind((hote,port))
connexion_principale.listen(5)

print("Le serveur écoute à présent sur le port  {}".format(port))


serveur_lance = True 
clients_connectes = []

while serveur_lance:

    connexions_demandees,wlist,xlist = select.select([connexion_principale],[],[],0.05)

    for connexion in connexions_demandees:
        connexion_avec_client,infos_connexion = connexion.accept()
        clients_connectes.append((connexion_avec_client,infos_connexion))

        print(infos_connexion)


    clients_a_lire = []
    try:
        clients_a_lire ,wlist,xlist = select.select([i[0] for i in clients_connectes],[],[],0.05)

    except select.error:
        pass 
    else:
        for client in clients_a_lire:
            msg_recu = client.recv(1024)

            msg_recu = msg_recu.decode()
            print("Recu {}".format(msg_recu))
            client.send(b"5 / 5")


            if msg_recu == "fin":
                serveur_lance = False 


print("Fermeture des connexions")
for client in clients_connectes:
    client.close()

connexion_principale.close()

"""
import threading

class Serveur():
    def __init__(self, ip_adress, port_number) -> None:
        self.ip_adress = ip_adress
        self.port_number = port_number
        self.tread = threading.Thread(group=None,target=self.run_server,name = "Server thread")

    def init(self):
        self.tread.start()

    def run_server(self):

        self.connexion_principale = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.connexion_principale.bind((self.ip_adress, self.port_number))
        self.connexion_principale.listen(5)

        print("Le serveur écoute à présent sur le port  {}".format(self.port_number))

        serveur_lance = True
        self.clients_connectes = []

        while serveur_lance:
            try:

                connexions_demandees, wlist, xlist = select.select(
                    [self.connexion_principale], [], [], 0.05)

                for connexion in connexions_demandees:
                    connexion_avec_client, infos_connexion = connexion.accept()
                    self.clients_connectes.append(
                    (connexion_avec_client, infos_connexion))

                    print(infos_connexion)

                clients_a_lire = []
                try:
                    clients_a_lire, wlist, xlist = select.select(
                    [i[0] for i in self.clients_connectes], [], [], 0.05)

                except select.error:
                    pass
                else:
                    for client in clients_a_lire:
                        msg_recu = client.recv(1024)

                        msg_recu = msg_recu.decode()
                        print("Recu {}".format(msg_recu))
                        client.send(b"5 / 5")

                        if msg_recu == "fin":
                            serveur_lance = False
            except Exception as e:
                print(e,"-----")
           

    def close(self):
        
        print("Fermeture des connexions")
        for client in self.clients_connectes:
            client.close()

        self.connexion_principale.close()


if __name__ == "__main__":
    a = Serveur("", 15845)
    a.init()
