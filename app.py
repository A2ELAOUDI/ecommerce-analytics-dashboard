"""
Dashboard E-commerce Analytics
Application Streamlit pour visualiser les données de ventes
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
sys.path.append('src')
from analysis import *

# Configuration de la page
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_all_data():
    """Charge toutes les données avec mise en cache"""
    transactions, customers = load_data()
    return transactions, customers

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 E-commerce Analytics Dashboard</h1>', unsafe_allow_html=True)

    # Chargement des données
    try:
        transactions, customers = load_all_data()
    except FileNotFoundError:
        st.error("❌ Fichiers de données introuvables. Veuillez exécuter 'python src/generate_data.py' d'abord.")
        return

    # Sidebar - Filtres
    st.sidebar.header("🔍 Filtres")

    # Filtre par date
    min_date = transactions['date'].min()
    max_date = transactions['date'].max()

    date_range = st.sidebar.date_input(
        "Période",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Filtre par catégorie
    categories = ['Toutes'] + sorted(transactions['category'].unique().tolist())
    selected_category = st.sidebar.selectbox("Catégorie", categories)

    # Filtre par région
    regions = ['Toutes'] + sorted(transactions['region'].unique().tolist())
    selected_region = st.sidebar.selectbox("Région", regions)

    # Filtrage des données
    filtered_df = transactions.copy()

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df['date'] >= pd.Timestamp(start_date)) &
            (filtered_df['date'] <= pd.Timestamp(end_date))
        ]

    if selected_category != 'Toutes':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]

    if selected_region != 'Toutes':
        filtered_df = filtered_df[filtered_df['region'] == selected_region]

    # KPIs principaux
    st.header("📈 KPIs Principaux")

    kpis = calculate_kpis(filtered_df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Chiffre d'Affaires",
            f"{kpis['total_revenue']:,.0f} €",
            help="Revenu total des transactions complétées"
        )

    with col2:
        st.metric(
            "🛒 Transactions",
            f"{kpis['total_transactions']:,}",
            help="Nombre total de transactions complétées"
        )

    with col3:
        st.metric(
            "📦 Panier Moyen",
            f"{kpis['avg_order_value']:.2f} €",
            help="Valeur moyenne d'une commande"
        )

    with col4:
        st.metric(
            "👥 Clients",
            f"{kpis['total_customers']:,}",
            help="Nombre de clients uniques"
        )

    col5, col6 = st.columns(2)

    with col5:
        st.metric(
            "📊 Produits Vendus",
            f"{kpis['total_products_sold']:,}",
            help="Nombre total d'unités vendues"
        )

    with col6:
        st.metric(
            "✅ Taux de Conversion",
            f"{kpis['conversion_rate']:.1f}%",
            help="Pourcentage de transactions complétées"
        )

    # Séparateur
    st.markdown("---")

    # Graphiques - Ligne 1
    st.header("📊 Analyses des Ventes")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ventes par Catégorie")
        cat_data = sales_by_category(filtered_df)

        fig_cat = px.pie(
            cat_data,
            values='revenue',
            names='category',
            title='Répartition du CA par Catégorie',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_cat.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_cat, use_container_width=True)

        # Tableau détaillé
        st.dataframe(
            cat_data.style.format({
                'revenue': '{:,.2f} €',
                'transactions': '{:,}',
                'units_sold': '{:,}'
            }),
            hide_index=True,
            use_container_width=True
        )

    with col2:
        st.subheader("Ventes par Région")
        region_data = sales_by_region(filtered_df)

        fig_region = px.bar(
            region_data,
            x='region',
            y='revenue',
            title='Chiffre d\'Affaires par Région',
            color='revenue',
            color_continuous_scale='Blues'
        )
        fig_region.update_layout(showlegend=False)
        st.plotly_chart(fig_region, use_container_width=True)

        # Tableau détaillé
        st.dataframe(
            region_data.style.format({
                'revenue': '{:,.2f} €',
                'transactions': '{:,}'
            }),
            hide_index=True,
            use_container_width=True
        )

    # Graphiques - Ligne 2
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Évolution des Ventes dans le Temps")

        # Sélection de la granularité
        time_freq = st.radio(
            "Granularité",
            ['Jour', 'Semaine', 'Mois'],
            horizontal=True,
            index=2
        )

        freq_map = {'Jour': 'D', 'Semaine': 'W', 'Mois': 'M'}
        time_data = sales_over_time(filtered_df, freq=freq_map[time_freq])

        fig_time = go.Figure()

        fig_time.add_trace(go.Scatter(
            x=time_data['date'],
            y=time_data['revenue'],
            mode='lines+markers',
            name='Revenus',
            line=dict(color='#1f77b4', width=3),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))

        fig_time.update_layout(
            title=f'Évolution du CA ({time_freq})',
            xaxis_title='Date',
            yaxis_title='Revenus (€)',
            hovermode='x unified'
        )

        st.plotly_chart(fig_time, use_container_width=True)

    with col2:
        st.subheader("Moyens de Paiement")
        payment_data = payment_method_analysis(filtered_df)

        fig_payment = px.bar(
            payment_data,
            x='payment_method',
            y='transactions',
            title='Transactions par Moyen de Paiement',
            color='payment_method',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_payment.update_layout(showlegend=False)
        st.plotly_chart(fig_payment, use_container_width=True)

        st.dataframe(
            payment_data[['payment_method', 'percentage']].style.format({
                'percentage': '{:.1f}%'
            }),
            hide_index=True,
            use_container_width=True
        )

    # Top Produits
    st.markdown("---")
    st.header("🏆 Top Produits")

    n_products = st.slider("Nombre de produits à afficher", 5, 20, 10)
    top_prod = top_products(filtered_df, n=n_products)

    fig_products = px.bar(
        top_prod,
        x='revenue',
        y='product',
        orientation='h',
        title=f'Top {n_products} Produits par CA',
        color='category',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_products.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_products, use_container_width=True)

    # Tableau détaillé
    st.dataframe(
        top_prod.style.format({
            'revenue': '{:,.2f} €',
            'units_sold': '{:,}',
            'orders': '{:,}'
        }),
        hide_index=True,
        use_container_width=True
    )

    # Analyse Clients
    st.markdown("---")
    st.header("👥 Analyse Clients")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Segments Clients")
        segment_data = customer_segments_analysis(customers)

        st.dataframe(
            segment_data.style.format({
                'nb_customers': '{:,}',
                'total_revenue': '{:,.2f} €',
                'avg_spent': '{:,.2f} €',
                'avg_purchases': '{:.1f}'
            }),
            hide_index=True,
            use_container_width=True
        )

    with col2:
        st.subheader("Distribution des Clients par Segment")

        fig_segments = px.sunburst(
            segment_data,
            path=['segment'],
            values='nb_customers',
            color='avg_spent',
            color_continuous_scale='RdYlGn',
            title='Répartition et Valeur des Segments'
        )
        st.plotly_chart(fig_segments, use_container_width=True)

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 2rem;'>
            <p>📊 Dashboard E-commerce Analytics | Projet Data Analysis</p>
            <p>Données générées pour démonstration | © 2025</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
