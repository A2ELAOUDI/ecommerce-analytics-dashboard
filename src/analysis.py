"""
Script d'analyse des données e-commerce
Contient les fonctions de calcul des KPIs et statistiques
"""
import pandas as pd
import numpy as np
from datetime import datetime

def load_data():
    """Charge les données depuis les fichiers CSV"""
    transactions = pd.read_csv('data/transactions.csv', parse_dates=['date'])
    customers = pd.read_csv('data/customers.csv', parse_dates=['first_purchase_date'])
    return transactions, customers

def calculate_kpis(df):
    """
    Calcule les KPIs principaux

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame des transactions

    Returns:
    --------
    dict
        Dictionnaire contenant les KPIs
    """
    # Filtrer seulement les transactions complétées
    completed = df[df['status'] == 'Complété']

    kpis = {
        'total_revenue': completed['total_amount'].sum(),
        'total_transactions': len(completed),
        'avg_order_value': completed['total_amount'].mean(),
        'total_customers': df['customer_id'].nunique(),
        'total_products_sold': completed['quantity'].sum(),
    }

    # Taux de conversion (non annulé)
    kpis['conversion_rate'] = (len(completed) / len(df)) * 100

    return kpis

def sales_by_category(df):
    """
    Analyse des ventes par catégorie

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame des transactions

    Returns:
    --------
    pd.DataFrame
        Ventes par catégorie
    """
    completed = df[df['status'] == 'Complété']

    category_stats = completed.groupby('category').agg({
        'total_amount': 'sum',
        'transaction_id': 'count',
        'quantity': 'sum'
    }).reset_index()

    category_stats.columns = ['category', 'revenue', 'transactions', 'units_sold']
    category_stats = category_stats.sort_values('revenue', ascending=False)

    return category_stats

def sales_by_region(df):
    """
    Analyse des ventes par région

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame des transactions

    Returns:
    --------
    pd.DataFrame
        Ventes par région
    """
    completed = df[df['status'] == 'Complété']

    region_stats = completed.groupby('region').agg({
        'total_amount': 'sum',
        'transaction_id': 'count'
    }).reset_index()

    region_stats.columns = ['region', 'revenue', 'transactions']
    region_stats = region_stats.sort_values('revenue', ascending=False)

    return region_stats

def sales_over_time(df, freq='M'):
    """
    Évolution des ventes dans le temps

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame des transactions
    freq : str
        Fréquence d'agrégation ('D', 'W', 'M', 'Y')

    Returns:
    --------
    pd.DataFrame
        Ventes par période
    """
    completed = df[df['status'] == 'Complété'].copy()
    completed['date'] = pd.to_datetime(completed['date'])

    time_series = completed.groupby(pd.Grouper(key='date', freq=freq)).agg({
        'total_amount': 'sum',
        'transaction_id': 'count'
    }).reset_index()

    time_series.columns = ['date', 'revenue', 'transactions']

    return time_series

def top_products(df, n=10):
    """
    Produits les plus vendus

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame des transactions
    n : int
        Nombre de produits à retourner

    Returns:
    --------
    pd.DataFrame
        Top produits
    """
    completed = df[df['status'] == 'Complété']

    product_stats = completed.groupby(['product', 'category']).agg({
        'total_amount': 'sum',
        'quantity': 'sum',
        'transaction_id': 'count'
    }).reset_index()

    product_stats.columns = ['product', 'category', 'revenue', 'units_sold', 'orders']
    product_stats = product_stats.sort_values('revenue', ascending=False).head(n)

    return product_stats

def customer_segments_analysis(customers_df):
    """
    Analyse des segments clients

    Parameters:
    -----------
    customers_df : pd.DataFrame
        DataFrame des clients

    Returns:
    --------
    pd.DataFrame
        Statistiques par segment
    """
    segment_stats = customers_df.groupby('segment').agg({
        'customer_id': 'count',
        'total_spent': ['sum', 'mean'],
        'total_purchases': 'mean'
    }).reset_index()

    segment_stats.columns = ['segment', 'nb_customers', 'total_revenue', 'avg_spent', 'avg_purchases']

    return segment_stats

def payment_method_analysis(df):
    """
    Analyse des moyens de paiement

    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame des transactions

    Returns:
    --------
    pd.DataFrame
        Statistiques par moyen de paiement
    """
    completed = df[df['status'] == 'Complété']

    payment_stats = completed.groupby('payment_method').agg({
        'total_amount': 'sum',
        'transaction_id': 'count'
    }).reset_index()

    payment_stats.columns = ['payment_method', 'revenue', 'transactions']
    payment_stats['percentage'] = (payment_stats['transactions'] / payment_stats['transactions'].sum()) * 100
    payment_stats = payment_stats.sort_values('revenue', ascending=False)

    return payment_stats

if __name__ == "__main__":
    # Test du script
    print("Chargement des donnees...")
    transactions, customers = load_data()

    print("\n=== KPIs PRINCIPAUX ===")
    kpis = calculate_kpis(transactions)
    for key, value in kpis.items():
        if 'rate' in key or 'percentage' in key:
            print(f"{key}: {value:.2f}%")
        elif 'revenue' in key or 'value' in key:
            print(f"{key}: {value:,.2f} EUR")
        else:
            print(f"{key}: {value:,}")

    print("\n=== VENTES PAR CATEGORIE ===")
    print(sales_by_category(transactions))

    print("\n=== TOP 5 PRODUITS ===")
    print(top_products(transactions, n=5))

    print("\n=== SEGMENTS CLIENTS ===")
    print(customer_segments_analysis(customers))
