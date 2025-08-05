import pandas as pd
import csv
import os
import sqlite3
from datetime import datetime

products = {
    1: {"name": "Apples", "price": 30},
    2: {"name": "Bananas", "price": 20},
    3: {"name": "Milk", "price": 50},
    4: {"name": "Bread", "price": 25},
    5: {"name": "Eggs", "price": 60}
}

cart = {}
TRANSACTION_FILE = "transactions.csv"
DB_FILE = "transactions.db"

# Ensure the CSV exists
if not os.path.exists(TRANSACTION_FILE):
    with open(TRANSACTION_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "product_id", "product_name", "quantity", "price", "total"])

def show_products():
    print("\nAvailable Products:")
    for pid, info in products.items():
        print(f"{pid}. {info['name']} - Rs. {info['price']}/unit")

def add_to_cart():
    try:
        pid = int(input("Enter Product ID to add to cart: "))
        if pid not in products:
            print("Invalid Product ID")
            return
        qty = int(input("Enter quantity: "))
        if pid in cart:
            cart[pid] += qty
        else:
            cart[pid] = qty
        print(f"Added {qty} x {products[pid]['name']} to cart.")
    except ValueError:
        print("Invalid input. Please enter numbers only.")

def view_cart():
    print("\nYour Cart:")
    if not cart:
        print("Cart is empty.")
        return
    total = 0
    for pid, qty in cart.items():
        name = products[pid]['name']
        price = products[pid]['price']
        subtotal = price * qty
        total += subtotal
        print(f"{name} x {qty} = Rs. {subtotal}")
    print(f"Total: Rs. {total}")

def checkout_and_save():
    if not cart:
        print("Your cart is empty. Nothing to checkout.")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TRANSACTION_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        for pid, qty in cart.items():
            name = products[pid]['name']
            price = products[pid]['price']
            total = price * qty
            writer.writerow([now, pid, name, qty, price, total])

    print("\nCheckout complete. Your transaction has been saved.")
    cart.clear()

def analyze_transactions():
    print("\n--- Transaction Analysis ---")
    if not os.path.exists(TRANSACTION_FILE):
        print("No transactions found.")
        return

    df = pd.read_csv(TRANSACTION_FILE)

    if df.empty:
        print("No data to analyze.")
        return

    print("\nTotal Revenue: Rs.", df['total'].sum())

    print("\nTop Selling Products:")
    top_products = df.groupby('product_name')['quantity'].sum().sort_values(ascending=False)
    print(top_products)

    print("\nRevenue by Product:")
    revenue_by_product = df.groupby('product_name')['total'].sum().sort_values(ascending=False)
    print(revenue_by_product)

def load_to_sqlite():
    print("\n--- Loading Data to SQLite ---")
    if not os.path.exists(TRANSACTION_FILE):
        print("Transaction CSV not found.")
        return

    df = pd.read_csv(TRANSACTION_FILE)

    if df.empty:
        print("No data to load.")
        return

    conn = sqlite3.connect(DB_FILE)
    df.to_sql("transactions", conn, if_exists='replace', index=False)

    print("Data loaded into SQLite database.")

    cursor = conn.cursor()
    cursor.execute("SELECT SUM(total) FROM transactions")
    print("\n[SQL] Total Revenue:", cursor.fetchone()[0])

    cursor.execute("""
        SELECT product_name, SUM(quantity) as total_qty
        FROM transactions
        GROUP BY product_name
        ORDER BY total_qty DESC
    """)
    print("\n[SQL] Top Selling Products:")
    for row in cursor.fetchall():
        print(row)

    conn.close()

def main():
    while True:
        print("\n--- Grocery Store Menu ---")
        print("1. View Products")
        print("2. Add to Cart")
        print("3. View Cart")
        print("4. Checkout and Save")
        print("5. Analyze Transactions")
        print("6. Load to SQLite + SQL Analysis")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            show_products()
        elif choice == '2':
            add_to_cart()
        elif choice == '3':
            view_cart()
        elif choice == '4':
            checkout_and_save()
        elif choice == '5':
            analyze_transactions()
        elif choice == '6':
            load_to_sqlite()
        elif choice == '7':
            print("Thank you for shopping with us!")
            break
        else:
            print("Invalid choice. Please select 1-7.")

if __name__ == "__main__":
    main()
