import streamlit as st
import pandas as pd
import altair as alt
import os

# === CONFIGURATION GÉNÉRALE ===
st.set_page_config(
    page_title="Opération Sauver Gaïa",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === STYLES PERSONNALISÉS ===
st.markdown("""
<style>
    body {
        background-color: #f7fcf9;
    }
    .main-header {
        font-size: 2.8em;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-style: italic;
        margin-bottom: 40px;
    }
    .metric-card {
        background-color: #ecf9f1;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2E8B57;
        margin: 10px 0;
        text-align: center;
    }
    .sidebar-header {
        font-size: 1.2em;
        font-weight: bold;
        color: #2E8B57;
    }
    .footer {
        text-align: center;
        font-style: italic;
        color: #666;
        margin-top: 60px;
    }
</style>
""", unsafe_allow_html=True)

# === CHARGEMENT DES DONNÉES ===
@st.cache_data
def load_data():
    data_path = os.getenv("GAIA_DATASET_PATH", "better_gaia_dataset.csv")
    return pd.read_csv(data_path)

df = load_data()

# === MENU DE NAVIGATION ===
st.sidebar.markdown('<p class="sidebar-header">🧭 Navigation</p>', unsafe_allow_html=True)

# Boutons de navigation
if st.sidebar.button("🏠 Accueil - Tableau de bord", key="home"):
    st.session_state.page = "home"
if st.sidebar.button("🎮 Espace Équipe", key="team"):
    st.session_state.page = "team"

# Initialiser la page si pas définie
if "page" not in st.session_state:
    st.session_state.page = "home"

# === LOGIQUE DE NAVIGATION ===
if st.session_state.page == "home":
    # === BARRE LATÉRALE FILTRES ===
    st.sidebar.markdown("---")
    st.sidebar.markdown('<p class="sidebar-header">🎛️ Filtres</p>', unsafe_allow_html=True)
    regions = df["Region"].unique().tolist()
    selected_regions = st.sidebar.multiselect("Choisir les régions :", regions, default=regions)
    years = sorted(df["Year"].unique())
    year_range = st.sidebar.slider("Période :", min_value=int(min(years)), max_value=int(max(years)), value=(2030,2050))

    filtered_df = df[(df["Region"].isin(selected_regions)) & (df["Year"].between(year_range[0], year_range[1]))]

    # === EN-TÊTE ===
    st.markdown('<h1 class="main-header">🌍 Opération Sauver Gaïa</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Tableau de bord environnemental interactif (2030–2050)</p>', unsafe_allow_html=True)

    # === INDICATEURS CLÉS ===
    st.subheader("📊 Indicateurs globaux")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'<div class="metric-card"><b>CO₂ Moyen</b><br>{filtered_df["CO2_ppm"].mean():.1f} ppm</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><b>Température Moy.</b><br>{filtered_df["Temp_anomaly_C"].mean():.2f} °C</div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><b>Déforestation Moy.</b><br>{filtered_df["Deforestation_pct"].mean():.1f}%</div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><b>Vulnérabilité Moy.</b><br>{filtered_df["Vulnerability_index_0_100"].mean():.1f}/100</div>', unsafe_allow_html=True)

    # === TÉLÉCHARGEMENT ===
    csv = filtered_df.to_csv(index=False)
    st.download_button("📥 Télécharger les données filtrées (CSV)", csv, "gaia_data_filtered.csv", "text/csv")

    # === ONGLET VISUALISATIONS ===
    tab1, tab2, tab3 = st.tabs(["🌫️ Climat", "🌲 Écologie", "⚡ Énergie & Vulnérabilité"])

    with tab1:
        st.subheader("Évolution du CO₂ (ppm)")
        co2_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
            x="Year:O", y="CO2_ppm:Q", color="Region:N",
            tooltip=["Region", "Year", "CO2_ppm"]
        ).properties(width="container", height=400)
        st.altair_chart(co2_chart, use_container_width=True)

        st.subheader("Anomalie de température (°C)")
        temp_chart = alt.Chart(filtered_df).mark_area(opacity=0.5).encode(
            x="Year:O", y="Temp_anomaly_C:Q", color="Region:N"
        ).properties(width="container", height=350)
        st.altair_chart(temp_chart, use_container_width=True)

    with tab2:
        st.subheader("Déforestation (%)")
        def_chart = alt.Chart(filtered_df).mark_bar().encode(
            x="Year:O", y="Deforestation_pct:Q", color="Region:N",
            tooltip=["Region", "Year", "Deforestation_pct"]
        ).properties(width="container", height=400)
        st.altair_chart(def_chart, use_container_width=True)

        st.subheader("Niveau moyen de la mer (cm)")
        sea_chart = alt.Chart(filtered_df).mark_line().encode(
            x="Year:O", y="SeaLevel_cm:Q", color="Region:N"
        ).properties(width="container", height=350)
        st.altair_chart(sea_chart, use_container_width=True)

    with tab3:
        st.subheader("Part des énergies renouvelables (%)")
        renew_chart = alt.Chart(filtered_df).mark_area(opacity=0.6).encode(
            x="Year:O", y="Renewable_share_pct:Q", color="Region:N"
        ).properties(width="container", height=350)
        st.altair_chart(renew_chart, use_container_width=True)

        st.subheader("Corrélation : Énergies renouvelables vs Vulnérabilité")
        scatter = alt.Chart(filtered_df).mark_circle(size=90, opacity=0.7).encode(
            x="Renewable_share_pct:Q",
            y="Vulnerability_index_0_100:Q",
            color="Region:N",
            tooltip=["Region", "Year", "Renewable_share_pct", "Vulnerability_index_0_100"]
        ).properties(width="container", height=400)
        st.altair_chart(scatter, use_container_width=True)

elif st.session_state.page == "team":
    # === PAGE ÉQUIPE ===
    st.markdown('<h1 class="main-header">🎮 Espace Équipe</h1>', unsafe_allow_html=True)
    
    # Import des fonctions de l'app équipe
    import datetime
    
    progress_file = os.getenv("GAIA_PROGRESS_PATH", "progress.csv")
    
    if not os.path.exists(progress_file):
        df_init = pd.DataFrame(columns=["Team", "Mission", "Score", "Hint", "Last_Update"])
        df_init.to_csv(progress_file, index=False)
    
    def load_progress():
        return pd.read_csv(progress_file)
    
    def save_progress(df):
        df.to_csv(progress_file, index=False)
    
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
    
    # Interface équipe
    team_name = st.text_input("🧭 Entrez le nom de votre équipe :").strip()
    if team_name:
        st.success(f"Bienvenue, **{team_name}** ! 🌿")
        progress = load_progress()
        
        if team_name in progress["Team"].values:
            current_mission = int(progress.loc[progress["Team"] == team_name, "Mission"].values[0])
            score = int(progress.loc[progress["Team"] == team_name, "Score"].values[0])
        else:
            current_mission = 1
            score = 0
            update_progress(team_name, current_mission, score, "")
        
        st.header(f"🚀 Mission {current_mission}")
        
        if current_mission == 1:
            st.info("**Objectif :** Identifier la région la plus vulnérable en 2050.")
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
            st.info("**Objectif :** Trouver la corrélation entre CO₂ et énergies renouvelables.")
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
            st.info("**Objectif :** Déterminer quand l'anomalie thermique dépasse 2 degrés Celsius.")
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
            st.info("**Objectif :** Proposez une mesure pour stabiliser Gaïa d'ici 2050.")
            proposal = st.text_area("Votre plan de sauvetage :")
            if st.button("Soumettre le plan final"):
                if len(proposal) > 30:
                    st.success("🌎 Bravo ! Votre plan est enregistré.")
                    score += 40
                    hint = "🏆 Mission terminée – Gaïa est sauvée grâce à vous !"
                    update_progress(team_name, current_mission, score, hint)
                else:
                    st.warning("Ajoutez un peu plus de détails à votre plan.")
        
        # Affichage des indices
        df_progress = load_progress()
        team_data = df_progress[df_progress["Team"] == team_name]
        if not team_data.empty:
            st.info(f"**Indice actuel :** {team_data['Hint'].values[0]}")
        
        st.markdown("---")
        st.info(f"🌿 Score actuel : **{score} points**")

# === PIED DE PAGE ===
st.markdown('<div class="footer">🌱 Données fictives pour l\'Escape Game pédagogique <b>"Sauver Gaïa"</b> – 2025<br>"Les données racontent l\'avenir, à vous de l\'écrire."</div>', unsafe_allow_html=True)
