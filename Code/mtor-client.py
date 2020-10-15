#! /usr/bin/python3

#Je sais que mon programme ne fonctionne pas tout a fait correctement, il fait geler
#toute la machine, J'ai longuement cherche, mais je n'ai pas reussi a trouver la cause
#du probleme. Je crois que mon TP semble assez cohérent malgré se bug.

import socket  # Import socket module
import sys
import os
from threading import Thread,Lock

listeTailleBloc = []
verrou = Lock()

#Mon programme n'accepte que 3 arguments, le programme, le dossier et le port
if len(sys.argv) != 3:
    print("Usage: ex1-clt.py <nom du fichier> <port>", file=sys.stderr)
    sys.exit(1)

#Methode pour diviser la taille du fichier que je veux télécharger
def diviserTailleFichier(taille, listeAdresse):
    offset = 0 #Offset que je vais utiliser par la suite
    global listeTailleBloc #Ma listeTailleBloc qui est global
    #Diviser en 4 blocs par thread
    tailleBloc = taille/len(listeAdresse)/4 #Je divise par 3, et par 4 ensuite
    tailleBloc = round(tailleBloc)#Arrondir

    compteur = 0#Initialiser mon compteur
    while compteur != len(listeAdresse*4):
        listeTailleBloc.append((tailleBloc, offset))#J'ajoute mon tailleBloc et mon offset a ma liste de bloc
        offset = offset + tailleBloc#Je dois modifier le offset a chaque itération, pour que le offset se rende au bon endroit


#Methode pour le socket, j'envoie le nom de fichier, j'envoie des messages et je recois l'information nécessaire pour la suite
def socket_fichier(adresse, nomFichier):#jai besoin de l'adresse et du nom de fichier
    #Je vais utiliser ma liste de bloc global, et le verrou qui est global aussi
    global verrou
    global listeTailleBloc

    #Initialiser socket
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(nomFichier)
    #Liste adresse[0] correspond a la premiere adresse ip, et sys.argv[2] le port
    socket_client.connect((adresse, int(sys.argv[2])))
    socket_client.send(str.encode(nomFichier))#J'envoie le nom de fichier

    message = socket_client.recv(4096).decode("UTF-8")#Je recois le message du serveur

    if message == "Pret":#Si le message correspond a pret, ca veut dire que la connexion a fonctionne

        while (len(listeTailleBloc)!=0): #Tant que ma taille de la liste n'est pas a 0, je continue le transfert
            temp = listeTailleBloc.pop(0)#Temp va stocker le premier element de listeTailleBloc
            bloc = temp[0]#Le temp[0] a stocker dans la variable bloc (pour un bloc)
            offset = temp[1]#Le temp[1] a stocker dans la variable offset, pour le modifier a chaque fois
            socket_client.send(str.encode(offset))#J'envoie le offset au serveur

            #Je recois encore un message si le offset a bien été recu par le serveur
            message = socket_client.recv(4096).decode("UTF-8")
            if message == "Offset recu":#SI le offset a ete recu, je peux continuer
                socket_client.send(str.encode(bloc))#J'envoie le bloc a telecharger

            blocInfo = socket_client.recv(bloc)#Je stocke ce que je recois du serveur (le bloc) dans blocInfo

            #J'ouvre le tout en mode binaire
            toDownload = open(nomFichier, 'rb+')
            toDownload.seek(int(offset))#Seek jusqu'au offset, ne pas oublier de cast le offset en int
            toDownload.write(blocInfo)#Ecrire dans le blocInfo
            toDownload.close()#Fermer le fichier

#Le main, j'ouvre le fichier mtr pour pouvoir stocker chaque ligne dans des variables
def main():

    listeAdresse = []#Liste d'adresse pour contenir les différentes adresse IP
    nomFichier = ""#Variable pour stocker le nom du fichier
    compteur = 0#Compteur que j'utiliserai pour la lecture du mtr
    file = open(sys.argv[1], 'r')#J'ouvre

    for i in file:

        line = i.strip()#Je strip la ligne pour enlever les espaces vides

        if compteur == 0:#Si le compteur est a 0, je stocke la ligne dans le nom du fichier
            nomFichier = line
        elif compteur == 1:#Si le compteur est a 0, je stocke la ligne dans la variable taille
            taille = int(line)
        else:
            listeAdresse.append(line)#Le reste, je l'ajoute dans ma liste d'adresse ip
        compteur = compteur+1#A chaque iteration, j'implemente le compteur

    diviserTailleFichier(taille, listeAdresse)#Je fait la division pour ma listeTailleBLoc

    #J'ouvre en mode binaire des le debut, tel que mentionné dans l'enonce de tp
    fichier = open(nomFichier, 'wb') #Ouverture du fichier avec wb
    fichier.seek(taille_fichier-1)
    fichier.write(b'\0')
    fichier.close() #Fermeture du fichier

    listThread = []#Je crée une liste de thread
    for adresse in listeAdresse:#Je fait appel a ma methode socket_fichier
        listThread.append(Thread(target = socket_fichier, args = (adresse,nomFichier)))#J'appel ma méthode avec le socket a chaque iteration de ma boucle for
    for thread in listThread:
        thread.start()
        thread.join()

#main
main()
