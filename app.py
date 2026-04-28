"""
Credit Scorecard — Global Manufacturing Companies
Direction des Investissements, La Mutuelle Generale
Reference : Moody's Rating Methodology, Juin 2017.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from src import (
    BROAD_CATEGORY_SCORES,
    SUBFACTORS,
    BUSINESS_PROFILE_DESC,
    FINANCIAL_POLICY_DESC,
    LMG_PRIMARY,
    LMG_PRIMARY_LIGHT,
    RATING_COLORS,
    run_rating,
)

st.set_page_config(page_title="Credit Scorecard — Manufacturing", page_icon="◆", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    .stApp { font-family: 'Inter', -apple-system, sans-serif; background: #FAFBFC; }
    .hbar { background:#1B2A4A; padding:1.1rem 1.8rem; border-radius:3px; margin-bottom:1.4rem; display:flex; align-items:center; justify-content:space-between; }
    .hbar .t { color:#FFF; font-size:1.1rem; font-weight:600; }
    .hbar .s { color:#8BA3C7; font-size:.76rem; margin-top:2px; }
    .hbar .tag { background:rgba(255,255,255,.12); color:#8BA3C7; padding:.22rem .65rem; border-radius:2px; font-size:.68rem; font-weight:500; letter-spacing:.04em; text-transform:uppercase; }
    .sl { font-size:.68rem; font-weight:600; color:#6B7A90; text-transform:uppercase; letter-spacing:.06em; margin:1.2rem 0 .4rem; padding-bottom:.25rem; border-bottom:2px solid #1B2A4A; display:inline-block; }
    .rd { display:flex; align-items:center; gap:1.2rem; padding:1.1rem 1.4rem; background:#FFF; border:1px solid #E1E5EB; border-left:4px solid #1B2A4A; border-radius:2px; }
    .rd .rv { font-size:2.1rem; font-weight:700; color:#1B2A4A; line-height:1; }
    .rd .rm { font-size:.78rem; color:#6B7A90; line-height:1.5; }
    .rd .rm strong { color:#1B2A4A; }
    .gp { display:inline-block; padding:.2rem .6rem; border-radius:2px; font-weight:600; font-size:.72rem; letter-spacing:.02em; }
    .gp.ig { background:#E8F5E9; color:#2E7D32; }
    .gp.sg { background:#FFEBEE; color:#C62828; }
    .fl { background:#F4F6F8; border-left:3px solid #1B2A4A; padding:.4rem .75rem; margin:.7rem 0 .35rem; font-weight:600; font-size:.8rem; color:#1B2A4A; }
    .qn { background:#F4F6F8; padding:.45rem .75rem; font-size:.76rem; color:#4A5568; border-radius:2px; margin-top:.25rem; line-height:1.5; }
    .disc { text-align:left; padding:1rem 0; color:#8BA3C7; font-size:.66rem; border-top:1px solid #E1E5EB; margin-top:2rem; line-height:1.6; }
    section[data-testid="stSidebar"] { background:#F4F6F8; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hbar">
    <div><div class="t">Credit Scorecard — Global Manufacturing Companies</div>
    <div class="s">Direction des Investissements · La Mutuelle Generale</div></div>
    <div class="tag">Methodologie Juin 2017</div>
</div>""", unsafe_allow_html=True)

BROAD_CATS = list(BROAD_CATEGORY_SCORES.keys())

with st.sidebar:
    st.markdown("**Reference methodologique**")
    st.caption("Grille de notation pour les Global Manufacturing Companies (14 juin 2017). Estimation du rating indicatif d'un emetteur.")
    st.markdown("---")
    st.markdown("**Ponderations**")
    st.dataframe(pd.DataFrame([{"Sub-Factor": s["name"], "Poids": f'{s["weight"]:.0%}'} for s in SUBFACTORS]), hide_index=True, use_container_width=True)
    st.markdown("---")
    st.markdown("**Echelle numerique**")
    st.dataframe(pd.DataFrame([{"Categorie": k, "Score": v} for k, v in BROAD_CATEGORY_SCORES.items()]), hide_index=True, use_container_width=True)
    st.markdown("---")
    st.caption("Usage interne. Ne constitue pas une opinion de credit officielle.")

issuer_name = st.text_input("Emetteur", placeholder="Ex : Schneider Electric SE, Siemens AG, Legrand SA")
inputs = {}

with st.expander("Factor 1 — Business Profile (20%)", expanded=True):
    st.markdown('<div class="fl">Evaluation qualitative du profil d\'activite</div>', unsafe_allow_html=True)
    st.caption("Volatilite attendue, position concurrentielle, diversification produit/geographique, concentration operationnelle.")
    bp = st.select_slider("Categorie", options=BROAD_CATS, value="Baa", key="bp")
    st.markdown(f'<div class="qn"><strong>{bp}</strong> — {BUSINESS_PROFILE_DESC[bp]}</div>', unsafe_allow_html=True)
    inputs["business_profile"] = bp

with st.expander("Factor 2 — Scale (20%)", expanded=True):
    st.markdown('<div class="fl">Chiffre d\'affaires annuel</div>', unsafe_allow_html=True)
    inputs["revenue"] = st.number_input("Revenue (USD Milliards)", min_value=0.0, max_value=500.0, value=5.0, step=0.5, format="%.2f", help="CA annuel en milliards USD (dernier exercice ou LTM).")

with st.expander("Factor 3 — Profitability (10%)", expanded=True):
    st.markdown('<div class="fl">Marge EBITA ajustee</div>', unsafe_allow_html=True)
    st.caption("EBITA ajuste, hors charges non recurrentes. Privilegie a l'EBITDA car integre la D&A.")
    inputs["ebita_margin"] = st.number_input("Marge EBITA (%)", min_value=-50.0, max_value=100.0, value=12.0, step=0.5, format="%.1f")

with st.expander("Factor 4 — Leverage & Coverage (40%)", expanded=True):
    st.markdown('<div class="fl">Ratios de couverture et d\'endettement</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        inputs["ebita_interest"] = st.number_input("EBITA / Charges d'interets (x)", min_value=0.0, max_value=100.0, value=6.0, step=0.5, format="%.1f")
        inputs["rcf_net_debt"] = st.number_input("RCF / Net Debt (%)", min_value=-100.0, max_value=200.0, value=30.0, step=1.0, format="%.1f")
    with c2:
        inputs["debt_ebitda"] = st.number_input("Debt / EBITDA (x)", min_value=0.0, max_value=30.0, value=2.5, step=0.25, format="%.2f")
        inputs["fcf_debt"] = st.number_input("FCF / Debt (%)", min_value=-50.0, max_value=100.0, value=8.0, step=0.5, format="%.1f")

with st.expander("Factor 5 — Financial Policy (10%)", expanded=True):
    st.markdown('<div class="fl">Evaluation qualitative de la politique financiere</div>', unsafe_allow_html=True)
    st.caption("Tolerance du management pour le risque financier, historique M&A, distributions, engagement credit.")
    fp = st.select_slider("Categorie", options=BROAD_CATS, value="Baa", key="fp")
    st.markdown(f'<div class="qn"><strong>{fp}</strong> — {FINANCIAL_POLICY_DESC[fp]}</div>', unsafe_allow_html=True)
    inputs["financial_policy"] = fp

st.markdown("---")

if st.button("Calculer le rating indicatif", use_container_width=True, type="primary"):
    result = run_rating(inputs)
    issuer = issuer_name.strip() or "Emetteur"
    ig_cls = "ig" if result["ig"] == "Investment Grade" else "sg"

    st.markdown('<div class="sl">Resultat</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="rd">
        <div class="rv">{result["alpha"]}</div>
        <div class="rm"><strong>{issuer}</strong><br>Score composite : {result["composite"]}<br><span class="gp {ig_cls}">{result["ig"]}</span></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sl">Detail par sub-factor</div>', unsafe_allow_html=True)
    df = pd.DataFrame(result["details"]).rename(columns={"name":"Sub-Factor","group":"Groupe","weight":"Poids","value":"Valeur","category":"Categorie","score":"Score","weighted":"Score Pondere"})
    df["Poids"] = df["Poids"].apply(lambda x: f"{x:.0%}")
    st.dataframe(df[["Groupe","Sub-Factor","Valeur","Categorie","Score","Poids","Score Pondere"]], hide_index=True, use_container_width=True)

    st.markdown('<div class="sl">Profil de risque</div>', unsafe_allow_html=True)
    cats = [d["name"] for d in result["details"]]
    scores = [d["score"] for d in result["details"]]
    fig = go.Figure(go.Scatterpolar(r=scores+[scores[0]], theta=cats+[cats[0]], fill="toself", fillcolor="rgba(27,42,74,0.08)", line=dict(color="#1B2A4A",width=1.5), marker=dict(size=5,color="#1B2A4A")))
    fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)", radialaxis=dict(visible=True,range=[0,20],tickvals=[1,3,6,9,12,15,18,20],ticktext=["Aaa","Aa","A","Baa","Ba","B","Caa","Ca"],tickfont=dict(size=9,color="#6B7A90"),gridcolor="#E1E5EB"), angularaxis=dict(tickfont=dict(size=10,color="#1B2A4A"),gridcolor="#E1E5EB")), showlegend=False, margin=dict(l=60,r=60,t=30,b=30), height=400, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter,sans-serif"))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="sl">Contribution au score composite</div>', unsafe_allow_html=True)
    bc = []
    for d in result["details"]:
        c = d["category"]
        bc.append("#3D7A5F" if c in ("Aaa","Aa","A") else "#5A7D9A" if c=="Baa" else "#C4873B" if c=="Ba" else "#A94442")
    fig_bar = go.Figure(go.Bar(x=[d["weighted"] for d in result["details"]], y=[d["name"] for d in result["details"]], orientation="h", marker_color=bc, text=[f'{d["weighted"]:.2f}' for d in result["details"]], textposition="auto", textfont=dict(size=11,color="white")))
    fig_bar.update_layout(xaxis_title="Score pondere", yaxis=dict(autorange="reversed"), margin=dict(l=10,r=20,t=10,b=40), height=320, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter,sans-serif",size=12,color="#1B2A4A"), xaxis=dict(gridcolor="#E1E5EB"))
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('<div class="disc">Cet outil fournit un rating indicatif base sur la grille methodologique publiee. Il ne constitue pas une opinion de credit officielle. Les ratings integrent des facteurs qualitatifs et forward-looking non captures par cette grille. Reference : "Global Manufacturing Companies", Moody\'s Investors Service, Juin 2017.</div>', unsafe_allow_html=True)
