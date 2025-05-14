import subprocess
import tempfile
import os
import pandas as pd
import sys
from datetime import datetime

class FinancialDataGenerator:
    def __init__(self, **params):
        """Initialize the Financial Data Generator with parameters."""
        self.params = params
    
    @staticmethod
    def get_config():
        """Return configuration for UI parameter generation."""
        return {
            'name': 'Financial Statements',
            'description': 'Generate sales transactions, product master data, and financial summaries',
            'parameters': {
                'num_transactions': {
                    'type': 'number',
                    'label': 'Number of Transactions',
                    'min': 1000,
                    'max': 100000,
                    'default': 20000,
                    'help': 'Total number of sales transactions to generate'
                },
                'num_products': {
                    'type': 'number',
                    'label': 'Number of Products',
                    'min': 50,
                    'max': 1000,
                    'default': 150,
                    'help': 'Number of unique products in catalog'
                },
                'num_customers': {
                    'type': 'number',
                    'label': 'Number of Customers',
                    'min': 100,
                    'max': 5000,
                    'default': 500,
                    'help': 'Number of unique customers'
                },
                'start_date': {
                    'type': 'date',
                    'label': 'Start Date',
                    'default': datetime(2023, 1, 1),
                    'help': 'Starting date for transactions'
                },
                'end_date': {
                    'type': 'date',
                    'label': 'End Date',
                    'default': datetime(2025, 12, 31),
                    'help': 'Ending date for transactions'
                },
                'category_focus': {
                    'type': 'select',
                    'label': 'Category Focus',
                    'options': ['All Categories', 'Technology Heavy', 'Supplies Heavy', 'Furniture Heavy', 'Services Heavy'],
                    'default_index': 0,
                    'help': 'Weight transactions toward specific categories'
                },
                'division_focus': {
                    'type': 'select',
                    'label': 'Division Focus',
                    'options': ['Even Distribution', 'North Heavy', 'South Heavy', 'East Heavy', 'West Heavy', 'Corporate Heavy'],
                    'default_index': 0,
                    'help': 'Weight transactions toward specific divisions'
                },
                'margin_profile': {
                    'type': 'select',
                    'label': 'Margin Profile',
                    'options': ['Standard', 'High Margin', 'Low Margin', 'Variable'],
                    'default_index': 0,
                    'help': 'Control profit margin patterns in the data'
                },
                'seasonality': {
                    'type': 'select',
                    'label': 'Seasonality Pattern',
                    'options': ['Standard (Q4 Heavy)', 'Even Distribution', 'Summer Peak', 'Winter Peak'],
                    'default_index': 0,
                    'help': 'Control seasonal patterns in transactions'
                }
            }
        }
    
    def generate(self):
        """Execute the original script and return generated DataFrames."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy the original script to temp directory
            script_path = os.path.join(os.path.dirname(__file__), 'GenericFinancialData.py')
            temp_script_path = os.path.join(temp_dir, 'GenericFinancialData.py')
            
            # Read the original script
            with open(script_path, 'r') as f:
                script_content = f.read()
            
            # Modify configuration based on parameters
            modifications = []
            
            # Modify basic parameters
            if 'num_transactions' in self.params:
                num_transactions = self.params['num_transactions']
                modifications.append(
                    ('num_transactions = 20000',
                     f'num_transactions = {num_transactions}')
                )
            
            if 'num_products' in self.params:
                num_products = self.params['num_products']
                modifications.append(
                    ('num_products = 150',
                     f'num_products = {num_products}')
                )
            
            if 'num_customers' in self.params:
                num_customers = self.params['num_customers']
                modifications.append(
                    ('num_customers = 500',
                     f'num_customers = {num_customers}')
                )
            
            # Modify date range
            if 'start_date' in self.params:
                start_date = self.params['start_date']
                date_str = f"datetime({start_date.year}, {start_date.month}, {start_date.day})"
                modifications.append(
                    ('start_date = datetime(2023, 1, 1)',
                     f'start_date = {date_str}')
                )
            
            if 'end_date' in self.params:
                end_date = self.params['end_date']
                date_str = f"datetime({end_date.year}, {end_date.month}, {end_date.day})"
                modifications.append(
                    ('end_date = datetime(2025, 12, 31)',
                     f'end_date = {date_str}')
                )
            
            # Modify category focus
            if self.params.get('category_focus') and self.params['category_focus'] != 'All Categories':
                category_focus = self.params['category_focus']
                if category_focus == 'Technology Heavy':
                    # Weight technology products more heavily
                    modifications.append(
                        ('category = random.choice(corporate_marketing_categories)',
                         'category = random.choices(corporate_marketing_categories, weights=[0.1, 0.1, 0.6, 0.1, 0.1], k=1)[0]')
                    )
                elif category_focus == 'Supplies Heavy':
                    modifications.append(
                        ('category = random.choice(corporate_marketing_categories)',
                         'category = random.choices(corporate_marketing_categories, weights=[0.6, 0.1, 0.1, 0.1, 0.1], k=1)[0]')
                    )
                elif category_focus == 'Furniture Heavy':
                    modifications.append(
                        ('category = random.choice(corporate_marketing_categories)',
                         'category = random.choices(corporate_marketing_categories, weights=[0.1, 0.6, 0.1, 0.1, 0.1], k=1)[0]')
                    )
                elif category_focus == 'Services Heavy':
                    modifications.append(
                        ('category = random.choice(corporate_marketing_categories)',
                         'category = random.choices(corporate_marketing_categories, weights=[0.1, 0.1, 0.1, 0.6, 0.1], k=1)[0]')
                    )
            
            # Modify division focus
            if self.params.get('division_focus') and self.params['division_focus'] != 'Even Distribution':
                division_focus = self.params['division_focus']
                weights_map = {
                    'North Heavy': '[0.4, 0.15, 0.15, 0.15, 0.15]',
                    'South Heavy': '[0.15, 0.4, 0.15, 0.15, 0.15]',
                    'East Heavy': '[0.15, 0.15, 0.4, 0.15, 0.15]',
                    'West Heavy': '[0.15, 0.15, 0.15, 0.4, 0.15]',
                    'Corporate Heavy': '[0.15, 0.15, 0.15, 0.15, 0.4]'
                }
                if division_focus in weights_map:
                    # Replace all division weight definitions
                    modifications.append(
                        ('division_weights = [0.15, 0.15, 0.15, 0.25, 0.3]',
                         f'division_weights = {weights_map[division_focus]}')
                    )
                    modifications.append(
                        ('division_weights = [0.2, 0.2, 0.2, 0.2, 0.2]',
                         f'division_weights = {weights_map[division_focus]}')
                    )
                    modifications.append(
                        ('division_weights = [0.25, 0.25, 0.2, 0.2, 0.1]',
                         f'division_weights = {weights_map[division_focus]}')
                    )
            
            # Modify margin profile
            if self.params.get('margin_profile'):
                margin_profile = self.params['margin_profile']
                if margin_profile == 'High Margin':
                    # Increase all markup values
                    modifications.append(
                        ('markup = random.uniform(1.3, 2.0)',
                         'markup = random.uniform(1.5, 2.3)')
                    )
                    modifications.append(
                        ('markup = random.uniform(1.2, 1.6)',
                         'markup = random.uniform(1.4, 1.9)')
                    )
                    modifications.append(
                        ('markup = random.uniform(1.5, 2.2)',
                         'markup = random.uniform(1.7, 2.5)')
                    )
                    modifications.append(
                        ('markup = random.uniform(1.2, 1.8)',
                         'markup = random.uniform(1.4, 2.1)')
                    )
                elif margin_profile == 'Low Margin':
                    # Decrease all markup values
                    modifications.append(
                        ('markup = random.uniform(1.3, 2.0)',
                         'markup = random.uniform(1.1, 1.5)')
                    )
                    modifications.append(
                        ('markup = random.uniform(1.2, 1.6)',
                         'markup = random.uniform(1.05, 1.3)')
                    )
                    modifications.append(
                        ('markup = random.uniform(1.5, 2.2)',
                         'markup = random.uniform(1.2, 1.7)')
                    )
                    modifications.append(
                        ('markup = random.uniform(1.2, 1.8)',
                         'markup = random.uniform(1.05, 1.4)')
                    )
                elif margin_profile == 'Variable':
                    # Increase variability
                    modifications.append(
                        ('markup = random.uniform(1.3, 2.0)',
                         'markup = random.uniform(1.0, 2.5)')
                    )
                    modifications.append(
                        ('markup = random.uniform(1.2, 1.6)',
                         'markup = random.uniform(1.0, 2.0)')
                    )
                    modifications.append(
                        ('markup = random.uniform(1.5, 2.2)',
                         'markup = random.uniform(1.1, 2.8)')
                    )
                    modifications.append(
                        ('markup = random.uniform(1.2, 1.8)',
                         'markup = random.uniform(1.0, 2.3)')
                    )
            
            # Modify seasonality pattern
            if self.params.get('seasonality'):
                seasonality = self.params['seasonality']
                if seasonality == 'Even Distribution':
                    # Replace seasonality logic with even distribution
                    new_logic = """        # Even distribution across all months
        random_days = random.randint(0, days_range)
        date = start_date + timedelta(days=random_days)"""
                    
                    old_logic = """        # Create seasonal patterns with more sales in Q4 and fewer in Q1
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
                    break"""
                    
                    modifications.append((old_logic, new_logic))
                
                elif seasonality == 'Summer Peak':
                    modifications.append(
                        ('if month in [10, 11, 12]:  # Q4',
                         'if month in [6, 7, 8]:  # Summer')
                    )
                    modifications.append(
                        ('elif month in [1, 2, 3]:  # Q1',
                         'elif month in [11, 12, 1, 2]:  # Winter')
                    )
                
                elif seasonality == 'Winter Peak':
                    modifications.append(
                        ('if month in [10, 11, 12]:  # Q4',
                         'if month in [11, 12, 1, 2]:  # Winter')
                    )
                    modifications.append(
                        ('elif month in [1, 2, 3]:  # Q1',
                         'elif month in [6, 7, 8]:  # Summer')
                    )
            
            # Apply modifications
            for old_text, new_text in modifications:
                script_content = script_content.replace(old_text, new_text)
            
            # Write modified script
            with open(temp_script_path, 'w') as f:
                f.write(script_content)
            
            # Change to temp directory and execute script
            original_dir = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                # Execute the script
                result = subprocess.run(
                    [sys.executable, 'GenericFinancialData.py'],
                    capture_output=True,
                    text=True,
                    timeout=300  # Add timeout
                )
                
                if result.returncode != 0:
                    raise Exception(f"Script execution failed: {result.stderr}")
                
                # Read the generated CSV files
                dataframes = {}
                
                # Read sales transactions
                if os.path.exists('sales_transactions.csv'):
                    df = pd.read_csv('sales_transactions.csv')
                    # Convert date column
                    if 'TransactionDate' in df.columns:
                        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
                    dataframes['sales_transactions'] = df
                
                # Read product master
                if os.path.exists('product_master.csv'):
                    dataframes['product_master'] = pd.read_csv('product_master.csv')
                
                if not dataframes:
                    raise Exception("No data files were generated")
                
                return dataframes
                
            except subprocess.TimeoutExpired:
                raise Exception("Script execution timed out. Try reducing the number of transactions.")
            finally:
                os.chdir(original_dir)