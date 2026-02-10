# GameTracker

Mini-projet individuel BUT Science des Données - Automatisation et Tests.
Ce projet implémente un pipeline ETL (Extract, Transform, Load) conteneurisé pour analyser les scores de jeux vidéo.

## Description
Le projet récupère des données brutes (fichiers CSV), les nettoie, les stocke dans une base de données MySQL et génère un rapport statistique.
Tout est orchestré via Docker Compose.

## Prérequis
- Docker
- Docker Compose

## Installation et Lancement
1. Cloner le dépôt.
2. Lancer le projet et générer le rapport :
   ```bash
   docker compose up -d --build
   ```
3. Le pipeline s'exécute automatiquement.
4. Le rapport sera généré dans `gametracker/output/rapport.txt`.

## Structure du Projet
```
gametracker/
├── docker-compose.yml   # Orchestration des services
├── Dockerfile           # Image de l'application Python
├── requirements.txt     # Dépendances Python
├── data/raw/            # Données sources (CSV)
├── scripts/             # Scripts d'automatisation (SQL, Bash)
├── src/                 # Code source Python (ETL, Config, Report)
└── output/              # Rapports générés
```

## Traitement des Données (Qualité)
Le pipeline corrige automatiquement les problèmes suivants :
1. **Doublons** : Suppression des doublons sur `player_id` et `score_id`.
2. **Emails invalides** : Remplacement par NULL si ne contient pas '@'.
3. **Dates incohérentes** : Conversion en format standard ou NULL si invalide.
4. **Espaces parasites** : Nettoyage des `username`.
5. **Scores négatifs** : Suppression des scores <= 0.
6. **Valeurs manquantes** : Gestion des NaN/None.
7. **Références orphelines** : Suppression des scores liés à des joueurs inexistants.

## Auteur
Esthor Paul
