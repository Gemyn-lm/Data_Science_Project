import streamlit as st
import pandas as pd

# Exemple de données
data = {
    'Nom': ['Alice', 'Bob', 'Charlie', 'David'],
    'Âge': [25, 30, 35, 40],
    'Ville': ['Paris', 'Lyon', 'Marseille', 'Toulouse']
}
df = pd.read_csv("restaurants_paris.csv")

st.title("Exemple d'interface Streamlit")
st.write("Voici quelques données affichées dans un tableau :")

name = st.text_input("Entrez votre prénom :")
if name:
    st.write(f"Bonjour {name}")
print("Le code a été exécuté")
st.dataframe(df)