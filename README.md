# Opération Sauver Gaïa

Application Streamlit multi‑page pour un escape game pédagogique.

## Lancer en local

```bash
# Depuis le dossier du projet
pip install -r requirements.txt
streamlit run gaia_streamlit_app.py
```

Variables d'environnement optionnelles:
- `GAIA_DATASET_PATH` chemin du CSV (par défaut `better_gaia_dataset.csv`).
- `GAIA_PROGRESS_PATH` chemin du fichier de progression (par défaut `progress.csv`).

## Structure
- `gaia_streamlit_app.py` page principale (tableau de bord données).
- `gaia_team_app.py` espace Équipe (progression missions).
- `gaia_admin_dashboard.py` tableau de bord Admin.
- `better_gaia_dataset.csv` données d'exemple.
- `progress.csv` état des équipes.

## Déploiement (Streamlit Cloud)
1. Pousser ce dépôt sur GitHub.
2. Sur Streamlit Cloud, créer une app en pointant sur `gaia_streamlit_app.py`.
3. Définir les secrets/variables si nécessaire:
   - `GAIA_DATASET_PATH=better_gaia_dataset.csv`
   - `GAIA_PROGRESS_PATH=progress.csv`
4. Activer Always On si désiré.

## Déploiement (Railway/Render)
- Configurer un service Web avec la commande `streamlit run gaia_streamlit_app.py --server.port $PORT --server.address 0.0.0.0`.
- Ajouter `PORT` fourni par la plateforme.

## Licence
Projet éducatif.
