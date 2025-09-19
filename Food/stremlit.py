import streamlit as st
import pandas as pd


df = pd.read_csv("restaurants_paris_complet.csv")

st.title("Exemple d'interface Streamlit")
st.write("Voici quelques données affichées dans un tableau :")
st.set_page_config(layout="wide")
name = st.text_input("Entrez votre prénom :")
if name:
    st.write(f"Bonjour {name}")
print("Le code a été exécuté")
st.dataframe(df)