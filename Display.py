import pandas as pd
import streamlit as st
import numpy as np

def ShowAgentWinrate():
    df_agents = pd.read_csv("Dataset/valo_agents_stat.csv")

    # Nettoyer la colonne 'Win %' et convertir en float
    df_agents['Win %'] = df_agents['Win %'].str.replace('%', '', regex=False)
    df_agents['Win %'] = pd.to_numeric(df_agents['Win %'], errors='coerce')

    # Sélection d'un agent
    agent_selected = st.selectbox("Choisir un agent pour %Winrate :", df_agents['Name'].unique())
    agent_df = df_agents[df_agents['Name'] == agent_selected]

    # Définir l'ordre des ranks
    rank_order = [
        "Unrated",
        "Iron 1", "Iron 2", "Iron 3",
        "Bronze 1", "Bronze 2", "Bronze 3",
        "Silver 1", "Silver 2", "Silver 3",
        "Gold 1", "Gold 2", "Gold 3",
        "Platinum 1", "Platinum 2", "Platinum 3",
        "Diamond 1", "Diamond 2", "Diamond 3",
        "Ascendant 1", "Ascendant 2", "Ascendant 3",
        "Immortal 1", "Immortal 2", "Immortal 3",
        "Radiant"
    ]
    

    # Calcul du %Winrate par Game Rank et Map
    winrate_rank = agent_df.groupby('Game Rank')['Win %'].mean()
    winrate_rank = winrate_rank.reindex(rank_order)  # Réordonner selon rank_order
    # Renommer les clés selon rank_order (en supprimant le préfixe)
    winrate_rank.index = ["\u200B" * i + rank_order[i] for i, rank in enumerate(winrate_rank.index)]
    print(winrate_rank)

    winrate_map  = agent_df.groupby('Map')['Win %'].mean()

    # Affichage des graphiques
    st.line_chart(winrate_rank)
    st.bar_chart(winrate_map)

def RunApp(best_agents: pd.DataFrame):
    st.title("Valorant – Meilleurs agents par rôle, map et elo")
    st.set_page_config(layout="wide")

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