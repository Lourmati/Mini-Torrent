#! /usr/bin/python3

#Mon serveur

import socket
import os
import sys
nomFichier = ""

#J'accepte 3 arguments
if len(sys.argv) != 3:
    print("Usage: ex1-clt.py <dossier> <port>", file=sys.stderr)
    sys.exit(1)

#Dans cette méthode, je recois le nom du fichier a telecharger
def recevoirNomFichier():
    port = int(sys.argv[2]) #Le port correspond au 3e argument
    # Petit serveur qui se contente de recevoir le nom du fichier
    socket_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_serveur.bind(("", port))
    socket_serveur.listen(5)
    print("Server listen")#Je print un message comme quoi le serveur écoute

    #J'accepte la connexion
    socket_client, address = socket_serveur.accept()
    print("Connection detected")#Connexion detectée
    nomFichier = socket_client.recv(4096).decode("UTF-8")#Je decode le message pour pouvoir le mettre dans ma variable nomFichier

    #Je crée mon chemin d'acces pour le fichier a telecharger, donc le 2e argument du programme + le nom du fichier que le serveur a recu
    chemin = sys.argv[1]+"/"+nomFichier
    present = os.path.isfile(chemin)#Retourne un boolean

    if present == true:#Si present est vrai, j'envoie comme quoi le serveur est pret
            socket_client.send(str.encode("Pret"))

            #Maintenant je vais utiliser 2 boucles, pour pouvoir telecharger mon fichier complet
            #Bloc par bloc, avec 2 boucles
            while True:#Si c'est vrai
                parcours = true#Boolean parcours initialisé a vrai

                while parcours:
                    offset = socket_client.recv(4096).decode("UTF-8")#Je recois le offset du moment

                    socket_client.send(str.encode("Offset recu"))#J'envoie comme quoi j'ai recu le offset
                    bloc = socket_client.recv(4096).decode("UTF-8")#Maintenant je recois le bloc a aller chercher dans le fichier

                    #J'ouvre le fichier en mode binaire, et j'utilise seek pour atteindre le offset
                    toDownload = open(chemin, 'rb')
                    toDownload.seek(int(offset))
                    blocInfo = toDownload.read(int(bloc))
                    socket_client.send(blocInfo)#J'envoie le bloc correspondant au client

                    parcours = false#Je remet la variable parcours a false

#main
recevoirNomFichier()
