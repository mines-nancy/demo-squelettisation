# Conteneur Docker de la démonstration squelettisation

L'objectif de ce projet est de conteneuriser la démonstration de squelettisation par intelligence artificielle du TechLab.
L'objectif est que la démonstration soit clé en main, pour toute personne amenée à présenter le TechLab.
Cette démonstration est conçue pour fonctionner sur un ordinateur sous Linux (testé majoritairement sur la distribution Ubuntu) avec une carte graphique Nvidia, dont les drivers sont configurés correctement pour une utilisation à travers des conteneurs Docker.

# Utilisation
## Exécution

Afin d'exécuter cette démonstration, il est nécessaire d'avoir, dans un seul dossier sur l'ordinateur : 
- le script bash (execute.sh)
- le fichier contenant l'image du conteneur (nommée avec le format "image_demo_squelettisation_v*.tar.gz"), dans le cas où l'image n'a pas déjà été installée sur l'ordinateur (elle peut être supprimée après une première exécution)

Une fois les fichiers nécessaires rassemblés et placés dans le répertoire de travail actif, `./execute.sh` peut être utilisé pour exécuter le script. Ce dernier guidera ensuite l'utilisateur.

> [!TIP]
> Dans le cas où l'exécution du programme échoue avec des erreurs en rapport avec CUDA, Nvidia ou ayant un quelconque lien avec le GPU, il est probable que les drivers Nvidia ne soient pas configurés correctement pour cette utilisation sur l'ordinateur utilisé. 

## Arrêt

Pour arrêter la démonstration, fermer la fenêtre de visualisation de la vidéo n'est pas suffisant, il faut stopper l'exécution du script. Pour ce faire, il suffit d'appuyer sur <kbd>Ctrl</kbd>+<kbd>C</kbd> en ayant sélectionné le terminal comme fenêtre active.
