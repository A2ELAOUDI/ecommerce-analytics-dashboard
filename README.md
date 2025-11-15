# 📊 E-commerce Analytics Dashboard

Un projet d'analyse de données e-commerce avec dashboard interactif, démontrant des compétences en **Data Analysis**, **Data Visualization**, et **Python**.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.1.4-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🎯 Objectif du Projet

Ce projet simule l'analyse complète de données e-commerce, incluant :
- Génération de données réalistes (5000 transactions)
- Calcul de KPIs business
- Visualisations interactives
- Analyses statistiques approfondies

**Cas d'usage :** Dashboard pour aider une équipe e-commerce à suivre les performances de ventes, identifier les produits les plus rentables, et comprendre le comportement des clients.

---

## ✨ Fonctionnalités

### 📈 KPIs Principaux
- Chiffre d'affaires total
- Nombre de transactions
- Panier moyen
- Nombre de clients uniques
- Taux de conversion
- Produits vendus

### 📊 Analyses Détaillées
- **Ventes par catégorie** : Répartition du CA par catégorie de produits
- **Ventes par région** : Performance géographique
- **Évolution temporelle** : Tendances des ventes (jour/semaine/mois)
- **Top produits** : Classement des produits les plus rentables
- **Segments clients** : Analyse Premium / Régulier / Occasionnel
- **Moyens de paiement** : Distribution des modes de paiement

### 🔍 Filtres Dynamiques
- Période (sélection de dates)
- Catégorie de produits
- Région géographique

---

## 🛠️ Technologies Utilisées

| Technologie | Usage |
|------------|-------|
| **Python 3.8+** | Langage principal |
| **Pandas** | Manipulation et analyse de données |
| **NumPy** | Calculs numériques |
| **Streamlit** | Dashboard web interactif |
| **Plotly** | Visualisations graphiques interactives |

---

## 📁 Structure du Projet

```
ecommerce-analytics/
│
├── data/                      # Données générées
│   ├── transactions.csv       # 5000 transactions e-commerce
│   └── customers.csv          # Informations clients
│
├── src/                       # Code source
│   ├── generate_data.py       # Script de génération de données
│   └── analysis.py            # Fonctions d'analyse et KPIs
│
├── notebooks/                 # Notebooks Jupyter (optionnel)
│
├── app.py                     # Application Streamlit principale
├── requirements.txt           # Dépendances Python
├── .gitignore                 # Fichiers ignorés par Git
└── README.md                  # Documentation
```

---

## 🚀 Installation et Lancement

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Étape 1 : Cloner le repository
```bash
git clone https://github.com/votre-username/ecommerce-analytics.git
cd ecommerce-analytics
```

### Étape 2 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 3 : Générer les données
```bash
python src/generate_data.py
```
Cela créera 5000 transactions et ~1000 clients dans le dossier `data/`.

### Étape 4 : Lancer le dashboard
```bash
streamlit run app.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse : `http://localhost:8501`

---

## 📸 Aperçu du Dashboard

### Vue d'ensemble des KPIs
Le dashboard affiche en temps réel :
- Revenus totaux
- Nombre de transactions
- Panier moyen
- Clients actifs

### Graphiques Interactifs
- Camembert : Répartition par catégorie
- Barres : Ventes par région
- Courbe temporelle : Évolution des ventes
- Top produits : Classement des best-sellers

*(Ajoutez des captures d'écran ici une fois le dashboard lancé)*

---

## 📊 Exemples d'Analyses

### KPIs Calculés
```python
# Exemple de sortie du script analysis.py
total_revenue: 2,036,508.33 EUR
total_transactions: 4,750
avg_order_value: 428.74 EUR
total_customers: 998
conversion_rate: 95.00%
```

### Top Catégories
1. **Électronique** : 1,100,098€ (54% du CA)
2. **Sports & Loisirs** : 474,625€ (23%)
3. **Maison & Jardin** : 260,504€ (13%)

### Segments Clients
- **Premium** (388 clients) : 3,706€ de dépense moyenne
- **Régulier** (449 clients) : 1,230€ de dépense moyenne
- **Occasionnel** (161 clients) : 284€ de dépense moyenne

---

## 🧪 Tests et Validation

Pour tester les fonctions d'analyse :
```bash
python src/analysis.py
```

Cela affichera un résumé des KPIs et analyses dans le terminal.

---

## 🎓 Compétences Démontrées

### Data Analysis
- Nettoyage et préparation de données
- Calcul de KPIs business
- Analyse statistique descriptive
- Segmentation clients (RFM-like)

### Data Visualization
- Création de graphiques interactifs
- Dashboard avec filtres dynamiques
- Storytelling avec les données

### Python & Développement
- Programmation orientée objet
- Gestion de fichiers CSV
- Documentation du code
- Gestion de version (Git)

---

## 🔮 Améliorations Futures

- [ ] Ajouter des prédictions de ventes avec Machine Learning (ARIMA, Prophet)
- [ ] Intégrer une vraie base de données (PostgreSQL)
- [ ] Déployer sur le cloud (Streamlit Cloud / Heroku)
- [ ] Ajouter des tests unitaires (pytest)
- [ ] Créer des rapports PDF automatiques
- [ ] Analyse de cohort pour la rétention clients
- [ ] Détection d'anomalies dans les ventes

---

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👤 Auteur

**Votre Nom**
- GitHub: [@votre-username](https://github.com/votre-username)
- LinkedIn: [Votre Profil](https://linkedin.com/in/votre-profil)
- Email: votre.email@example.com

---

## 🙏 Remerciements

- Données générées avec Python pour des besoins éducatifs
- Inspiration : dashboards e-commerce réels (Shopify, Amazon Analytics)

---

## 📚 Ressources Supplémentaires

- [Documentation Pandas](https://pandas.pydata.org/docs/)
- [Documentation Streamlit](https://docs.streamlit.io/)
- [Documentation Plotly](https://plotly.com/python/)

---

**⭐ Si ce projet vous plaît, n'hésitez pas à mettre une étoile !**
