# ===============================
# 🧭 Tableau de bord - Administrateur
# ===============================
# Fichier : gaia_admin_dashboard.py

import streamlit as st
import pandas as pd
import datetime
import os

# -------------------------------
# CONFIGURATION DE LA PAGE
# -------------------------------
st.set_page_config(
    page_title="Admin - Sauver Gaïa",
    page_icon="🛰️",
    layout="wide"
)

# -------------------------------
# FICHIER DE PROGRESSION
# -------------------------------
progress_file = os.getenv("GAIA_PROGRESS_PATH", "progress.csv")

if not os.path.exists(progress_file):
    df_init = pd.DataFrame(columns=["Team", "Mission", "Score", "Hint", "Last_Update"])
    df_init.to_csv(progress_file, index=False)

def load_progress():
    return pd.read_csv(progress_file)

def save_progress(df):
    df.to_csv(progress_file, index=False)

# -------------------------------
# STYLE
# -------------------------------
st.markdown("""
<style>
    .title {
        text-align: center;
        font-size: 2.4em;
        color: #1E88E5;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        font-style: italic;
        color: #555;
        margin-bottom: 30px;
    }
    .hint-box {
        background-color: #e3f2fd;
        border-left: 5px solid #1E88E5;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# EN-TÊTE
# -------------------------------
st.markdown('<div class="title">🛰️ Tableau de bord – Opération Sauver Gaïa</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Suivi en temps réel des équipes</div>', unsafe_allow_html=True)

# -------------------------------
# AFFICHAGE DES DONNÉES
# -------------------------------
st.header("📋 Progression des équipes")
progress = load_progress()

if progress.empty:
    st.info("Aucune équipe enregistrée pour l'instant.")
else:
    st.dataframe(progress, use_container_width=True)

# -------------------------------
# ENVOYER UN INDICE PERSONNALISÉ
# -------------------------------
st.header("💬 Envoyer un indice à une équipe")

if not progress.empty:
    team_selected = st.selectbox("Choisir une équipe :", progress["Team"].unique())
    custom_hint = st.text_area("Écris l'indice ou message à envoyer :")

    if st.button("📨 Envoyer l'indice"):
        progress.loc[progress["Team"] == team_selected, ["Hint", "Last_Update"]] = [
            custom_hint, datetime.datetime.now().strftime("%H:%M:%S")
        ]
        save_progress(progress)
        st.success(f"Indice envoyé à **{team_selected}** ✅")

# -------------------------------
# AJUSTER SCORE OU MISSION
# -------------------------------
st.header("⚙️ Ajuster manuellement les missions / scores")

if not progress.empty:
    team_selected2 = st.selectbox("Choisir une équipe à modifier :", progress["Team"].unique(), key="adjust")
    col1, col2 = st.columns(2)
    with col1:
        new_score = st.number_input("Nouveau score :", min_value=0, step=5)
    with col2:
        new_mission = st.number_input("Mission actuelle :", min_value=1, max_value=4, step=1)

    if st.button("🔁 Mettre à jour les informations"):
        progress.loc[progress["Team"] == team_selected2, ["Score", "Mission", "Last_Update"]] = [
            new_score, new_mission, datetime.datetime.now().strftime("%H:%M:%S")
        ]
        save_progress(progress)
        st.success(f"✅ Données mises à jour pour {team_selected2}")

# -------------------------------
# RÉINITIALISER LE JEU
# -------------------------------
st.header("🧹 Réinitialiser toutes les données")

if st.button("⚠️ Réinitialiser le fichier de progression"):
    df_init = pd.DataFrame(columns=["Team", "Mission", "Score", "Hint", "Last_Update"])
    save_progress(df_init)
    st.warning("Toutes les données ont été réinitialisées. Le jeu recommence à zéro.")

# -------------------------------
# NOTES FINALES
# -------------------------------
st.markdown("---")
st.caption("🪶 Créé pour l'Escape Game pédagogique *Opération Sauver Gaïa* – by Japhet Calixte N'dri 🌍")
