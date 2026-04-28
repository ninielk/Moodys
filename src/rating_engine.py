"""
Moteur de calcul du rating Moody's — Global Manufacturing Companies.

1. Chaque sub-factor → broad category (Aaa → Ca)
2. Broad category → score numérique (1 → 20)
3. Score composite pondéré
4. Score composite → rating alphanumérique
"""

from .config import BROAD_CATEGORY_SCORES, SCORE_TO_ALPHA_RATING, SUBFACTORS, IG_RATINGS


def map_to_category(value: float, subfactor: dict) -> str:
    """Mappe une valeur quantitative vers la broad category Moody's."""
    for cat, lower, upper in subfactor["thresholds"]:
        if lower is None and upper is not None and value < upper:
            return cat
        if upper is None and lower is not None and value >= lower:
            return cat
        if lower is not None and upper is not None and lower <= value < upper:
            return cat
    return subfactor["thresholds"][-1][0]


def composite_to_alpha(score: float) -> str:
    """Convertit un score composite en rating alphanumérique."""
    for rating, lo, hi in SCORE_TO_ALPHA_RATING:
        if lo <= score < hi:
            return rating
    return "Ca"


def broad_cat(alpha: str) -> str:
    """Extrait la broad category d'un rating alpha (Baa1 → Baa)."""
    for c in ["Aaa", "Aa", "Baa", "Ba", "Caa", "Ca", "A", "B"]:
        if alpha.startswith(c):
            return c
    return "Ca"


def run_rating(inputs: dict) -> dict:
    """
    Calcul complet du rating.

    Paramètres
    ----------
    inputs : dict
        {subfactor_id: valeur} — catégorie pour les qualitatifs, nombre pour les quantitatifs.

    Retourne
    --------
    dict avec details, composite, alpha, broad, ig
    """
    details = []
    composite = 0.0

    for sf in SUBFACTORS:
        raw = inputs.get(sf["id"])
        if raw is None:
            continue

        if sf["type"] == "qualitative":
            cat = raw
        else:
            cat = map_to_category(float(raw), sf)

        score = BROAD_CATEGORY_SCORES[cat]
        weighted = round(score * sf["weight"], 2)
        composite += weighted

        details.append({
            "name": sf["name"],
            "group": sf["group"],
            "weight": sf["weight"],
            "value": raw,
            "category": cat,
            "score": score,
            "weighted": weighted,
        })

    composite = round(composite, 2)
    alpha = composite_to_alpha(composite)
    bc = broad_cat(alpha)

    return {
        "details": details,
        "composite": composite,
        "alpha": alpha,
        "broad": bc,
        "ig": "Investment Grade" if alpha in IG_RATINGS else "Speculative Grade",
    }
