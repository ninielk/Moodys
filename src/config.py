"""
Configuration de la méthodologie Moody's — Global Manufacturing Companies (Juin 2017).

Référence : Rating Methodology - Global Manufacturing Companies, 14 June 2017.
Les seuils, pondérations et grilles sont extraits directement du document méthodologique.
"""

# ---------------------------------------------------------------------------
# Echelle numérique Moody's (broad categories)
# ---------------------------------------------------------------------------
BROAD_CATEGORY_SCORES = {
    "Aaa": 1, "Aa": 3, "A": 6, "Baa": 9,
    "Ba": 12, "B": 15, "Caa": 18, "Ca": 20,
}

# ---------------------------------------------------------------------------
# Mapping score composite → rating alphanumérique
# ---------------------------------------------------------------------------
SCORE_TO_ALPHA_RATING = [
    ("Aaa",  0.0,  1.5),  ("Aa1",  1.5,  2.5),  ("Aa2",  2.5,  3.5),
    ("Aa3",  3.5,  4.5),  ("A1",   4.5,  5.5),   ("A2",   5.5,  6.5),
    ("A3",   6.5,  7.5),  ("Baa1", 7.5,  8.5),   ("Baa2", 8.5,  9.5),
    ("Baa3", 9.5, 10.5),  ("Ba1", 10.5, 11.5),   ("Ba2", 11.5, 12.5),
    ("Ba3", 12.5, 13.5),  ("B1",  13.5, 14.5),   ("B2",  14.5, 15.5),
    ("B3",  15.5, 16.5),  ("Caa1",16.5, 17.5),   ("Caa2",17.5, 18.5),
    ("Caa3",18.5, 19.5),  ("Ca",  19.5, 21.0),
]

# ---------------------------------------------------------------------------
# Sub-factors : poids, type, seuils
# ---------------------------------------------------------------------------
SUBFACTORS = [
    {
        "id": "business_profile",
        "name": "Business Profile",
        "group": "Business Profile",
        "weight": 0.20,
        "type": "qualitative",
    },
    {
        "id": "revenue",
        "name": "Revenue (USD Mds)",
        "group": "Scale",
        "weight": 0.20,
        "type": "quantitative",
        "thresholds": [
            ("Aaa", 40, None), ("Aa", 20, 40), ("A", 10, 20), ("Baa", 5, 10),
            ("Ba", 1.5, 5), ("B", 0.25, 1.5), ("Caa", 0.1, 0.25), ("Ca", None, 0.1),
        ],
    },
    {
        "id": "ebita_margin",
        "name": "Marge EBITA (%)",
        "group": "Profitability",
        "weight": 0.10,
        "type": "quantitative",
        "thresholds": [
            ("Aaa", 25, None), ("Aa", 20, 25), ("A", 15, 20), ("Baa", 10, 15),
            ("Ba", 5, 10), ("B", 2.5, 5), ("Caa", 0, 2.5), ("Ca", None, 0),
        ],
    },
    {
        "id": "ebita_interest",
        "name": "EBITA / Intérêts (x)",
        "group": "Leverage & Coverage",
        "weight": 0.10,
        "type": "quantitative",
        "thresholds": [
            ("Aaa", 15, None), ("Aa", 12, 15), ("A", 8, 12), ("Baa", 5, 8),
            ("Ba", 2.5, 5), ("B", 1, 2.5), ("Caa", 0.5, 1), ("Ca", None, 0.5),
        ],
    },
    {
        "id": "debt_ebitda",
        "name": "Debt / EBITDA (x)",
        "group": "Leverage & Coverage",
        "weight": 0.10,
        "type": "quantitative",
        "direction": "lower_is_better",
        "thresholds": [
            ("Aaa", None, 0.5), ("Aa", 0.5, 1), ("A", 1, 1.75), ("Baa", 1.75, 3.25),
            ("Ba", 3.25, 4.75), ("B", 4.75, 6.25), ("Caa", 6.25, 7.75), ("Ca", 7.75, None),
        ],
    },
    {
        "id": "rcf_net_debt",
        "name": "RCF / Net Debt (%)",
        "group": "Leverage & Coverage",
        "weight": 0.10,
        "type": "quantitative",
        "thresholds": [
            ("Aaa", 60, None), ("Aa", 45, 60), ("A", 35, 45), ("Baa", 25, 35),
            ("Ba", 15, 25), ("B", 7.5, 15), ("Caa", 0, 7.5), ("Ca", None, 0),
        ],
    },
    {
        "id": "fcf_debt",
        "name": "FCF / Debt (%)",
        "group": "Leverage & Coverage",
        "weight": 0.10,
        "type": "quantitative",
        "thresholds": [
            ("Aaa", 25, None), ("Aa", 20, 25), ("A", 15, 20), ("Baa", 10, 15),
            ("Ba", 5, 10), ("B", 0, 5), ("Caa", -5, 0), ("Ca", None, -5),
        ],
    },
    {
        "id": "financial_policy",
        "name": "Financial Policy",
        "group": "Financial Policy",
        "weight": 0.10,
        "type": "qualitative",
    },
]

# ---------------------------------------------------------------------------
# Descriptions qualitatives — Business Profile
# ---------------------------------------------------------------------------
BUSINESS_PROFILE_DESC = {
    "Aaa": "Volatilité quasi inexistante. Position dominante, avantages de coûts et techno ancrés, couverture mondiale.",
    "Aa":  "Très faible volatilité. Leader profondément ancré, défendable par coûts et techno, exposition mondiale.",
    "A":   "Faible volatilité. Position forte, avantages concurrentiels démontrés, diversification solide.",
    "Baa": "Volatilité modérée. Position solide sur marchés clés. Intégration verticale ou pass-through. Bonne diversification.",
    "Ba":  "Produits largement indifférenciés, marché concurrentiel. Tempéré par position établie et diversification correcte.",
    "B":   "Produits indifférenciés, concurrence intense, clients price-sensitive. Résultats très volatils. Concentration élevée.",
    "Caa": "Volatilité extrême. Présence modeste, peu d'avantages, coûts potentiellement élevés. 1-2 sites.",
    "Ca":  "Cash flows très volatils, mono-produit, position insignifiante, aucun pricing power, site unique non compétitif.",
}

# ---------------------------------------------------------------------------
# Descriptions qualitatives — Financial Policy
# ---------------------------------------------------------------------------
FINANCIAL_POLICY_DESC = {
    "Aaa": "Politiques extrêmement conservatrices. Métriques très stables. Engagement long terme très solide.",
    "Aa":  "Politiques très stables et conservatrices. Risque d'événement minimal. Engagement crédit fort.",
    "A":   "Politiques prévisibles préservant les créanciers. Risque d'événement modeste et temporaire.",
    "Baa": "Équilibre créanciers/actionnaires. Risque de migration via acquisitions ou distributions.",
    "Ba":  "Tendance à favoriser les actionnaires. Risque financier supérieur à la moyenne.",
    "B":   "Favorise actionnaires au détriment des créanciers. Risque financier élevé.",
    "Caa": "Risque élevé de restructuration de dette en environnements variés.",
    "Ca":  "Risque élevé de restructuration même en environnement économique sain.",
}

# ---------------------------------------------------------------------------
# Couleurs
# ---------------------------------------------------------------------------
LMG_PRIMARY = "#004B87"
LMG_PRIMARY_LIGHT = "#0072CE"

RATING_COLORS = {
    "Aaa": "#1B5E20", "Aa": "#2E7D32", "A": "#43A047", "Baa": "#66BB6A",
    "Ba": "#FFA726", "B": "#F57C00", "Caa": "#E53935", "Ca": "#B71C1C",
}

IG_RATINGS = {"Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3", "Baa1", "Baa2", "Baa3"}
