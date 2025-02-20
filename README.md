# AutoTweetVideoUploader

## Description
Ce script Python permet de télécharger des vidéos depuis des comptes Twitter spécifiques et de les publier automatiquement sur un compte Twitter. Il scrute des comptes, choisit des vidéos à uploader, puis les poste sur un compte Twitter prédéfini. Ce script nécessite une configuration initiale pour fonctionner correctement.

## Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/votre-utilisateur/nom-du-depot.git
   cd nom-du-depot
   ```

2. **Installer les dépendances**
   Vous devez installer les dépendances suivantes :
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Avant d'exécuter le script, vous devez modifier certaines parties du code pour y entrer vos informations personnelles et la configuration des comptes à scraper et à publier.

### Étape 1 : Modifier les informations de connexion
Dans le fichier `main.py`, remplacez les valeurs suivantes par vos informations personnelles :

```python
email, username, pwd = "ton_mail", "ton_pseudo", "ton_mdp"
```
Entrez votre adresse email, votre nom d'utilisateur et votre mot de passe Twitter.

### Étape 2 : Ajouter les IDs des comptes Twitter à scraper
Ajoutez les identifiants des comptes Twitter dont vous souhaitez télécharger les vidéos dans la liste `ids`. Vous pouvez obtenir l'ID d'un utilisateur Twitter sur [https://ilo.so/twitter-id/](https://ilo.so/twitter-id/).

```python
ids = []
id1 = id_de_compte_1  # Remplacez avec l'ID du premier compte
id2 = id_de_compte_2  # Remplacez avec l'ID du deuxième compte
id3 = id_de_compte_3  # Remplacez avec l'ID du troisième compte

ids.append(id1)
ids.append(id2)
ids.append(id3)
```

### Étape 3 : Créer les dossiers nécessaires
Le script va automatiquement créer les dossiers nécessaires pour stocker les vidéos et les informations associées. Assurez-vous que vous avez les permissions nécessaires pour écrire dans le répertoire où le script est exécuté.

### Étape 4 : Lancer le script
Une fois que vous avez effectué les modifications, vous pouvez lancer le script avec la commande suivante :

```bash
python main.py
```

Le script fonctionnera en boucle infinie, téléchargeant et publiant des vidéos toutes les 10 à 14 heures.

## Contributeurs
Ce projet a été créé en collaboration avec [@Clement-Garro](https://github.com/Clement-Garro).
