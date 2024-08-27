import streamlit as st
import pandas as pd
import plotly.express as px

# Titre de l'application
st.title("Analyse des Ruptures de Stock par Chaîne et Magasin")

# Étape 1: Charger le fichier Excel
uploaded_file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx"])

if uploaded_file is not None:
    # Lire le fichier Excel
    df_combined = pd.read_excel(uploaded_file)

    # Afficher un aperçu du dataframe
    st.write("Aperçu des données :", df_combined.head())

    # Agréger les données pour les visualisations
    agg_df = df_combined.groupby(['PRODUCT_ID', 'SITE_ID', 'MONTH', 'chain_code'], as_index=False)['rupture'].sum()

    # Sélectionner les visualisations à afficher
    st.sidebar.header("Sélectionnez les visualisations")
    show_heatmap = st.sidebar.checkbox("Afficher la Heatmap", value=True)
    show_barplot = st.sidebar.checkbox("Afficher le Bar Plot Empilé", value=True)
    show_treemap = st.sidebar.checkbox("Afficher le Treemap", value=True)

    # 1. Heatmap
    if show_heatmap:
        st.subheader("Heatmap des ruptures par mois, magasin et chaîne")
        heatmap = px.density_heatmap(
            agg_df, 
            x='MONTH', 
            y='SITE_ID', 
            z='rupture', 
            facet_col='PRODUCT_ID', 
            facet_row='chain_code',  # Ajout de `chain_code` comme facette supplémentaire
            color_continuous_scale='Viridis'
        )

        heatmap.update_layout(
            title_font_size=16,  # Taille du titre principal
            title_x=0.5,  # Centrer le titre
            xaxis_tickangle=-45,  # Tourner les étiquettes de l'axe X
            margin=dict(t=50, l=50, b=150, r=50),  # Ajuster les marges
            xaxis=dict(
                title='Mois',
                title_font_size=8,  # Taille du titre de l'axe X réduite à 8
                tickfont_size=8  # Taille des étiquettes des ticks de l'axe X réduite à 8
            ),
            yaxis=dict(
                title='SITE_ID',
                title_font_size=8,  # Taille du titre de l'axe Y réduite à 8
                tickfont_size=8  # Taille des étiquettes des ticks de l'axe Y réduite à 8
            ),
            height=800,  # Ajuster la hauteur du graphique pour accueillir les facettes supplémentaires
            font=dict(
                size=10  # Taille générale du texte (incluant les titres des facettes)
            )
        )

        heatmap.for_each_annotation(lambda a: a.update(font=dict(size=10)))

        st.plotly_chart(heatmap)

    # 2. Bar Plot Empilé
    if show_barplot:
        st.subheader("Ruptures de stock par mois, magasin, produit et chaîne")
        bar_plot = px.bar(
            agg_df, 
            x='MONTH', 
            y='rupture', 
            color='SITE_ID', 
            facet_col='PRODUCT_ID',
            facet_row='chain_code',  # Ajout de `chain_code` comme facette supplémentaire
            barmode='stack'
        )

        bar_plot.update_layout(
            title_font_size=16,  # Taille du titre principal
            title_x=0.5,  # Centrer le titre
            xaxis_tickangle=-45,  # Tourner les étiquettes de l'axe X
            margin=dict(t=50, l=50, b=150, r=50),  # Ajuster les marges
            xaxis=dict(
                title='Mois',
                title_font_size=8,  # Taille du titre de l'axe X réduite à 8
                tickfont_size=8  # Taille des étiquettes des ticks de l'axe X réduite à 8
            ),
            yaxis=dict(
                title='Nombre de ruptures',
                title_font_size=8,  # Taille du titre de l'axe Y réduite à 8
                tickfont_size=8  # Taille des étiquettes des ticks de l'axe Y réduite à 8
            ),
            height=800,  # Ajuster la hauteur du graphique pour accueillir les facettes supplémentaires
            font=dict(
                size=10  # Taille générale du texte (incluant les titres des facettes)
            )
        )

        bar_plot.for_each_annotation(lambda a: a.update(font=dict(size=10)))

        st.plotly_chart(bar_plot)

    # 3. Treemap
    if show_treemap:
        st.subheader("Treemap des ruptures de stock par chaîne, produit, et magasin")
        treemap = px.treemap(
            df_combined, 
            path=['chain_code', 'PRODUCT_ID', 'SITE_ID', 'MONTH'], 
            values='rupture'
        )

        treemap.update_layout(
            title_font_size=16,  # Taille du titre principal
            font=dict(
                size=10  # Taille générale du texte
            )
        )

        st.plotly_chart(treemap)

else:
    st.write("Veuillez télécharger un fichier Excel pour commencer l'analyse.")
