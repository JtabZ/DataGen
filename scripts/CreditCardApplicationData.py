import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import uuid
import calendar # Keep for potential future use

# --- Configuration (Simplified) ---
START_DATE = datetime(2023, 5, 1) # Approx 2 years prior
END_DATE = datetime(2026, 5, 1)     # Approx 1 year into the future
NUM_CARDHOLDERS = 750 # Number of unique cardholders
AVG_APPS_PER_DAY = 30      # Increased average applications per day (previously 10)
APPROVAL_RATE = 0.55 # 55% of applications are approved
ACTIVATION_RATE = 0.85 # 85% of approved accounts are activated
TRANSACTIONS_PER_ACTIVATED_ACCOUNT = 5 # Fixed number of transactions per activated account

STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
          'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
          'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
          'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
          'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

# --- Configuration for Delinquency ---
DELINQUENCY_CONFIG = {
    "BASE_RATE": 0.07,  # General delinquency rate (7%) for accounts 30+ DPD
    "Q1_2024_RATE": 0.065, # Q1 (Jan, Feb, Mar) 2024 delinquency rate (6.5%)
    "Q1_2025_RATE": 0.059, # Q1 (Jan, Feb, Mar) 2025 delinquency rate (5.9%)
    "Q1_2026_RATE": 0.055, # Q1 (Jan, Feb, Mar) 2026 delinquency rate (5.5%, continued improvement)
    "MIN_BALANCE_FOR_DELINQUENCY": 10.00, # Min outstanding balance to be considered for delinquency
    "MIN_PAYMENT_FLAT": 25.00, # Flat part of minimum payment calculation
    "MIN_PAYMENT_PERCENT": 0.02 # Percentage part of minimum payment calculation (2% of balance)
}
CREDIT_LIMIT_OPTIONS = [500, 1000, 2500, 5000, 7500, 10000, 15000, 20000]

# --- Helper Functions ---
def random_date(start, end):
    """Generate a random datetime between start and end."""
    if isinstance(start, pd.Timestamp): start = start.to_pydatetime()
    if isinstance(end, pd.Timestamp): end = end.to_pydatetime()

    if start > end:
        return start 

    time_diff = end - start
    total_seconds_diff = time_diff.total_seconds()
    
    if total_seconds_diff < 0: total_seconds_diff = 0

    return start + timedelta(
        seconds=random.randint(0, int(total_seconds_diff)),
    )

def generate_ids(prefix, n):
    """Generates a list of unique IDs."""
    n = max(0, n)
    return [f"{prefix}_{uuid.uuid4().hex[:8].upper()}" for _ in range(n)]

# --- Data Generation ---

print("Generating Cardholders...")
cardholder_ids = generate_ids("CUST", NUM_CARDHOLDERS)
print(f"Generated {len(cardholder_ids)} cardholders.")

print("Generating Applications...")
applications_data = []
total_days = (END_DATE - START_DATE).days
num_applications = total_days * AVG_APPS_PER_DAY # This will now be higher
application_ids = generate_ids("APP", num_applications)

app_styles = ["Standard Application", "Net Applications", "New Applications", "Activated New Accounts"]
app_style_weights = [0.45, 0.25, 0.20, 0.10]

for i in range(num_applications):
    app_id = application_ids[i]
    if not cardholder_ids: break # Should not happen with current NUM_CARDHOLDERS
    cardholder_id = random.choice(cardholder_ids)
    app_date = random_date(START_DATE, END_DATE)
    state = random.choice(STATES)
    actual_status = 'Approved' if random.random() < APPROVAL_RATE else 'Rejected'
    assigned_style = random.choices(app_styles, weights=app_style_weights, k=1)[0]

    applications_data.append({
        'ApplicationID': app_id,
        'CardholderID': cardholder_id,
        'ApplicationDate': app_date,
        'ApplicantState': state,
        'ApplicationStatus': actual_status,
        'ApplicationStyle': assigned_style
    })
    if (i + 1) % 10000 == 0: print(f"Generated {i+1}/{num_applications} applications...") # Adjusted print frequency

applications_df = pd.DataFrame(applications_data)
print(f"Generated {len(applications_df)} total applications with ApplicationStyle.")

print("Generating Accounts...")
accounts_data = []
approved_apps = applications_df[applications_df['ApplicationStatus'] == 'Approved'].copy()
print(f"Processing {len(approved_apps)} approved applications for account creation...")

num_accounts_needed = len(approved_apps)
account_ids_list = generate_ids("ACC", num_accounts_needed)

account_id_counter = 0
for index, app_row in approved_apps.iterrows():
    if account_id_counter >= len(account_ids_list): break
    account_id = account_ids_list[account_id_counter]
    account_id_counter += 1

    app_date = app_row['ApplicationDate']
    open_delay = random.randint(1, 5)
    open_date_dt = pd.to_datetime(app_date) + timedelta(days=open_delay)
    open_date_dt = min(open_date_dt, pd.to_datetime(END_DATE))
    open_date = open_date_dt.date()

    activation_status = 'Activated' if random.random() < ACTIVATION_RATE else 'Not Activated'
    activation_date_val = None 
    if activation_status == 'Activated':
        activation_delay = random.randint(1, 14)
        activation_date_dt = open_date_dt + timedelta(days=activation_delay)
        activation_date_dt = min(activation_date_dt, pd.to_datetime(END_DATE))
        if activation_date_dt >= open_date_dt:
             activation_date_val = activation_date_dt.date()
        else:
            activation_status = 'Not Activated' 

    account_status = 'Active' if activation_status == 'Activated' and activation_date_val is not None else 'Inactive'
    credit_limit = random.choice(CREDIT_LIMIT_OPTIONS)

    accounts_data.append({
        'AccountID': account_id,
        'ApplicationID': app_row['ApplicationID'],
        'CardholderID': app_row['CardholderID'],
        'AccountOpenDate': open_date,
        'ActivationStatus': activation_status,
        'ActivationDate': activation_date_val, 
        'AccountStatus': account_status,
        'CreditLimit': credit_limit
    })
    if (index + 1) % 2000 == 0: print(f"Generated {index + 1}/{len(approved_apps)} accounts...") # Adjusted print frequency

accounts_df = pd.DataFrame(accounts_data)
print(f"Generated {len(accounts_df)} accounts.")


print("Generating Transactions (Simplified)...")
transactions_data = []
if not accounts_df.empty:
    active_accounts_for_trans = accounts_df[
        (accounts_df['ActivationStatus'] == 'Activated') &
        (accounts_df['ActivationDate'].notna())
    ].copy()
    print(f"Generating transactions for {len(active_accounts_for_trans)} activated accounts...")

    estimated_transactions = len(active_accounts_for_trans) * TRANSACTIONS_PER_ACTIVATED_ACCOUNT
    transaction_ids = generate_ids("TRX", estimated_transactions)
    transaction_id_counter = 0

    for index, acc_row in active_accounts_for_trans.iterrows():
        account_id = acc_row['AccountID']
        cardholder_id = acc_row['CardholderID']
        try:
            transaction_start_dt = pd.to_datetime(acc_row['ActivationDate'])
        except ValueError:
            print(f"Warning: Could not parse ActivationDate for AccountID {account_id}. Skipping transactions.")
            continue

        transaction_end_dt = pd.to_datetime(END_DATE)
        
        if transaction_start_dt > transaction_end_dt:
            continue

        for _ in range(TRANSACTIONS_PER_ACTIVATED_ACCOUNT):
            if transaction_id_counter >= len(transaction_ids):
                print("Warning: Ran out of pre-generated transaction IDs.")
                break
            
            trans_date = random_date(transaction_start_dt, transaction_end_dt)
            # MODIFIED: Increased transaction amounts
            # Lognormal distribution: exp(mu + sigma^2/2) is the mean.
            # For mean around 1000-1200: mu=6.8, sigma=0.8 => exp(6.8 + 0.8^2/2) = exp(7.12) approx 1236
            trans_amount = round(np.random.lognormal(mean=6.8, sigma=0.8), 2) 
            trans_amount = min(trans_amount, 7500) # Increased cap for transaction amount
            trans_type = random.choices(['Purchase', 'Payment', 'Fee', 'Return'], weights=[0.75, 0.15, 0.05, 0.05], k=1)[0]

            transactions_data.append({
                'TransactionID': transaction_ids[transaction_id_counter],
                'AccountID': account_id,
                'CardholderID': cardholder_id,
                'TransactionDate': trans_date,
                'TransactionAmount': trans_amount if trans_type != 'Payment' else -trans_amount,
                'TransactionType': trans_type
            })
            transaction_id_counter += 1
        if transaction_id_counter >= len(transaction_ids): break
        if (index + 1) % 1000 == 0: print(f"Processed transactions for {index + 1}/{len(active_accounts_for_trans)} accounts...") # Adjusted print frequency

transactions_df = pd.DataFrame(transactions_data)
if not transactions_df.empty:
    transactions_df['TransactionAmount'] = pd.to_numeric(transactions_df['TransactionAmount'])
    transactions_df['TransactionDate'] = pd.to_datetime(transactions_df['TransactionDate'])
print(f"Generated {len(transactions_df)} transactions.")


# --- Add Delinquency Snapshot to Accounts DataFrame ---
print("Adding delinquency snapshot to accounts...")
if not accounts_df.empty:
    accounts_df['SnapshotDate'] = pd.NaT
    accounts_df['OutstandingBalanceAtSnapshot'] = 0.0
    accounts_df['MinimumPaymentDueAtSnapshot'] = 0.0
    accounts_df['PaymentDueDateAtSnapshot'] = pd.NaT
    accounts_df['DelinquencyStatusAtSnapshot'] = 'Current (No Balance)'
    accounts_df['DaysPastDueAtSnapshot'] = 0

    active_accounts_indices = accounts_df[
        (accounts_df['AccountStatus'] == 'Active') &
        (accounts_df['ActivationDate'].notna())
    ].index

    processed_count = 0 # Counter for print statements
    for idx in active_accounts_indices:
        acc_row = accounts_df.loc[idx]
        activation_date = pd.to_datetime(acc_row['ActivationDate'])
        credit_limit = acc_row['CreditLimit']
        
        snapshot_period_start = activation_date + timedelta(days=30)
        snapshot_period_end = pd.to_datetime(END_DATE)

        if snapshot_period_start > snapshot_period_end:
            accounts_df.loc[idx, 'SnapshotDate'] = snapshot_period_end.date() 
            accounts_df.loc[idx, 'DelinquencyStatusAtSnapshot'] = 'Current (Too New)'
            continue

        snapshot_date_dt = random_date(snapshot_period_start, snapshot_period_end) # Keep as datetime for year/month extraction
        accounts_df.loc[idx, 'SnapshotDate'] = snapshot_date_dt.date()


        outstanding_balance = round(random.uniform(0, credit_limit * 1.05), 2)
        if outstanding_balance < 0: outstanding_balance = 0
        accounts_df.loc[idx, 'OutstandingBalanceAtSnapshot'] = outstanding_balance

        minimum_payment_due = 0
        payment_due_date = None
        days_past_due = 0
        delinquency_status = 'Current (No Balance)'

        if outstanding_balance >= DELINQUENCY_CONFIG["MIN_BALANCE_FOR_DELINQUENCY"]:
            month_of_snapshot = snapshot_date_dt.replace(day=1)
            minimum_payment_due = round(max(DELINQUENCY_CONFIG["MIN_PAYMENT_FLAT"], 
                                            outstanding_balance * DELINQUENCY_CONFIG["MIN_PAYMENT_PERCENT"]), 2)
            payment_due_date = (month_of_snapshot + timedelta(days=random.randint(20,25))).date()

            year = snapshot_date_dt.year
            month = snapshot_date_dt.month
            
            target_delinquency_rate = DELINQUENCY_CONFIG["BASE_RATE"]
            if month in [1, 2, 3]: 
                if year == 2024 and "Q1_2024_RATE" in DELINQUENCY_CONFIG:
                    target_delinquency_rate = DELINQUENCY_CONFIG["Q1_2024_RATE"]
                elif year == 2025 and "Q1_2025_RATE" in DELINQUENCY_CONFIG:
                    target_delinquency_rate = DELINQUENCY_CONFIG["Q1_2025_RATE"]
                elif year == 2026 and "Q1_2026_RATE" in DELINQUENCY_CONFIG:
                    target_delinquency_rate = DELINQUENCY_CONFIG["Q1_2026_RATE"]

            is_delinquent_30_plus = random.random() < target_delinquency_rate

            if is_delinquent_30_plus:
                dpd_category_roll = random.random()
                if dpd_category_roll < 0.7: 
                    days_past_due = random.randint(30, 59)
                    delinquency_status = '30-59 DPD'
                elif dpd_category_roll < 0.9: 
                    days_past_due = random.randint(60, 89)
                    delinquency_status = '60-89 DPD'
                else: 
                    days_past_due = random.randint(90, 120)
                    delinquency_status = '90+ DPD'
            else:
                days_past_due = 0
                delinquency_status = 'Current'
        elif outstanding_balance > 0 : 
            delinquency_status = 'Current (Low Balance)'
            minimum_payment_due = outstanding_balance 
            month_of_snapshot = snapshot_date_dt.replace(day=1)
            payment_due_date = (month_of_snapshot + timedelta(days=random.randint(20,25))).date()
        
        accounts_df.loc[idx, 'MinimumPaymentDueAtSnapshot'] = minimum_payment_due
        accounts_df.loc[idx, 'PaymentDueDateAtSnapshot'] = payment_due_date
        accounts_df.loc[idx, 'DelinquencyStatusAtSnapshot'] = delinquency_status
        accounts_df.loc[idx, 'DaysPastDueAtSnapshot'] = days_past_due
        
        processed_count +=1
        if processed_count % 1000 == 0: # Adjusted print frequency
             print(f"Processed delinquency snapshot for {processed_count}/{len(active_accounts_indices)} active accounts...")
    print("Finished adding delinquency snapshot to accounts.")
else:
    print("Accounts DataFrame is empty. Skipping delinquency snapshot addition.")


# --- Data Type Conversion and Sorting ---
print("Finalizing DataFrames...")
if not applications_df.empty:
    applications_df['ApplicationDate'] = pd.to_datetime(applications_df['ApplicationDate'])
    applications_df = applications_df.sort_values(by='ApplicationDate').reset_index(drop=True)

if not accounts_df.empty:
    accounts_df['AccountOpenDate'] = pd.to_datetime(accounts_df['AccountOpenDate']).dt.date
    accounts_df['ActivationDate'] = pd.to_datetime(accounts_df['ActivationDate'], errors='coerce').dt.date
    if 'SnapshotDate' in accounts_df.columns:
        accounts_df['SnapshotDate'] = pd.to_datetime(accounts_df['SnapshotDate'], errors='coerce').dt.date
    if 'PaymentDueDateAtSnapshot' in accounts_df.columns:
        accounts_df['PaymentDueDateAtSnapshot'] = pd.to_datetime(accounts_df['PaymentDueDateAtSnapshot'], errors='coerce').dt.date
    accounts_df = accounts_df.sort_values(by='AccountOpenDate', na_position='last').reset_index(drop=True)

if not transactions_df.empty:
    transactions_df['TransactionDate'] = pd.to_datetime(transactions_df['TransactionDate'])
    transactions_df = transactions_df.sort_values(by='TransactionDate').reset_index(drop=True)

# --- Save to CSV ---
print("Saving data to CSV files...")
try:
    if not applications_df.empty:
        applications_df.to_csv('applications.csv', index=False, date_format='%Y-%m-%d %H:%M:%S')
    else: print("Applications DataFrame is empty. Skipping save.")

    if not accounts_df.empty:
        accounts_df.to_csv('accounts.csv', index=False, date_format='%Y-%m-%d') 
    else: print("Accounts DataFrame is empty. Skipping save.")

    if not transactions_df.empty:
        transactions_df.to_csv('transactions.csv', index=False, date_format='%Y-%m-%d %H:%M:%S')
    else: print("Transactions DataFrame is empty. Skipping save.")

    print("Finished saving available data.")
except Exception as e:
    print(f"Error saving files: {e}")

