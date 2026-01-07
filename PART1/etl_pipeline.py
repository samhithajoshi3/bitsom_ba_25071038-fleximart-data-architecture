print("🔥 FILE.PY IS RUNNING 🔥", flush=True)

# # ==============================
# # STEP 0: IMPORTS
# # ==============================
import pandas as pd
import numpy as np
import mysql.connector
import os
import re
import sys

print("STEP 1: Script started")

# ==============================
# STEP 1: DATABASE CONNECTION
# ==============================
db_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SQLPass@2025",
        database="Fleximart"
    )
cursor = db_conn.cursor()
print(" MySQL connection successful")

# # ==============================
# # STEP 2: READ CSV FILE
# # ==============================
customers_raw_csv_path = (
    r"C:\Users\SAMHITHA SHARMA\Desktop\Fleximart\Data\customers_raw.csv"
)

print("STEP 3: Checking CSV path...")
print(customers_raw_csv_path)

if not os.path.exists(customers_raw_csv_path):
    print("ERROR: CSV file NOT FOUND")
    sys.exit(1)

customers_raw_df = pd.read_csv(customers_raw_csv_path)

print("STEP 4: CSV loaded successfully")
print("Rows:", len(customers_raw_df))
print(customers_raw_df.head())

# # ==============================
# # STEP 3: REMOVE NULL customer_id
# # ==============================
customers_raw_df = customers_raw_df[customers_raw_df['customer_id'].notna()]
print("STEP 5: Removed null customer_id rows")

# # ==============================
# # STEP 4: CLEAN PHONE NUMBERS
# # ==============================
customers_raw_df['phone'] = customers_raw_df['phone'].astype(str)

def standardize_phone(phone):
    digits = re.sub(r'[^0-9]', '', phone)
    if len(digits) >= 10:
        return "'+91" + digits[-10:]
    return None

customers_raw_df['phone'] = customers_raw_df['phone'].apply(standardize_phone)
print("STEP 6: Phone numbers standardized")

# # ==============================
# # STEP 5: HANDLE EMAILS
# # ==============================
def generate_email(row):
    if pd.isna(row['email']) or str(row['email']).strip() == '':
        fn = str(row['first_name']).strip().lower()
        ln = str(row['last_name']).strip().lower()
        return f"{fn}.{ln}.{row['customer_id']}@fleximart.com"
    return row['email'].strip().lower()

customers_raw_df['email'] = customers_raw_df.apply(generate_email, axis=1)
print("STEP 7: Emails cleaned")

# # ==============================
# # STEP 6: REMOVE DUPLICATES
# # ==============================
before = len(customers_raw_df)
customers_raw_df = customers_raw_df.drop_duplicates(
    subset='customer_id',
    keep='first'
)
after = len(customers_raw_df)
print(f"STEP 8: Removed {before - after} duplicates")

# # ==============================
# # STEP 7: SAVE FILE
# # ==============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

os.makedirs(DATA_DIR, exist_ok=True)

output_path = os.path.join(DATA_DIR, "customers_clean.csv")
customers_raw_df.to_csv(output_path, index=False)

print("STEP 9: File saved successfully")
print("Saved at:", output_path)

print("✅ SCRIPT COMPLETED SUCCESSFULLY")

print("🔥 PRODUCTS ETL STARTED 🔥", flush=True)

def debug(msg):
    print(f"[DEBUG] {msg}", flush=True)

# # ==============================
# # CSV INPUT PATH
# # ==============================
products_csv_path = r"C:\Users\SAMHITHA SHARMA\Desktop\Fleximart\Data\products_raw.csv"

debug(f"Reading CSV from: {products_csv_path}")

if not os.path.exists(products_csv_path):
    debug("❌ product_raw.csv not found")
    sys.exit(1)

products_raw_df = pd.read_csv(products_csv_path)
debug(f"Loaded {len(products_raw_df)} rows")

# # ==============================
# # CLEANING STEPS
# # ==============================
products_raw_df['category'] = (
    products_raw_df['category']
    .astype(str)
    .str.strip()
    .str.lower()
)

products_raw_df['category'] = products_raw_df['category'].replace({
    'electronics': 'Electronics',
    'fashion': 'Fashion',
    'groceries': 'Groceries'
}).fillna('Other')

products_raw_df['product_name'] = (
    products_raw_df['product_name']
    .astype(str)
    .str.strip()
    .str.title()
)

products_raw_df['price'] = pd.to_numeric(
    products_raw_df['price'], errors='coerce'
)

products_raw_df['price'] = products_raw_df.groupby('category')['price']\
    .transform(lambda x: x.fillna(x.median()))

products_raw_df['stock_quantity'] = pd.to_numeric(
    products_raw_df['stock_quantity'], errors='coerce'
).fillna(0).astype(int)

# # ==============================
# # SAVE CLEAN FILE (EXPLICIT PATH)
# # ==============================
output_path = r"C:\Users\SAMHITHA SHARMA\Desktop\Fleximart\Data\products_clean.csv"

products_raw_df.to_csv(output_path, index=False)

print("✅ products_clean.csv saved successfully", flush=True)
print("📍 Location:", output_path, flush=True)

# # =====================================================
# # SALES ETL - STEP 1: EXTRACT
# # =====================================================

sales_csv_path = r"C:\Users\SAMHITHA SHARMA\Desktop\Fleximart\Data\sales_raw.csv"

sales_raw_df = pd.read_csv(sales_csv_path)

print("\n================ SALES RAW DATA ================\n")
print(sales_raw_df.head())
print("\nTotal sales records:", len(sales_raw_df))

# # ==============================
# # DEBUG: Check extra / garbage rows in sales
# # ==============================

print("\nSales DataFrame info:")
sales_raw_df.info()

print("\nLast 5 rows of sales data:")
print(sales_raw_df.tail())

# # ==============================
# # SALES TRANSFORM: Remove garbage rows
# # ==============================

before = len(sales_raw_df)

# Remove rows with missing or blank transaction_id
sales_raw_df = sales_raw_df[
    sales_raw_df['transaction_id'].notna() &
    (sales_raw_df['transaction_id'].astype(str).str.strip() != '')
]

after = len(sales_raw_df)

print("\nGarbage sales rows removed:", before - after)
print("Sales records after garbage removal:", after)

# # ==============================
# # SALES TRANSFORM: Remove duplicate transactions
# # ==============================

before = len(sales_raw_df)

sales_raw_df = sales_raw_df.drop_duplicates(subset='transaction_id', keep='first')

after = len(sales_raw_df)

print("\nDuplicate transactions removed:", before - after)
print("Sales records after deduplication:", after)

# # ==============================
# # SALES TRANSFORM: Drop rows with missing customer_id
# # ==============================

before = len(sales_raw_df)

sales_raw_df = sales_raw_df[sales_raw_df['customer_id'].notna()]

after = len(sales_raw_df)

print("\nRows dropped due to missing customer_id:", before - after)
print("Sales records after customer_id cleaning:", after)

# # ==============================
# # SALES TRANSFORM: Drop rows with missing product_id
# # ==============================

before = len(sales_raw_df)

sales_raw_df = sales_raw_df[sales_raw_df['product_id'].notna()]

after = len(sales_raw_df)

print("\nRows dropped due to missing product_id:", before - after)
print("Sales records after product_id cleaning:", after)

# # ==============================
# # SALES TRANSFORM: Clean transaction_date
# # ==============================

def clean_transaction_date(date_value):
    try:
        parsed_date = pd.to_datetime(date_value, dayfirst=True)
        return parsed_date.strftime('%Y-%m-%d')
    except:
        return None

sales_raw_df['transaction_date'] = sales_raw_df['transaction_date'].apply(clean_transaction_date)

print("\nInvalid transaction dates after cleaning:",
      sales_raw_df['transaction_date'].isna().sum())

# # ==============================
# # STRICT FK CLEANING: Remove empty strings also
# # ==============================

sales_raw_df['customer_id'] = sales_raw_df['customer_id'].astype(str).str.strip()
sales_raw_df['product_id'] = sales_raw_df['product_id'].astype(str).str.strip()

before = len(sales_raw_df)

sales_raw_df = sales_raw_df[
    (sales_raw_df['customer_id'] != '') &
    (sales_raw_df['product_id'] != '')
]

after = len(sales_raw_df)

print("\nRows dropped due to empty customer_id/product_id:", before - after)
print("Sales records after strict FK cleaning:", after)

# # =====================================================
# # SALES TRANSFORM: Add total_amount column
# # =====================================================

sales_raw_df['total_amount'] = sales_raw_df['quantity'] * sales_raw_df['unit_price']

print("\nTotal amount column added.")
print(sales_raw_df[['transaction_id', 'quantity', 'unit_price', 'total_amount']].head())

print("\nNULL check including total_amount:")
print(
    sales_raw_df[
        ['transaction_id','customer_id','product_id',
         'quantity','unit_price','total_amount','transaction_date']
    ].isna().sum()
)

print("\nTotal amount sanity (min, max):")
print(sales_raw_df['total_amount'].min(), sales_raw_df['total_amount'].max())

# # =====================================================
# # SAVE CLEAN SALES CSV
# # =====================================================

sales_clean_path =r"C:\Users\SAMHITHA SHARMA\Desktop\Fleximart\Data\sales_clean.csv"
sales_raw_df.to_csv(sales_clean_path, index=False)

print(f"\n Clean sales data saved to {sales_clean_path}")

# # ====================================================
# # LOAD PHASE: INSERT CUSTOMERS
# # =====================================================

insert_customer_sql = """
INSERT IGNORE INTO customers
(first_name, last_name, email, phone, city, registration_date)
VALUES (%s, %s, %s, %s, %s, %s)
"""

customer_records = customers_raw_df[
    ['first_name', 'last_name', 'email', 'phone', 'city', 'registration_date']
].values.tolist()

cursor.executemany(insert_customer_sql, customer_records)
db_conn.commit()

print(f" Customers inserted: {cursor.rowcount}")

# # # =====================================================
# # # LOAD PHASE: INSERT PRODUCTS
# # # =====================================================

insert_product_sql = """
INSERT INTO products
(product_name, category, price, stock_quantity)
VALUES (%s, %s, %s, %s)
"""

product_records = products_raw_df[
    ['product_name', 'category', 'price', 'stock_quantity']
].values.tolist()

cursor.executemany(insert_product_sql, product_records)
db_conn.commit()

print(f" Products inserted: {cursor.rowcount}")

# =====================================================
# BUILD PRODUCT MAP (CSV product_id -> DB product_id)
# =====================================================

# Get DB products
cursor.execute("SELECT product_id, product_name FROM products")
db_products = cursor.fetchall()

# Build CSV lookup: product_id -> product_name
csv_product_lookup = {
    row["product_id"]: row["product_name"]
    for _, row in products_raw_df.iterrows()
}

product_map = {}

for db_pid, db_name in db_products:
    for csv_pid, csv_name in csv_product_lookup.items():
        if csv_name.strip().lower() == db_name.strip().lower():
            product_map[csv_pid] = db_pid

print(" Product map created:", len(product_map))


# =====================================================
# BUILD CUSTOMER MAP (email -> db customer_id)
# =====================================================

cursor.execute("SELECT customer_id, email FROM customers")
customer_map = {email: cid for cid, email in cursor.fetchall()}

print(" Customer map created:", len(customer_map))


# =====================================================
# CSV customer_id -> email lookup
# =====================================================

customer_lookup = {
    row["customer_id"]: row["email"]
    for _, row in customers_raw_df.iterrows()
}

print(" Customer lookup created")


# =====================================================
# DETECT TOTAL AMOUNT COLUMN SAFELY
# =====================================================

if "total_amount" in sales_raw_df.columns:
    amount_col = "total_amount"
elif "amount" in sales_raw_df.columns:
    amount_col = "amount"
elif "order_amount" in sales_raw_df.columns:
    amount_col = "order_amount"
else:
    raise Exception(
        f"No amount column found. Available columns: {list(sales_raw_df.columns)}"
    )

print(f" Using amount column: {amount_col}")


# =====================================================
# INSERT ORDERS & BUILD ORDER MAP
# =====================================================

insert_order_sql = """
INSERT INTO orders (customer_id, order_date, total_amount)
VALUES (%s, %s, %s)
"""

order_map = {}
inserted = 0
skipped = 0


for _, row in sales_raw_df.iterrows():

    # CSV customer_id -> email
    email = customer_lookup.get(row["customer_id"])
    if email is None:
        skipped += 1
        continue

    # email -> DB customer_id
    db_customer_id = customer_map.get(email)
    if db_customer_id is None:
        skipped += 1
        continue

    cursor.execute(
        insert_order_sql,
        (
            db_customer_id,
            row["transaction_date"],
            row[amount_col]
        )
    )

    order_id = cursor.lastrowid
    order_map[row["transaction_id"]] = order_id

    inserted += 1

db_conn.commit()

print(f" Orders inserted: {inserted}")
print(f" Orders skipped: {skipped}")

# =====================================================
# INSERT ORDER ITEMS
# =====================================================

insert_order_item_sql = """
INSERT INTO order_items
(order_id, product_id, quantity, unit_price, subtotal)
VALUES (%s, %s, %s, %s, %s)
"""


inserted_items = 0
skipped_items = 0

for _, row in sales_raw_df.iterrows():

    order_id = order_map.get(row["transaction_id"])
    if order_id is None:
        skipped_items += 1
        continue

    product_id = product_map.get(row["product_id"])
    if product_id is None:
        skipped_items += 1
        continue
    
    subtotal = int(row["quantity"]) * float(row["unit_price"])

    cursor.execute(
        insert_order_item_sql,
        (
            order_id,
            product_id,
            int(row["quantity"]),
            float(row["unit_price"]),
            subtotal
        )
    )

    inserted_items += 1

db_conn.commit()

print(f" Order items inserted: {inserted_items}")
print(f" Order items skipped: {skipped_items}")


# ===============================
# CLOSE CONNECTION
# ===============================

cursor.close()
db_conn.close()
print(" Database connection closed")