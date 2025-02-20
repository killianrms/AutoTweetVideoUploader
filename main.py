from twitter.account import Account
from twitter.scraper import Scraper
import os
import json
import random
import time



email, username, pwd = "ton_mail", "ton_pseudo", "ton_mdp"

global account, scraper, chosen_videos_data, countTryTweet
countTryTweet = 0
#liste des comptes à scraper
ids = []
id1 = id_de_compte_1
id2 = id_de_compte_2
id3 = id_de_compte_3

ids.append(id1)
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


def poster_tweet():
    global countTryTweet
    if chosen_videos_data is []:
        print("Aucune vidéo à poster.")
        return
    else :
        all_failed = True
        for data in chosen_videos_data:
            print("creation du tweet pour le compte: ", data['account_id'])
            account_id = data['account_id']
            chosen_videos = data['chosen_videos']

            for idVideo in chosen_videos:
                with open(f"data/{account_id}/uploaded.json", 'r') as dataUploaded:
                    if os.path.getsize(f"data/{account_id}/uploaded.json") > 0:
                        uploaded = json.load(dataUploaded)
                    else:
                        uploaded = {}
                dataUploaded.close()

                if f'{account_id}' not in uploaded:
                    print("ajout de l'account_id dans le fichier uploaded.json")
                    uploaded[account_id] = []
                    with open(f"data/{account_id}/uploaded.json", 'w') as fichier:
                        json.dump(uploaded, fichier)
                    fichier.close()


                if idVideo in uploaded.get(account_id, []):
                    print(f"Video ID {idVideo} already in uploaded list for account {account_id}")
                    continue
                else:
                    print(f"Video ID {idVideo} not in uploaded list for account {account_id}")
                video = None
                try:
                    download = scraper.download_media([idVideo])
                    if download :
                        for video in os.listdir("media"):
                            video = video
                            os.rename(f"media/{video}", f"data/{data['account_id']}/media/{video}")
                        tweet = None
                        msg = '@DailyClubPorn'
                        if len(os.listdir(f"data/{account_id}/media")) > 1:
                            media = []
                            for video in os.listdir(f"data/{account_id}/media"):
                                media.append({'media': f"data/{account_id}/media/{video}", 'alt': '', 'tagged_users': []})
                            tweet = account.tweet(msg, media=media)
                        else:
                            tweet = account.tweet(msg, media=[{'media': f"data/{account_id}/media/{os.listdir(f'data/{account_id}/media')[0]}", 'alt': '', 'tagged_users': []}])
                        all_failed = False

                        print(f"Tweet publié pour le fichier {video} du compte {account_id}")
                        print(f"Tweet: {tweet}")

                        addTweetFileToUploaded(account_id, idVideo)
                        removeTweetFileById(account_id, idVideo)
                        removeVideoInMediaFolder(account_id)
                        removeBatchFolder()
                    else :
                        print("Le telechargement de la video n'a pas aboutie")
                except Exception as e:
                    if not video:
                        video = "\'Aucune vidéo\'"
                    removeTweetFileFromUploaded(account_id, idVideo)
                    print(f"Erreur lors de la publication du tweet: {e}, pour la video {video} du compte {account_id}")

        if countTryTweet > 6 and all_failed:
            print("Tous les tweets ont échoué")
            countTryTweet = 0
            return

        if all_failed:
            countTryTweet += 1
            print(f"Essai numéro {countTryTweet}")
            choose3videosToUpload()
            poster_tweet()

def removeTweetFileFromUploaded(accountId, id):
    try:
        with open(f"data/{accountId}/uploaded.json", 'r') as fichier:
            uploaded = json.load(fichier)
        fichier.close()

        print(f"uploaded: {uploaded}")

        if f'{accountId}' not in uploaded:
            print("ajout de l'account_id dans le fichier uploaded.json depuis la fonction removeTweetFileFromUploaded")
            uploaded[accountId] = []

        print(uploaded.get(accountId, []))

        if id in uploaded.get(accountId, []):
            uploaded[f'{accountId}'].remove(id)

        print(f"uploaded: {uploaded}")

        with open(f"data/{accountId}/uploaded.json", 'w') as fichier:
            json.dump(uploaded, fichier)
        print(f"Le fichier {id}.json a été retiré de la liste des fichiers uploadés.")
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier de la liste des fichiers uploadés: {e}")
        return removeTweetFileFromUploaded(accountId, id)


def addTweetFileToUploaded(accountId, id):
    try:
        with open(f"data/{accountId}/uploaded.json", 'r') as fichier:
            uploaded = json.load(fichier)
        fichier.close()

        print(f"uploaded: {uploaded}")

        if f'{accountId}' not in uploaded:
            print("ajout de l'account_id dans le fichier uploaded.json depuis la fonction addTweetFileToUploaded")
            uploaded[accountId] = []

        print(uploaded.get(accountId, []))

        if id not in uploaded.get(accountId, []):
            uploaded[f'{accountId}'].append(id)

        print(f"uploaded: {uploaded}")

        with open(f"data/{accountId}/uploaded.json", 'w') as fichier:
            json.dump(uploaded, fichier)
        print(f"Le fichier {id}.json a été ajouté à la liste des fichiers uploadés.")
    except Exception as e:
        print(f"Erreur lors de l'ajout du fichier à la liste des fichiers uploadés: {e}")
        return addTweetFileToUploaded(accountId, id)

def removeTweetFileById(accountId,id):
    try:
        os.remove(f"data/{accountId}/tweet/{id}.json")
        print(f"Le fichier {id}.json a été supprimé.")
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier: {e}")
        return removeTweetFileById(id)

def removeVideoInMediaFolder(accountId):
    try:
        for video in os.listdir(f"data/{accountId}/media"):
            os.remove(f"data/{accountId}/media/{video}")
            print(f"La vidéo {video} a été supprimée.")
        os.remove(f"media.json")
        print(f"Les vidéos ont été supprimées.")
    except Exception as e:
        print(f"Erreur lors de la suppression des vidéos: {e}")
        return removeVideoInMediaFolder(accountId)

def removeBatchFolder():
    try:
        for file in os.listdir("data/batch"):
            os.remove(f"data/batch/{file}")
    except Exception as e:
        print(f"Erreur lors de la suppression du dossier: {e}")
        return removeBatchFolder()


def initFolder(ids):
    if not os.path.exists("data"):
        os.makedirs("data")
        print(f"Le dossier data a été créé.")
        for id in ids:
            if not os.path.exists(f"data/{id}"):
                os.makedirs(f"data/{id}")
                print(f"Le dossier data/{id} a été créé.")
            if not os.path.exists(f"data/{id}" + "/media"):
                os.makedirs(f"data/{id}" + "/media")
                print(f"Le dossier media a été créé.")
            if not os.path.exists(f"data/{id}" + "/tweet"):
                os.makedirs(f"data/{id}" + "/tweet")
                print(f"Le dossier tweet a été créé.")
            if not os.path.exists(f"data/{id}" + "/data"):
                os.makedirs(f"data/{id}" + "/data")
                print(f"Le dossier data a été créé.")
            if not os.path.exists(f"data/{id}" + "uploaded.json"):
                with open(f"data/{id}" + "/uploaded.json", 'w') as fichier:
                    json.dump({}, fichier)
                print(f"Le fichier uploaded.json a été créé.")
    else:
        print(f"Le dossier data existe déjà.")


def initConnectionAccount():
    global account, scraper
    try:
        account = Account(email, username, pwd)
        scraper = Scraper(email, username, pwd)
    except Exception as e:
        print(f"Erreur lors de la connexion: {e}")
        return initConnectionAccount()
    print("Connexion réussie")


def scraperVideos(ids):
    for id in ids:
        list_tweet = []
        scraper.tweets([id], limit=400)
        print("Scrapping des tweets du compte terminé")
        dossier = f"data/{id}"
        fichiers = [f for f in os.listdir(dossier) if f.endswith('.json')]

        if "uploaded.json" in fichiers:
            fichiers.remove("uploaded.json")

        for i in range(len(fichiers)):
            try:
                os.rename(f"{dossier}/{fichiers[i]}", f"{dossier}/data/{fichiers[i]}")
            except:
                print("Erreur lors du déplacement des fichiers")
                return scraperVideos(ids)
        print(f"Scrapping des vidéos du compte {id} terminé")



def choose3videosToUpload():
    global chosen_videos_data
    chosen_videos_data = []
    videosChoosed = []

    for id in ids:
        dossier = f"data/{id}/tweet"
        if os.listdir(dossier):
            fichiers = [f for f in os.listdir(dossier) if f.endswith('.json')]
            pathJson = f"data/{id}/uploaded.json"
            with open(pathJson, 'r') as fichier:
                if os.path.getsize(pathJson) > 0:
                    uploadJson = json.load(fichier)
                else:
                    uploadJson = {}
            print(f"uploadJson: {uploadJson}")
            print(f"uploaded: {uploadJson.get(f'{id}', [])}")
            try :
                for i in range(len(fichiers)):
                    if fichiers[i] not in videosChoosed and fichiers[i].split(".")[0] not in uploadJson.get(f'{id}', []):
                        print("video valide pour l'upload")
                        idVideo = fichiers[i].split(".")[0]
                        videosChoosed.append(idVideo)
                        break
            except Exception as e:
                print(f"Erreur lors de la sélection des vidéos: {e}")

            if len(videosChoosed) > 0 :chosen_videos_data.append({"account_id": id, "chosen_videos": videosChoosed})
            videosChoosed = []
        else :
            print(f"Aucune vidéo à uploader pour le compte {id}")


def grabTweetByEntryId(entryId, filePath):
    tweet = None
    try:
        with open(filePath, 'r') as fichier:
            contenu = json.load(fichier)
            instructions = contenu['data']['user']['result']['timeline_v2']['timeline']['instructions']
            timeLineAddEntries = []
            timelinePinEntry = []

            for instruction in instructions:
                if 'entries' in instruction:
                    timeLineAddEntries.extend(instruction['entries'])
                elif 'entry' in instruction:
                    timelinePinEntry.append(instruction['entry'])

            entries = timeLineAddEntries + timelinePinEntry

            for entry in entries:
                if entry['entryId'] == "tweet-" + entryId:
                    tweet = {'data': {'tweetResult': entry['content']['itemContent']['tweet_results']}}
                    break
    except Exception as e:
        print(entryId)
        print(filePath)
        print(f"Erreur lors de la lecture du fichier: {e}")
        return None

    return tweet

def createEachSubVideoOfScrappedTweets(ids):
    for id in ids:
        dossier = f"data/{id}"
        fichiers = [f for f in os.listdir(dossier + "/data") if f.endswith('.json')]
        if "uploaded.json" in fichiers:
            fichiers.remove("uploaded.json")
        for i in range(len(fichiers)):
            filePath = os.path.join(dossier + "/data", fichiers[i])
            print(filePath)
            with open(filePath, 'r', encoding='utf-8') as fichier:
                contenu = json.load(fichier)
                videos = rechercher_entry_id(contenu)
                for video in videos:
                    try:
                        file_path = f"{dossier}/tweet/{video}.json"
                        data = grabTweetByEntryId(video, filePath)
                        if data is None:
                            continue
                        with open(file_path, 'w') as tweet:
                            json.dump(data, tweet)
                    except Exception as e:
                        print(f"Erreur lors du téléchargement de la vidéo: {e}")
                        return createEachSubVideoOfScrappedTweets(ids)
        print(f"Création des sous vidéos du compte {id} terminée")

if __name__ == '__main__':
    initFolder(ids)
    while True:
        initConnectionAccount()
        scraperVideos(ids)
        createEachSubVideoOfScrappedTweets(ids)
        choose3videosToUpload()
        print(chosen_videos_data)

        poster_tweet()
        time.sleep(random.randint(36000, 50400))

