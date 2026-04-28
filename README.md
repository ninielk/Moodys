# Scoring Crédit Moody's — Global Manufacturing Companies

**Direction des Investissements · La Mutuelle Générale**

---

## Contenu du dossier

```
Moodys_GMC/
├── app.py                              ← Dashboard Streamlit
├── src/
│   ├── __init__.py                     ← Expose les modules
│   ├── config.py                       ← Grilles, seuils, pondérations (méthodologie)
│   └── rating_engine.py                ← Moteur de calcul du rating
├── moodys_manufacturing_rating.html    ← Version offline (navigateur)
├── pyproject.toml                      ← Config Poetry
└── README.md
```

---

## Version HTML standalone (le plus simple)

Double-cliquer sur **`moodys_manufacturing_rating.html`** — c'est tout.
Aucune installation, aucun terminal. Fonctionne dans Chrome, Safari, Firefox.

---

## Version Streamlit — Lancement avec Poetry

### Prérequis

- Python 3.11+ installé
- Poetry installé (`pip install poetry` ou `brew install poetry`)

### Étapes

```bash
# 1. Aller dans le dossier du projet
cd ~/Downloads/Moodys_GMC

# 2. Installer les dépendances avec Poetry
poetry install

# 3. Lancer le dashboard Streamlit
poetry run streamlit run app.py
```

Le dashboard s'ouvre dans le navigateur à `http://localhost:8501`.

### Alternative sans Poetry (pip classique)

```bash
cd ~/Downloads/Moodys_GMC
python -m venv .venv
source .venv/bin/activate
pip install streamlit plotly pandas
streamlit run app.py
```

---

## Comment ça marche

1. Renseigner le **nom de l'émetteur**
2. Remplir les **5 facteurs** (accordéons dépliables) :
   - **Business Profile** (20%) → qualitatif, sélectionner Aaa → Ca
   - **Scale / Revenue** (20%) → CA en milliards USD
   - **Profitability / Marge EBITA** (10%) → en %
   - **Leverage & Coverage** (40%) → 4 ratios financiers
   - **Financial Policy** (10%) → qualitatif, sélectionner Aaa → Ca
3. Cliquer sur **Calculer le Rating Indicatif**
4. Résultat : rating alphanumérique, score composite, IG/SG, détail par factor, radar, barres

---

## Méthodologie

Chaque sub-factor → broad category (Aaa → Ca) → score numérique :

| Catégorie | Score |
|-----------|-------|
| Aaa       | 1     |
| Aa        | 3     |
| A         | 6     |
| Baa       | 9     |
| Ba        | 12    |
| B         | 15    |
| Caa       | 18    |
| Ca        | 20    |

Score composite pondéré → rating alphanumérique final (Aaa, Aa1, ..., Ca).

---

## Avertissement

Rating **indicatif** uniquement. Ne constitue pas une opinion de crédit officielle Moody's.

**Référence :** Moody's Investors Service, "Global Manufacturing Companies", Juin 2017.
