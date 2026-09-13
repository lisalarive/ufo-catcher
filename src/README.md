# Projet UFO-catcher
Groupe 3 LU1IN021 - Joelly Huin, Sylvie Zhang, Lisa Larive

## Explication du projet:
Notre groupe a créé un UFO-catcher permettant au joueur de contrôler la pince à l'aide du module Raspberry Pi, équipé d'un joystick et d'un bouton. Le jeu affiche également les résultats du joueur sur un écran LCD et une musique change en fonction de la peluche attrapée. De plus, il permet au joueur de suivre ses statistiques grâce à son compte.

## Comment lancer le projet:
Le projet est divisé en deux parties :
   - Le site (Flask)
   - Le jeu (Pygame)
Les deux sont reliés par une base de données commune.

Pour lancer le projet, commencez par exécuter le fichier `game.py`. Vous pouvez créer un compte ou vous connecter, puis accéder au site `app.py` en lançant Flask (`run flask`).

Alternativement, nous avons créé un fichier qui peut ouvrir directement les deux en exécutant la commande suivante dans le terminal:
```bash
./start.sh
```
⚠️ Cependant, veillez à ne pas fermer la fenêtre du jeu pendant l'utilisation. ⚠️

Le site est hébergé sur le localhost:5000.

## Explication des fichiers:

### Dossiers:

- **dossier jeux:**  
  Contient tous les assets du jeu (images et musiques).

- **dossier templates:**  
  Contient tous les fichiers HTML et CSS pour le site.

- **dossier static:**  
  Contient les assets du site.

### Fichiers:

- **game.py:**  
  Contient le jeu, la gestion et la création de la base de données.

- **UFO-Catcher.bd:**  
  La base de données du jeu et du site.

- **app.py:**  
  Le fichier Flask avec les différentes routes, requêtes, etc.

- **start.sh:**  
  Fichier de lancement du site et du jeu.