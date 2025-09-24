import pandas as pd
import streamlit as st

def RunApp(df):
    # --- Chargement et nettoyage des données ---
    df.columns = ["Role", "Map", "Elo", "Agent", "Win%", "Pick%", "Score"]

    # Supprimer les préfixes (ex: "Role: controller" -> "controller")
    for col in df.columns:
        df[col] = df[col].apply(lambda x: x.split(": ")[1] if ": " in x else x)

    # Conversion en float
    for col in ["Win%", "Pick%", "Score"]:
        df[col] = df[col].astype(float)

    # --- Interface Streamlit ---
    st.title("📊 Analyse des meilleurs agents Valorant")

    # Filtres utilisateur
    maps = ["All"] + sorted(df["Map"].unique())
    elos = sorted(df["Elo"].unique())

    map_choice = st.selectbox("Choisir une map :", maps)
    elo_choice = st.selectbox("Choisir une fourchette de rang (Elo) :", elos)
    top_n = st.slider("Nombre de meilleurs agents à afficher :", 1, 5, 3)

    # Filtrage dynamique
    filtered = df.copy()
    if map_choice != "All":
        filtered = filtered[filtered["Map"] == map_choice]

    if elo_choice:
        filtered = filtered[filtered["Elo"] == elo_choice]

    # Tri et sélection
    best_agents = filtered.sort_values("Score", ascending=False).head(top_n)

    # --- Affichage ---
    st.subheader(f"Top {top_n} agents sur {map_choice} ({elo_choice})")
    st.dataframe(best_agents)

    # Graphique
    st.bar_chart(best_agents.set_index("Agent")["Score"])