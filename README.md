# SpotiDLIS

## Lancement

Un `docker-compose.yml` permet de lancer 2 conteneurs:
- un Alpine Linux avec Python 3.10 d'installé accessible via le port `80`
- un MongoDB accesible via le port `27017`

`docker compuse up -d --build` pour lancer les images

## Infos

Le framework utilisé est [FastAPI](https://fastapi.tiangolo.com/). La route `/docs` permet donc d'accéder à la documentation OpenAPI.  
<br>
Le premier utilisateur créé possèdera le statut "admin" et pourra donc accéder à l'ensemble des fonctionnalités présent dans la page d'accueil `/home`.  
