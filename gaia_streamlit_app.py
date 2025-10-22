import streamlit as st
import pandas as pd
import altair as alt
import os

# === CONFIGURATION GÉNÉRALE ===
st.set_page_config(
    page_title="Opération Sauver Gaïa",
    page_icon="🌍",
    layout="wide"
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

# === BARRE LATÉRALE ===
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

# === PIED DE PAGE ===
st.markdown('<div class="footer">🌱 Données fictives pour l'Escape Game pédagogique <b>"Sauver Gaïa"</b> – 2025<br>"Les données racontent l'avenir, à vous de l'écrire."</div>', unsafe_allow_html=True)
