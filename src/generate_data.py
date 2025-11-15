"""
Génère des données e-commerce réalistes pour l'analyse
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration
np.random.seed(42)
random.seed(42)

# Listes de produits réalistes
CATEGORIES = ['Électronique', 'Vêtements', 'Maison & Jardin', 'Sports & Loisirs', 'Livres']
PRODUCTS = {
    'Électronique': ['Smartphone', 'Laptop', 'Tablette', 'Écouteurs', 'Montre connectée', 'Enceinte Bluetooth'],
    'Vêtements': ['T-shirt', 'Jean', 'Robe', 'Veste', 'Chaussures', 'Sac à main'],
    'Maison & Jardin': ['Aspirateur', 'Cafetière', 'Lampe', 'Coussin', 'Plante', 'Bougie'],
    'Sports & Loisirs': ['Ballon', 'Tapis de yoga', 'Vélo', 'Raquette', 'Sac de sport', 'Gourde'],
    'Livres': ['Roman', 'BD', 'Guide pratique', 'Biographie', 'Science-fiction', 'Cuisine']
}

REGIONS = ['Île-de-France', 'Auvergne-Rhône-Alpes', 'Provence-Alpes-Côte d\'Azur',
           'Nouvelle-Aquitaine', 'Occitanie', 'Hauts-de-France', 'Bretagne', 'Grand Est']

PAYMENT_METHODS = ['Carte bancaire', 'PayPal', 'Virement', 'Apple Pay']

def generate_ecommerce_data(n_transactions=5000):
    """
    Génère un dataset de transactions e-commerce

    Parameters:
    -----------
    n_transactions : int
        Nombre de transactions à générer

    Returns:
    --------
    pd.DataFrame
        DataFrame avec les transactions
    """
    data = []

    # Date de début : il y a 2 ans
    start_date = datetime.now() - timedelta(days=730)

    for i in range(n_transactions):
        # Génération de la date (plus de ventes récentes)
        days_offset = int(np.random.exponential(200))
        if days_offset > 730:
            days_offset = random.randint(0, 730)
        transaction_date = start_date + timedelta(days=days_offset)

        # Catégorie et produit
        category = random.choice(CATEGORIES)
        product = random.choice(PRODUCTS[category])

        # Prix basé sur la catégorie
        if category == 'Électronique':
            base_price = random.uniform(50, 1200)
        elif category == 'Vêtements':
            base_price = random.uniform(15, 150)
        elif category == 'Maison & Jardin':
            base_price = random.uniform(10, 300)
        elif category == 'Sports & Loisirs':
            base_price = random.uniform(10, 500)
        else:  # Livres
            base_price = random.uniform(5, 50)

        # Quantité (plus souvent 1-2)
        quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])

        # Prix total avec petite variation aléatoire
        price = round(base_price * random.uniform(0.9, 1.1), 2)
        total = round(price * quantity, 2)

        # Client ID (environ 1000 clients différents)
        customer_id = f"CUST_{random.randint(1, 1000):04d}"

        # Région
        region = random.choice(REGIONS)

        # Moyen de paiement
        payment = random.choice(PAYMENT_METHODS)

        # Statut (95% de succès)
        status = np.random.choice(['Complété', 'Annulé', 'Remboursé'],
                                   p=[0.95, 0.03, 0.02])

        # Ajouter la transaction
        data.append({
            'transaction_id': f"TXN_{i+1:06d}",
            'date': transaction_date.strftime('%Y-%m-%d'),
            'customer_id': customer_id,
            'category': category,
            'product': product,
            'quantity': quantity,
            'unit_price': price,
            'total_amount': total if status == 'Complété' else 0,
            'region': region,
            'payment_method': payment,
            'status': status
        })

    df = pd.DataFrame(data)

    # Trier par date
    df = df.sort_values('date').reset_index(drop=True)

    return df

def generate_customer_data(transactions_df):
    """
    Génère une table de clients basée sur les transactions

    Parameters:
    -----------
    transactions_df : pd.DataFrame
        DataFrame des transactions

    Returns:
    --------
    pd.DataFrame
        DataFrame avec les informations clients
    """
    customers = transactions_df['customer_id'].unique()

    data = []
    for customer_id in customers:
        # Première transaction du client
        first_purchase = transactions_df[transactions_df['customer_id'] == customer_id]['date'].min()

        # Nombre total d'achats
        total_purchases = len(transactions_df[transactions_df['customer_id'] == customer_id])

        # Montant total dépensé
        total_spent = transactions_df[
            (transactions_df['customer_id'] == customer_id) &
            (transactions_df['status'] == 'Complété')
        ]['total_amount'].sum()

        # Segment client basé sur le total dépensé
        if total_spent > 2000:
            segment = 'Premium'
        elif total_spent > 500:
            segment = 'Régulier'
        else:
            segment = 'Occasionnel'

        data.append({
            'customer_id': customer_id,
            'first_purchase_date': first_purchase,
            'total_purchases': total_purchases,
            'total_spent': round(total_spent, 2),
            'segment': segment
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generation des donnees e-commerce...")

    # Générer les transactions
    transactions = generate_ecommerce_data(n_transactions=5000)
    transactions.to_csv('data/transactions.csv', index=False, encoding='utf-8')
    print(f"OK - {len(transactions)} transactions generees -> data/transactions.csv")

    # Générer les données clients
    customers = generate_customer_data(transactions)
    customers.to_csv('data/customers.csv', index=False, encoding='utf-8')
    print(f"OK - {len(customers)} clients generes -> data/customers.csv")

    # Afficher un aperçu
    print("\nApercu des donnees:")
    print("\nTransactions:")
    print(transactions.head())
    print(f"\nShape: {transactions.shape}")
    print("\nClients:")
    print(customers.head())
    print(f"\nShape: {customers.shape}")

    print("\nGeneration terminee!")
