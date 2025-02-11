from twitter.account import Account
from twitter.scraper import Scraper
import os
import json
import random
import time



email, username, pwd = "stormshop83@gmail.com", "DailyClubPorn", "Aeroz@2806!83?"
account = Account(email, username, pwd)
scraper = Scraper(email, username, pwd)

ids = []
PornClubDaily = 1145115635283910656 
id2 = 1690093798360055808
id3 = 1667367932647854080
ids.append(PornClubDaily)
ids.append(id2)
ids.append(id3)

# Chemin du dossier contenant les fichiers
def trouver_premiere_occurence_entry_id(dossier):
    # Liste des fichiers dans le dossier
    fichiers = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
    
    if not fichiers:
        print("Aucun fichier trouvé dans le dossier.")
        return None

    # Chemin du premier fichier
    premier_fichier = os.path.join(dossier, fichiers[random.randint(0, len(fichiers)-1)])
    
    try:
        # Ouvre et lit le contenu du fichier
        with open(premier_fichier, 'r', encoding='utf-8') as fichier:
            contenu = json.load(fichier)
        
        # Recherche de la première occurrence de entry_id
        return rechercher_entry_id(contenu)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier: {e}")
        return None
    
def rechercher_entry_id(contenu):
    entry_ids = []
    if isinstance(contenu, dict):
        for key, value in contenu.items():
            if key == 'entryId':
                entry_ids.append(value.split("-")[1])
            elif isinstance(value, (dict, list)):
                entry_ids.extend(rechercher_entry_id(value))
    elif isinstance(contenu, list):
        for item in contenu:
            entry_ids.extend(rechercher_entry_id(item))

    for elt in entry_ids:
        if not str(elt).startswith('1'):
            entry_ids.remove(elt)
    
    return entry_ids

def rechercher_rest_id(contenu):
    rest_ids = []
    if isinstance(contenu, dict):
        for key, value in contenu.items():
            if key == 'rest_id':
                rest_ids.append(value)
            elif isinstance(value, (dict, list)):
                rest_ids.extend(rechercher_rest_id(value))
    elif isinstance(contenu, list):
        for item in contenu:
            rest_ids.extend(rechercher_rest_id(item))

    for elt in rest_ids:
        if not str(elt).startswith('1'):
            rest_ids.remove(elt)
    
    return rest_ids

def obtenir_nom_premier_fichier(dossier):
    try:
        fichiers = os.listdir(dossier)
        if fichiers:
            return fichiers[0]
        else:
            print("Aucun fichier trouvé dans le dossier.")
            return None
    except FileNotFoundError:
        print(f"Le dossier {dossier} n'existe pas.")
        return None

def nom_dossier(dossier):
    elements = os.listdir(dossier)

    # Filtrer les dossiers
    dossiers = [element for element in elements if os.path.isdir(os.path.join(dossier, element))]

    # Imprimer les noms des dossiers
    for dossier in dossiers:
        print(dossier)
    
    return dossier

def supprimer_fichiers(dossier, id):

    chemin = f"{dossier}/{id}"

    if len(os.listdir(chemin)) <= 15:
        print("Aucun fichier à supprimer")
        return

    for i in range (len(os.listdir(chemin)) - 15):
        alea = random.randint(0, len(os.listdir(chemin)) - 1)
        try:
            os.remove(f"{chemin}/{os.listdir(chemin)[alea]}")
        except:
            print("Erreur de suppression")
            return supprimer_fichiers(dossier, id)
        
def poster_tweet(ids, anctweet):

    for id in ids:

        if len(anctweet) >= len(ids):
            return
    
        if str(id) not in nom_dossier('data'):
            scraper.tweets([id])
        else:
            print("Dossier déjà téléchagé")

        dossier = "data/"+str(id)

        try:
            liste_entry_id = trouver_premiere_occurence_entry_id(dossier)
            entry_id = liste_entry_id[random.randint(0, len(liste_entry_id)-1)]
        except:
            print("Tweet sans vidéo ou erreur dans le dossier")
            return poster_tweet(ids, anctweet)

        print(liste_entry_id)
        
        l= []
        idtxt = open("ids.txt", "r")
        l.append(idtxt.read())
        print(idtxt.read())
        idtxt.close()
        
        liste_id = []
        nbId = l[0].count(" ")
        for i in range(nbId):
            liste_id.append(l[0].split(" ")[i+1])

        if entry_id not in liste_id:
            idtxt = open("ids.txt", "a")
            idtxt.write(f" {str(entry_id)}")
            idtxt.close()
        else:
            return poster_tweet(ids, anctweet)
    
        print("")
        print(entry_id)

        if entry_id:
            print(f"Occurence trouvée")
        else:
            print("Aucune occurrence de 'entry_id' trouvée.")

        if entry_id not in anctweet:
            scraper.download_media([entry_id])
            try:
                like = account.tweet('Visit my shop on discord : discord.gg/dealabs', media=[
                {'media': 'media/'+obtenir_nom_premier_fichier("media"), 'alt': '', 'tagged_users': []}
                ])
            except:
                print("Aucun fichier dans le dossier")
                return poster_tweet(ids, anctweet)
            
            print("Vidéo postée")

            liste_rest_id_mon_post = rechercher_rest_id(like)
            print("liste rest_id de mon post : ", liste_rest_id_mon_post)
            account.like(liste_rest_id_mon_post[0])

            if (len(anctweet)<len(ids)):
                anctweet.append(entry_id)
                

            os.remove('media/'+obtenir_nom_premier_fichier("media"))
        else:
            print("Aucun nouveau tweet")

        supprimer_fichiers("data", id)

    supprimer_fichiers("data", "batch")

while True:
    ancien_tweet = []
    poster_tweet(ids, ancien_tweet) 
    time.sleep(random.randint(36000, 50400))
