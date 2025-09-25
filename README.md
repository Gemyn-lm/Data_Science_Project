# 🧠 Data Science Project — Analyse de l’équilibrage dans *Valorant*

## 🎯 Objectif du projet

Dans ce projet, nous avons choisi d’analyser les données du jeu *Valorant* développé par Riot Games, afin d’identifier d’éventuels problèmes d’équilibrage pouvant nuire à l’expérience des joueurs.

## 📊 Données utilisées

Nous avons utilisé un dataset provenant de **Kaggle**, contenant des statistiques détaillées telles que :

- **Winrate** (taux de victoire)
- **Pickrate** (taux de sélection)

Ces données sont segmentées par **personnage**, **rang** (elo) et **carte** (map).

## 🛠️ Méthodologie

Pour explorer et visualiser les données, nous avons utilisé [**Streamlit**](https://docs.streamlit.io/
), une bibliothèque Python permettant de créer des interfaces web interactives pour les projets de data science.

### Visualisations proposées :

- Graphiques comparant les winrates par personnage en fonction de la **map** ou du **rank**.
- Outil permettant de **trouver le meilleur personnage** à jouer selon un **niveau** et une **map** donnés.
- Représentations interactives pour faciliter la compréhension intuitive des déséquilibres éventuels.

## 🧩 Interprétation

L’interprétation de ces statistiques permet :

- D’identifier des **anomalies** ou des **déséquilibres** dans le design des agents.
- De proposer des **axes d’amélioration** pour les futurs patch notes en matière d’équilibrage.

---

### 🔍 Exemples d'applications :

- Aide à la prise de décision pour les game designers.
- Recommandation de personnages pour les joueurs selon leur niveau.
- Détection de personnages surpuissants ou sous-performants.