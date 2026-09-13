# UFO Catcher

Jeu d'arcade interactif développé dans le cadre d'un projet universitaire
en équipe de trois : Lisa Larive, Sylvie Zhang et Joelly Huin.

Le projet reproduit le fonctionnement d'une machine à pince :
le joueur contrôle une pince à l'aide d'un joystick et d'un bouton
connectés à un Raspberry Pi afin d'attraper des peluches.

Le projet comprend également une application web permettant de consulter
les informations du joueur, son score et sa collection.

## Technologies

- Python
- Pygame
- Flask
- SQLite3
- HTML / CSS / JavaScript
- Raspberry Pi
- Figma

## Architecture

Le projet est composé de deux parties principales :

- Jeu : Pygame + Raspberry Pi
- Application web : Flask + HTML/CSS/JavaScript

Les deux parties utilisent une base de données SQLite commune.

## État du projet

Ce projet a été développé et testé sur un Raspberry Pi équipé du
matériel nécessaire au fonctionnement de la machine.

Le matériel utilisé dans le cadre universitaire n'étant plus disponible,
le projet n'est actuellement pas directement rejouable dans les mêmes
conditions.

L'application web n'est également plus déployée.

Le code source et les documents sont donc conservés principalement comme
archive du projet universitaire, permettant de consulter sa conception,
son architecture et les différentes étapes de sa réalisation.

Un ancien README est également conservé dans le dossier `src/`.
Il présente les instructions qui permettaient de lancer le jeu et
l'application web lorsque le projet était encore utilisé dans son
environnement d'origine. Ces instructions sont aujourd'hui conservées
à titre documentaire et ne garantissent plus le fonctionnement du projet.

## Fonctionnement

Lors de son utilisation, le joueur pouvait :

lancer le jeu sur le Raspberry Pi ;
contrôler la pince avec le joystick ;
utiliser le bouton pour attraper une peluche ;
consulter les résultats affichés sur l'écran LCD ;
retrouver ses informations et sa collection sur l'application web.

La base de données SQLite permettait de faire le lien entre le jeu et
l'application web

## Conception IHM

La conception de l'interface a d'abord été réalisée individuellement
par chaque membre du groupe. La proposition de Lisa Larive a ensuite
servi de base pour la structure de l'interface finale, après comparaison
des différentes propositions et réalisation de tests utilisateurs.

Le rapport individuel de conception IHM et les résultats des tests sont
disponibles dans `docs/ihm/`.

Évaluation individuelle : 20/20.

## Documentation

Les différents documents produits au cours du projet sont disponibles
dans le dossier `docs/` :

- **Rapport final** : présentation du projet et de sa réalisation ;
- **soutenance** : support utilisé pour la soutenance ;
- **Démonstration** : document lié à la démonstration du projet sur
  Raspberry Pi ;
- **IHM** : documents liés à la conception individuelle et à l'évaluation des
  interfaces.