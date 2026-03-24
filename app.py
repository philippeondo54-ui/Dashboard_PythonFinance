import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Transactions",
    layout="wide",
)
st.header(":blue[Tableau de bord des transactions]", divider="rainbow")

# Fonction de chargement des données avec cache
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

# Charger directement ton fichier transactions_cleaned.csv
df = load_data("transactions_cleaned.csv")

# Préparation des colonnes
df["Diff"] = df["Value"] - df["AmountAbs"]

# Sidebar options
st.sidebar.subheader("Options")
show_data = st.sidebar.checkbox("Afficher les données brutes")
if show_data:
    st.dataframe(df, use_container_width=True)

# Tabs
tabs = st.tabs(["Vue d’ensemble", "Par stratégie de pricing", "Fraudes", "Catégories de produits", ])

# Vue d’ensemble
with tabs[0]:

    st.subheader("Salut, bienvenue sur le dashboard de Philippe Ondo")
    col1, col2,col3, col4 = st.columns(4)
    with col1:
        st.metric("Total transactions", len(df))
    with col2:
        st.metric("Total fraudes", df["FraudResult"].sum())
    with col3:
        st.metric("Total produits existants", df["ProductId"].nunique())
    with col4:
        st.metric("Jour le plus actif", df["Transaction Day"].max())

    st.subheader("Évolution des montants par date")
    # Agréger les montants par date
    daily_amounts = df.groupby("Transaction Date")["Amount"].sum().reset_index()

    fig = px.line(daily_amounts, x="Transaction Date", y="Amount",
                title="Montants totaux des transactions par jour")
    st.plotly_chart(fig, use_container_width=True)

    fig = px.scatter(df, x="Transaction Date", y="Amount", color="ProductCategory")
    st.plotly_chart(fig, use_container_width=True)


    st.subheader("Fréquence des transactions par jour")
    counts = df["Transaction Day"].value_counts().reset_index()
    counts.columns = ["Transaction Day", "Total"]
    fig = px.bar(counts, x="Transaction Day", y="Total", color="Transaction Day",
    title="Fréquence des transactions par jour")
    st.plotly_chart(fig, use_container_width=True)

    # Histogramme des produits par jour
    fig = px.histogram(df, x="Transaction Day", color="ProductCategory")
    st.plotly_chart(fig, use_container_width=True)

    # Histogramme des canaux par jour
    fig = px.histogram(df, x="Transaction Day", color="ChannelId")
    st.plotly_chart(fig, use_container_width=True)

    counts = df.groupby("ChannelId")["ProductCategory"].size().reset_index(name="Total")

    # Camembert interactif
    fig = px.pie(counts, values="Total", names="ChannelId",
                title="Répartition des produits par ChannelId",
                hole=0) 
    st.plotly_chart(fig, use_container_width=True)





# Analyse par stratégie de pricing
with tabs[1]:

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Nombre de stratégies de prix", df["PricingStrategy"].count())
    with col2:
        st.metric("Stratégie de prix la plus prisee", df["PricingStrategy"].mode()[0])



    st.subheader("Répartition des montants par stratégie de pricing")
    fig = px.histogram(df, y="Amount", x="PricingStrategy", color="PricingStrategy")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Écarts par stratégie de pricing")
    fig = px.box(df, x="PricingStrategy", y="Diff", color="PricingStrategy",
                 title="Distribution des écarts par stratégie de pricing")
    fig.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig, use_container_width=True)

# Fraudes 
with tabs[2]:

    col1, col2,col3 = st.columns(3)
    with col1:
        st.metric("Nombre de fraudes", df["FraudResult"].sum())
    with col2:
        st.metric("Montant total des fraudes", df["Amount"][df["FraudResult"] == 1].sum())
    with col3:
        st.metric("Jour le plus fraudé", df["Transaction Day"][df["FraudResult"] == 1].max())

    st.subheader("Transactions individuelles dans le temps")
    fig = px.scatter(df, x="Transaction Date", y="Amount", color="FraudResult",
                    title="Transactions par jour (fraudes vs normales)",
                    hover_data=["ProductCategory","ChannelId"])
    st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("Répartition des fraudes par ChannelId")
    counts = df.groupby("ChannelId")["FraudResult"].size().reset_index(name="Total")
    fig = px.pie(counts, values="Total", names="ChannelId",
                 title="Répartition des fraudes par ChannelId")
    st.plotly_chart(fig, use_container_width=True)

    # Histogramme des fraudes par 
    st.subheader("Histogramme des fraudes par catégorie de produit")

    fig = px.histogram(df, x="ProductCategory", y="FraudResult", color="ProductCategory")
    st.plotly_chart(fig, use_container_width=True)

    # Histogramme des fraudes par jour
    st.subheader("Histogramme des fraudes par jour")
    fig = px.histogram(df, x="Transaction Day", y="FraudResult", color="Transaction Day")
    st.plotly_chart(fig, use_container_width=True)



# Catégories de produits
with tabs[3]:

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Nombre de catégories de produits", df["ProductCategory"].nunique())
    with col2:
        st.metric("Categorie la plus importante", df["ProductCategory"].mode()[0])

    st.subheader("Répartition des montants par catégorie de produit")
    fig = px.histogram(df, x="ProductCategory", y="Amount", color="ProductCategory")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Répartition des stratégies de prix par produit")
    fig = px.histogram(df, x="ProductId", y="PricingStrategy", color="PricingStrategy")
    st.plotly_chart(fig, use_container_width=True)
