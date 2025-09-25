import pandas as pa

def get_best_agents(csv_path: str) -> pa.DataFrame:
    # Charger le CSV
    df = pa.read_csv("Dataset/valo_agents_stat.csv")
    
    # On ne garde que le mode compétitif
    df = df[df["Game Type"] == "Competitive"].copy()
    
    # Nettoyage colonnes
    df["Win %"] = df["Win %"].str.replace("%", "").astype(float)
    df["Pick %"] = df["Pick %"].str.replace("%", "").astype(float)
    
    # --- 1. Définir les fourchettes de rank ---
    def rank_to_elo(rank):
        if isinstance(rank, str):
            rank_lower = rank.lower()
            if any(x in rank_lower for x in ["iron", "bronze", "silver"]):
                return "Low"
            elif any(x in rank_lower for x in ["gold", "plat", "diamond"]):
                return "Mid"
            elif any(x in rank_lower for x in ["ascendant", "immortal", "radiant"]):
                return "High"
        return None
    
    df["Elo"] = df["Game Rank"].apply(rank_to_elo)
    
    # --- 2. Calcul d’un score combiné ---
    # Exemple : pondérer winrate et pickrate (tu peux ajuster les poids)
    df["Score"] = df["Win %"]
    
    # --- 3. Trouver le meilleur agent par Role + Map + Elo ---
    best_agents = (
        df.sort_values("Score", ascending=False)
          .groupby(["Role", "Map", "Elo"])
          .first()
          .reset_index()
    )
    
    # --- 4. Sauvegarder en .txt ---
    # with open("best_agents.txt", "w", encoding="utf-8") as f:
    #     for _, row in best_agents.iterrows():
    #         f.write(
    #             f"Role: {row['Role']}, Map: {row['Map']}, Elo: {row['Elo']}, "
    #             f"Agent: {row['Name']}, Win%: {row['Win %']}, "
    #             f"Pick%: {row['Pick %']}, Score: {row['Score']:.2f}\n"
    #         )

    print("Résultats sauvegardés dans best_agents.txt ✅")
    return best_agents