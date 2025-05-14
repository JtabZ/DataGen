import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid

# Set random seed for reproducibility
random.seed(42)
np.random.seed(42)

# Define parameters
start_date = datetime(2023, 1, 1)
end_date = datetime(2025, 12, 31)
num_transactions = 20000  # Total number of transactions
num_products = 150
num_customers = 500

# Define categories and dimensions
corporate_marketing_categories = ["Supplies", "Furniture", "Technology", "Services", "Equipment"]
divisions = ["North", "South", "East", "West", "Corporate"]
departments = {
    "North": ["Sales-North-A", "Sales-North-B", "Support-North", "Marketing-North"],
    "South": ["Sales-South-A", "Sales-South-B", "Support-South", "Marketing-South"],
    "East": ["Sales-East-A", "Sales-East-B", "Support-East", "Marketing-East"],
    "West": ["Sales-West-A", "Sales-West-B", "Support-West", "Marketing-West"],
    "Corporate": ["Executive", "Finance", "HR", "Legal", "IT"]
}
product_classes = ["Consumables", "Capital Goods", "Accessories", "Software", "Hardware", "Services"]
strategy_categories = ["Core Business", "Growth Area", "Strategic Initiative", "Legacy", "Innovation"]

# Create mapping dictionaries for more realistic data generation
product_to_category = {}
product_to_class = {}
product_to_cost_base = {}  # Base cost for each product
product_to_price_base = {}  # Base price for each product

# Generate products with consistent attributes
for i in range(1, num_products + 1):
    product_id = f"PROD-{i:05d}"
    category = random.choice(corporate_marketing_categories)
    product_class = random.choice(product_classes)
    
    # Assign logical base cost and price based on category and class
    if category == "Technology" and product_class in ["Software", "Hardware"]:
        base_cost = random.uniform(200, 1500)
        markup = random.uniform(1.3, 2.0)  # Higher margin for tech
    elif category == "Furniture":
        base_cost = random.uniform(100, 800)
        markup = random.uniform(1.2, 1.6)  # Medium margin
    elif category == "Supplies" and product_class == "Consumables":
        base_cost = random.uniform(10, 100)
        markup = random.uniform(1.5, 2.2)  # High margin for consumables
    else:
        base_cost = random.uniform(50, 300)
        markup = random.uniform(1.2, 1.8)
    
    base_price = base_cost * markup
    
    product_to_category[product_id] = category
    product_to_class[product_id] = product_class
    product_to_cost_base[product_id] = base_cost
    product_to_price_base[product_id] = base_price

# Generate customer IDs
customers = [f"CUST-{i:05d}" for i in range(1, num_customers + 1)]

# Function to generate a single transaction
def generate_transaction(transaction_id):
    # Generate transaction date with more transactions in certain periods
    days_range = (end_date - start_date).days
    
    # Create seasonal patterns with more sales in Q4 and fewer in Q1
    while True:
        random_days = int(np.random.triangular(0, days_range*0.6, days_range))
        date = start_date + timedelta(days=random_days)
        month = date.month
        
        # Higher probability of transactions in Q4 (Oct-Dec), lower in Q1 (Jan-Mar)
        if month in [10, 11, 12]:  # Q4
            if random.random() < 0.7:  # 70% chance to accept this date
                break
        elif month in [1, 2, 3]:  # Q1
            if random.random() < 0.3:  # 30% chance to accept this date
                break
        else:  # Q2 and Q3
            if random.random() < 0.5:  # 50% chance to accept this date
                break
    
    # Select a product
    product_id = random.choice(list(product_to_category.keys()))
    
    # Get product attributes
    category = product_to_category[product_id]
    product_class = product_to_class[product_id]
    
    # Determine division with some categories more common in certain divisions
    if category == "Technology":
        # Technology more common in Corporate and West
        division_weights = [0.15, 0.15, 0.15, 0.25, 0.3]  # North, South, East, West, Corporate
    elif category == "Supplies":
        # Supplies more evenly distributed
        division_weights = [0.2, 0.2, 0.2, 0.2, 0.2]
    else:
        # Other categories have different distribution
        division_weights = [0.25, 0.25, 0.2, 0.2, 0.1]
    
    division = random.choices(divisions, weights=division_weights, k=1)[0]
    
    # Select department based on division
    department = random.choice(departments[division])
    
    # Select strategy category with some logic
    if product_class in ["Software", "Services"] and random.random() < 0.7:
        strategy = "Growth Area" if random.random() < 0.6 else "Strategic Initiative"
    elif product_class == "Consumables":
        strategy = "Core Business" if random.random() < 0.8 else "Legacy"
    elif product_class == "Hardware" and random.random() < 0.6:
        strategy = "Innovation" if random.random() < 0.4 else "Strategic Initiative"
    else:
        strategy = random.choice(strategy_categories)
    
    # Get base cost and price for the product
    base_cost = product_to_cost_base[product_id]
    base_price = product_to_price_base[product_id]
    
    # Add some variability to cost and price
    cost_variability = random.uniform(0.95, 1.05)  # ±5% variability
    price_variability = random.uniform(0.97, 1.08)  # Slightly higher price variability
    
    # Introduce time-based trends:
    # - Costs generally increase over time (inflation)
    # - Prices may increase or decrease based on competition and market
    days_factor = random_days / days_range
    
    if category == "Technology":
        # Technology costs decrease over time (newer tech gets cheaper)
        cost_trend = 1 - (days_factor * 0.15)  # Up to 15% decrease over the period
        # But competition causes prices to decrease faster
        price_trend = 1 - (days_factor * 0.2)  # Up to 20% decrease over the period
    elif category == "Supplies":
        # Supplies costs increase due to inflation
        cost_trend = 1 + (days_factor * 0.1)  # Up to 10% increase
        # Prices increase slightly more due to markup
        price_trend = 1 + (days_factor * 0.12)  # Up to 12% increase
    else:
        # Other categories have mild cost increases
        cost_trend = 1 + (days_factor * 0.08)  # Up to 8% increase
        # Prices rise with costs
        price_trend = 1 + (days_factor * 0.09)  # Up to 9% increase
    
    # Apply all factors
    final_cost = base_cost * cost_variability * cost_trend
    final_price = base_price * price_variability * price_trend
    
    # Add some randomness to sales amounts (e.g., discounts, bulk purchases)
    quantity = np.random.choice([1, 1, 1, 2, 2, 3, 4, 5], p=[0.5, 0.2, 0.1, 0.1, 0.05, 0.03, 0.01, 0.01])
    
    # Adjust pricing for bulk purchases
    if quantity > 1:
        bulk_discount = 1 - (quantity * 0.02)  # 2% discount per quantity
        final_price = final_price * max(bulk_discount, 0.85)  # max 15% discount
    
    sales_amount = round(final_price * quantity, 2)
    cost_of_goods_sold = round(final_cost * quantity, 2)
    
    # Ensure profits are generally positive but allow some negative margins
    if cost_of_goods_sold > sales_amount and random.random() > 0.05:  # Only allow 5% of transactions to have negative margins
        # Adjust sales amount to create a small positive margin
        sales_amount = round(cost_of_goods_sold * random.uniform(1.01, 1.1), 2)
    
    # Select a customer
    customer_id = random.choice(customers)
    
    return {
        "TransactionID": f"ORD-{transaction_id:06d}",
        "TransactionDate": date.strftime("%Y-%m-%d"),
        "ProductID": product_id,
        "CustomerID": customer_id,
        "SalesAmount": sales_amount,
        "CostOfGoodsSold": cost_of_goods_sold,
        "CorporateMarketingCategory": category,
        "Division": division,
        "Department": department,
        "ProductClass": product_class,
        "StrategyCategory": strategy
    }

# Generate all transactions
transactions = [generate_transaction(i) for i in range(1, num_transactions + 1)]

# Convert to DataFrame
df = pd.DataFrame(transactions)

# Add calculated fields for reference (these would typically be created in Tableau)
df["Profit"] = df["SalesAmount"] - df["CostOfGoodsSold"]
df["MarginRate"] = df["Profit"] / df["SalesAmount"]
df["Year"] = pd.to_datetime(df["TransactionDate"]).dt.year

# Verify data
print(f"Data ranges from {df['TransactionDate'].min()} to {df['TransactionDate'].max()}")
print(f"Total number of transactions: {len(df)}")
print(f"Average Sales Amount: ${df['SalesAmount'].mean():.2f}")
print(f"Average Margin Rate: {df['MarginRate'].mean():.2%}")
print(f"Year distribution: {df['Year'].value_counts().to_dict()}")

# Save the data
df.to_csv("sales_transactions.csv", index=False)
print("Data saved to sales_transactions.csv")

# Generate some summary statistics for verification
print("\nSummary by Corporate Marketing Category:")
category_summary = df.groupby("CorporateMarketingCategory").agg({
    "SalesAmount": "sum",
    "Profit": "sum",
    "TransactionID": "count"
}).rename(columns={"TransactionID": "Count"})
category_summary["MarginRate"] = category_summary["Profit"] / category_summary["SalesAmount"]
print(category_summary)

print("\nSummary by Year and Division:")
year_division_summary = df.groupby(["Year", "Division"]).agg({
    "SalesAmount": "sum",
    "Profit": "sum"
})
print(year_division_summary)

# Optional: Create a product master table
product_df = pd.DataFrame([
    {
        "ProductID": prod_id,
        "CorporateMarketingCategory": product_to_category[prod_id],
        "ProductClass": product_to_class[prod_id],
        "BaseCost": product_to_cost_base[prod_id],
        "BasePrice": product_to_price_base[prod_id]
    } for prod_id in product_to_category.keys()
])
product_df.to_csv("product_master.csv", index=False)
print("Product master data saved to product_master.csv")