# ===============================
# 🎮 Opération Sauver Gaïa - ÉQUIPE
# ===============================
# Fichier : gaia_team_app.py

import streamlit as st
import pandas as pd
import datetime
import os

# -------------------------------
# CONFIGURATION DE LA PAGE
# -------------------------------
st.set_page_config(
    page_title="Sauver Gaïa - Espace Équipe",
    page_icon="🌍",
    layout="wide"
)

# -------------------------------
# INITIALISATION DU FICHIER DE PROGRESSION
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
        color: #2E8B57;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        font-style: italic;
        color: #555;
        margin-bottom: 30px;
    }
    .hint {
        background-color: #e8f5e9;
        border-left: 5px solid #2E8B57;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .mission-box {
        background-color: #f8f9fa;
        border: 1px solid #ccc;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# FONCTIONS
# -------------------------------
def update_progress(team, mission, score, hint):
    df = load_progress()
    if team in df["Team"].values:
        df.loc[df["Team"] == team, ["Mission", "Score", "Hint", "Last_Update"]] = [
            mission, score, hint, datetime.datetime.now().strftime("%H:%M:%S")
        ]
    else:
        new_row = pd.DataFrame([{
            "Team": team,
            "Mission": mission,
            "Score": score,
            "Hint": hint,
            "Last_Update": datetime.datetime.now().strftime("%H:%M:%S")
        }])
        df = pd.concat([df, new_row], ignore_index=True)
    save_progress(df)

def get_hint(mission, score):
    hints = {
        1: "🌱 Regarde où la mer monte le plus vite…",
        2: "💡 Ce qui sauve Gaïa, ce n'est pas la machine, mais la volonté.",
        3: "🔥 Les chiffres sont froids, la conviction les réchauffe.",
        4: "🏁 Le futur se joue dans les choix que vous faites aujourd'hui."
    }
    if score < 20:
        return "Indice : observe les variables les plus extrêmes."
    return hints.get(mission, "Continuez votre exploration...")

# -------------------------------
# INTERFACE PRINCIPALE
# -------------------------------
st.markdown('<div class="title">🌍 Opération Sauver Gaïa</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Espace privé de votre équipe</div>', unsafe_allow_html=True)

team_name = st.text_input("🧭 Entrez le nom de votre équipe :").strip()
if not team_name:
    st.stop()

st.success(f"Bienvenue, **{team_name}** ! 🌿")
progress = load_progress()

if team_name in progress["Team"].values:
    current_mission = int(progress.loc[progress["Team"] == team_name, "Mission"].values[0])
    score = int(progress.loc[progress["Team"] == team_name, "Score"].values[0])
else:
    current_mission = 1
    score = 0
    update_progress(team_name, current_mission, score, "")

# -------------------------------
# MISSIONS DYNAMIQUES
# -------------------------------
st.header(f"🚀 Mission {current_mission}")

if current_mission == 1:
    st.markdown('<div class="mission-box"><b>Objectif :</b> Identifier la région la plus vulnérable en 2050.</div>', unsafe_allow_html=True)
    answer = st.text_input("Votre réponse :")
    if st.button("Valider la mission 1"):
        if answer.lower().strip() in ["archipel", "sud"]:
            st.success("✅ Bonne réponse !")
            score += 30
            current_mission = 2
            hint = get_hint(current_mission, score)
            update_progress(team_name, current_mission, score, hint)
        else:
            st.error("❌ Réponse incorrecte. Essayez encore !")

elif current_mission == 2:
    st.markdown('<div class="mission-box"><b>Objectif :</b> Trouver la corrélation entre CO₂ et énergies renouvelables.</div>', unsafe_allow_html=True)
    answer = st.text_input("Décrivez la relation observée :")
    if st.button("Valider la mission 2"):
        if "inverse" in answer.lower() or "baisse" in answer.lower():
            st.success("✅ Exact ! Plus de renouvelables = moins de CO₂.")
            score += 25
            current_mission = 3
            hint = get_hint(current_mission, score)
            update_progress(team_name, current_mission, score, hint)
        else:
            st.warning("Pas tout à fait. Cherchez encore la tendance.")

elif current_mission == 3:
    st.markdown('<div class="mission-box"><b>Objectif :</b> Déterminer quand l'anomalie thermique dépasse 2°C.</div>', unsafe_allow_html=True)
    year = st.number_input("Entrez l'année :", min_value=2030, max_value=2050, step=1)
    if st.button("Valider la mission 3"):
        if year == 2045:
            st.success("🌡️ Bonne analyse !")
            score += 25
            current_mission = 4
            hint = get_hint(current_mission, score)
            update_progress(team_name, current_mission, score, hint)
        else:
            st.error("Essayez une autre année proche de la fin de la période.")

elif current_mission == 4:
    st.markdown('<div class="mission-box"><b>Objectif :</b> Proposez une mesure pour stabiliser Gaïa d'ici 2050.</div>', unsafe_allow_html=True)
    proposal = st.text_area("Votre plan de sauvetage :")
    if st.button("Soumettre le plan final"):
        if len(proposal) > 30:
            st.success("🌎 Bravo ! Votre plan est enregistré.")
            score += 40
            hint = "🏆 Mission terminée – Gaïa est sauvée grâce à vous !"
            update_progress(team_name, current_mission, score, hint)
        else:
            st.warning("Ajoutez un peu plus de détails à votre plan.")

# -------------------------------
# AFFICHAGE DES INDICES
# -------------------------------
df = load_progress()
team_data = df[df["Team"] == team_name]
if not team_data.empty:
    st.markdown(f'<div class="hint"><b>Indice actuel :</b> {team_data["Hint"].values[0]}</div>', unsafe_allow_html=True)

# -------------------------------
# SCORE FINAL
# -------------------------------
st.markdown("---")
st.info(f"🌿 Score actuel : **{score} points**")
st.caption("Les données de progression sont sauvegardées automatiquement.")
