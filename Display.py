import pandas as pd
import streamlit as st

def ShowAgentWinrate():
    df_agents = pd.read_csv("Dataset/valo_agents_stat.csv")

    # Nettoyer la colonne 'Win %' et convertir en float
    df_agents['Win %'] = df_agents['Win %'].str.replace('%', '', regex=False)
    df_agents['Win %'] = pd.to_numeric(df_agents['Win %'], errors='coerce')

    # Sélection d'un agent
    agent_selected = st.selectbox("Choisir un agent pour %Winrate :", df_agents['Name'].unique())
    agent_df = df_agents[df_agents['Name'] == agent_selected]

    # Calcul du %Winrate par Game Rank et Map
    winrate_rank = agent_df.groupby('Game Rank')['Win %'].mean()
    winrate_map  = agent_df.groupby('Map')['Win %'].mean()

    # Affichage des graphiques
    st.line_chart(winrate_rank)
    st.bar_chart(winrate_map)

def RunApp(best_agents: pd.DataFrame):
    st.title("Valorant – Meilleurs agents par rôle, map et elo")

    # Préparer les colonnes
    df = best_agents[["Role", "Map", "Elo", "Name", "Win %", "Pick %", "Score"]].copy()
    df.columns = ["Role", "Map", "Elo", "Agent", "Win%", "Pick%", "Score"]

    # Filtres
    role_filter = st.selectbox("Filtrer par rôle", ["Tous"] + sorted(df["Role"].unique().tolist()))
    map_filter = st.selectbox("Filtrer par map", ["Toutes"] + sorted(df["Map"].unique().tolist()))
    elo_filter = st.selectbox("Filtrer par elo", ["Tous"] + sorted(df["Elo"].unique().tolist()))

    filtered_df = df.copy()
    if role_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Role"] == role_filter]
    if map_filter != "Toutes":
        filtered_df = filtered_df[filtered_df["Map"] == map_filter]
    if elo_filter != "Tous":
        filtered_df = filtered_df[filtered_df["Elo"] == elo_filter]

    st.dataframe(filtered_df, use_container_width=True)

    ShowAgentWinrate()