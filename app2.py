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

    # Sélectionner les visualisations et statistiques à afficher
    st.sidebar.header("Sélectionnez les Visualisations et Statistiques")
    show_heatmap = st.sidebar.checkbox("Afficher la Heatmap", value=True)
    show_barplot = st.sidebar.checkbox("Afficher le Bar Plot Empilé", value=True)
    show_treemap = st.sidebar.checkbox("Afficher le Treemap", value=True)
    show_global_stats = st.sidebar.checkbox("Afficher les Statistiques Globales", value=True)
    show_product_stats = st.sidebar.checkbox("Afficher les Statistiques par Produit", value=True)
    show_site_stats = st.sidebar.checkbox("Afficher les Statistiques par Magasin", value=True)
    show_chain_stats = st.sidebar.checkbox("Afficher les Statistiques par Chaîne", value=True)

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

    # 4. Statistiques Descriptives
    if show_global_stats:
        descriptive_stats = df_combined['rupture'].describe()
        st.subheader("Statistiques Globales des Ruptures")
        st.write(descriptive_stats)

    if show_product_stats:
        product_stats = df_combined.groupby('PRODUCT_ID')['rupture'].describe()
        st.subheader("Statistiques Descriptives par Produit")
        st.write(product_stats)

    # if show_site_stats:
    #     site_stats = df_combined.groupby('SITE_ID')['rupture'].describe()
    #     st.subheader("Statistiques Descriptives par Magasin (SITE_ID)")
    #     st.write(site_stats)

    # if show_chain_stats:
    #     chain_stats = df_combined.groupby('chain_code')['rupture'].describe()
    #     st.subheader("Statistiques Descriptives par Chaîne (chain_code)")
    #     st.write(chain_stats)

    # 5. Moyenne des Ruptures par Produit
    # mean_rupture_product = df_combined.groupby('PRODUCT_ID')['rupture'].mean().reset_index()
    # st.subheader("Moyenne des Ruptures par Produit")
    # bar_plot_mean = px.bar(mean_rupture_product, x='PRODUCT_ID', y='rupture', title="Moyenne des Ruptures par Produit")
    # st.plotly_chart(bar_plot_mean)
    # 5. Moyenne des Ruptures par Produit
    mean_rupture_product = df_combined.groupby('PRODUCT_ID')['rupture'].mean().reset_index()
    mean_rupture_product['PRODUCT_ID'] = mean_rupture_product['PRODUCT_ID'].astype(str)

    st.subheader("Moyenne des Ruptures par Produit")
    bar_plot_mean = px.bar(mean_rupture_product, x='PRODUCT_ID', y='rupture', title="Moyenne des Ruptures par Produit")
    bar_plot_mean.update_layout(
        xaxis_tickangle=-90  # Rotation des étiquettes sur l'axe X pour une meilleure lisibilité
    )

    st.plotly_chart(bar_plot_mean)

    # 6. Moyenne des Ruptures par Magasin
    mean_rupture_site = df_combined.groupby('SITE_ID')['rupture'].mean().reset_index()
    mean_rupture_site['SITE_ID'] = mean_rupture_site['SITE_ID'].astype(str)

    st.subheader("Moyenne des Ruptures par Magasin")
    bar_plot_mean_site = px.bar(
        mean_rupture_site, 
        x='SITE_ID', 
        y='rupture', 
        title="Moyenne des Ruptures par Magasin"
    )

    # Ajustements pour améliorer la lisibilité de l'axe des abscisses
    bar_plot_mean_site.update_layout(
        xaxis=dict(
            title='Magasin (SITE_ID)',
            tickmode='linear',  # Afficher chaque magasin individuellement
            tickangle=-90,  # Rotation des étiquettes à 90 degrés pour une meilleure lisibilité
            tickfont=dict(size=8)  # Réduire encore plus la taille de la police des étiquettes
        ),
        height=600,  # Ajuster la hauteur pour accueillir plus de magasins
        width=1200,  # Augmenter significativement la largeur du graphique
        margin=dict(l=40, r=40, t=40, b=200)  # Marges supplémentaires en bas pour éviter le chevauchement des étiquettes
    )

    # Afficher le graphique
    st.plotly_chart(bar_plot_mean_site)

    # 7. Produits avec le Plus Grand Nombre de Ruptures
    total_rupture_product = df_combined.groupby('PRODUCT_ID')['rupture'].sum().reset_index().sort_values(by='rupture', ascending=False)
    st.subheader("Produits avec le Plus Grand Nombre de Ruptures")
    st.write(total_rupture_product.head(10))  # Afficher les 10 produits avec le plus de ruptures

else:
    st.write("Veuillez télécharger un fichier Excel pour commencer l'analyse.")
