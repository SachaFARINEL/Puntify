# SpotiDLIS

@authors : Hervouet Clément & Farinel Sacha

## Lancement

Cloner le projet depuis le [Github](https://github.com/SachaFARINEL/Puntify) ou dézipper le dossier.

Un `docker-compose.yml` permet de lancer 2 conteneurs:
- un Alpine Linux avec Python 3.10 d'installé accessible via le port `80`
- un MongoDB accesible via le port `27017`

`docker compose up -d --build` pour lancer les images

## Infos

Le framework utilisé est [FastAPI](https://fastapi.tiangolo.com/). La route `/docs` permet donc d'accéder à la documentation OpenAPI.  
<br>
Le premier utilisateur créé possèdera le statut "admin" et pourra donc accéder à l'ensemble des fonctionnalités présent dans la page d'accueil `/home`.  

Au lancement de l'application, il faudra ajouter une musique (Seulement l'admin en a les droits).

## Les fonctionnalitées demandées

1. [x] Design de type bibliothèque, avec un framework CSS. Nous avons utilsé le framework CSS [Bulma](https://bulma.io/) (Que nous avons découvert). Bulma est facile d'utilisation, flexible, responsive, compatibile avec l'ensemble des navigateurs et possède une communauté active.
2. [x] L'application doit comporter au minimum des routes d'API pour :
   1. [x] Afficher une page d'accueil (Home) avec un mot de bienvenue
   2. [x] Afficher une page Bibliothèque qui liste dans une table tous les titres
   3. [x] Affiche une page /profil dans laquelle on retrouve les informations de l'utilisateur
   4. [x] Par extension on devra retrouver toutes les routes d'API liées a cet usage, a savoir get/post/put/delete pour les titres. Mais également les route signup, signin pour les comptes utilisateurs avec une gestion par cookie d'authentification.
   5. [x] Une formulaire d'upload permettant a un utilisateur enregistré de charger un fichier de musique.
3. [x] La liste des titres, ainsi que la liste des users devront etre enregistrés dans une base de données MongoDB. Nous avons opté pour un mongo dans un image Docker.
4. [x] Une page d'administration permettra de visualiser tous les utilisateurs de l'application sous forme de table avec la possibilité de supprimer un utilisateur.
5. [x] L'architecture de votre application devra permettre de séparer distinctement les routes d'authentification et de role supérieurs (type admin) des routes classiques
6. [x] Mise en place d'un Router
7. [x]  En haut de la page de bibliothèque des titres, un lecteur avec deux boutons Play / Stop, devra permettre de lancer l'écoute du titre sélectionné dans la bibliothèque.
8. [x] Utilisation de la musique en "Stream"
