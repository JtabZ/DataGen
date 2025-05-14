import subprocess
import tempfile
import os
import pandas as pd
import sys
from datetime import datetime

class CreditCardGenerator:
    def __init__(self, **params):
        """Initialize the Credit Card Application Data Generator with parameters."""
        self.params = params
    
    @staticmethod
    def get_config():
        """Return configuration for UI parameter generation."""
        return {
            'name': 'Credit Card Applications',
            'description': 'Generate credit card application data, accounts, transactions, and delinquency metrics',
            'parameters': {
                'num_cardholders': {
                    'type': 'number',
                    'label': 'Number of Cardholders',
                    'min': 100,
                    'max': 5000,
                    'default': 750,
                    'help': 'Number of unique cardholders to generate'
                },
                'avg_apps_per_day': {
                    'type': 'number',
                    'label': 'Average Applications per Day',
                    'min': 5,
                    'max': 100,
                    'default': 30,
                    'help': 'Average number of applications submitted per day'
                },
                'start_date': {
                    'type': 'date',
                    'label': 'Start Date',
                    'default': datetime(2023, 5, 1),
                    'help': 'Starting date for data generation'
                },
                'end_date': {
                    'type': 'date',
                    'label': 'End Date',
                    'default': datetime(2026, 5, 1),
                    'help': 'Ending date for data generation'
                },
                'approval_rate': {
                    'type': 'number',
                    'label': 'Approval Rate (%)',
                    'min': 10,
                    'max': 90,
                    'default': 55,
                    'help': 'Percentage of applications that are approved'
                },
                'activation_rate': {
                    'type': 'number',
                    'label': 'Activation Rate (%)',
                    'min': 50,
                    'max': 95,
                    'default': 85,
                    'help': 'Percentage of approved accounts that are activated'
                },
                'delinquency_trend': {
                    'type': 'select',
                    'label': 'Delinquency Trend',
                    'options': ['Default (Q1 Improvements)', 'Stable', 'Increasing', 'Decreasing'],
                    'default_index': 0,
                    'help': 'Trend for delinquency rates over time'
                },
                'state_focus': {
                    'type': 'select',
                    'label': 'State Focus',
                    'options': ['All States', 'West Coast', 'East Coast', 'Midwest', 'South'],
                    'default_index': 0,
                    'help': 'Focus applications on specific regions'
                }
            }
        }
    
    def generate(self):
        """Execute the original script and return generated DataFrames."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy the original script to temp directory
            script_path = os.path.join(os.path.dirname(__file__), 'CreditCardApplicationData.py')
            temp_script_path = os.path.join(temp_dir, 'CreditCardApplicationData.py')
            
            # Read the original script
            with open(script_path, 'r') as f:
                script_content = f.read()
            
            # Modify configuration based on parameters
            modifications = []
            
            # Modify date range
            if 'start_date' in self.params:
                start_date = self.params['start_date']
                start_date_str = f"datetime({start_date.year}, {start_date.month}, {start_date.day})"
                modifications.append(
                    ('START_DATE = datetime(2023, 5, 1)',
                     f'START_DATE = {start_date_str}')
                )
            
            if 'end_date' in self.params:
                end_date = self.params['end_date']
                end_date_str = f"datetime({end_date.year}, {end_date.month}, {end_date.day})"
                modifications.append(
                    ('END_DATE = datetime(2026, 5, 1)',
                     f'END_DATE = {end_date_str}')
                )
            
            # Modify cardholder count
            if 'num_cardholders' in self.params:
                num_cardholders = self.params['num_cardholders']
                modifications.append(
                    ('NUM_CARDHOLDERS = 750',
                     f'NUM_CARDHOLDERS = {num_cardholders}')
                )
            
            # Modify applications per day
            if 'avg_apps_per_day' in self.params:
                avg_apps = self.params['avg_apps_per_day']
                modifications.append(
                    ('AVG_APPS_PER_DAY = 30',
                     f'AVG_APPS_PER_DAY = {avg_apps}')
                )
            
            # Modify approval rate
            if 'approval_rate' in self.params:
                approval_rate = self.params['approval_rate'] / 100.0  # Convert percentage to decimal
                modifications.append(
                    ('APPROVAL_RATE = 0.55',
                     f'APPROVAL_RATE = {approval_rate}')
                )
            
            # Modify activation rate
            if 'activation_rate' in self.params:
                activation_rate = self.params['activation_rate'] / 100.0  # Convert percentage to decimal
                modifications.append(
                    ('ACTIVATION_RATE = 0.85',
                     f'ACTIVATION_RATE = {activation_rate}')
                )
            
            # Modify delinquency trend
            if self.params.get('delinquency_trend'):
                trend = self.params['delinquency_trend']
                if trend == 'Stable':
                    # Make all quarters the same
                    modifications.append(
                        ('"Q1_2024_RATE": 0.065',
                         '"Q1_2024_RATE": 0.07')
                    )
                    modifications.append(
                        ('"Q1_2025_RATE": 0.059',
                         '"Q1_2025_RATE": 0.07')
                    )
                    modifications.append(
                        ('"Q1_2026_RATE": 0.055',
                         '"Q1_2026_RATE": 0.07')
                    )
                elif trend == 'Increasing':
                    modifications.append(
                        ('"Q1_2024_RATE": 0.065',
                         '"Q1_2024_RATE": 0.065')
                    )
                    modifications.append(
                        ('"Q1_2025_RATE": 0.059',
                         '"Q1_2025_RATE": 0.075')
                    )
                    modifications.append(
                        ('"Q1_2026_RATE": 0.055',
                         '"Q1_2026_RATE": 0.085')
                    )
                elif trend == 'Decreasing':
                    modifications.append(
                        ('"Q1_2024_RATE": 0.065',
                         '"Q1_2024_RATE": 0.08')
                    )
                    modifications.append(
                        ('"Q1_2025_RATE": 0.059',
                         '"Q1_2025_RATE": 0.06')
                    )
                    modifications.append(
                        ('"Q1_2026_RATE": 0.055',
                         '"Q1_2026_RATE": 0.04')
                    )
            
            # Modify state focus - simplified approach
            if self.params.get('state_focus') and self.params['state_focus'] != 'All States':
                state_focus = self.params['state_focus']
                if state_focus == 'West Coast':
                    states_list = "['CA', 'OR', 'WA', 'NV', 'AZ']"
                elif state_focus == 'East Coast':
                    states_list = "['NY', 'NJ', 'CT', 'MA', 'ME', 'VT', 'NH', 'RI', 'PA', 'MD', 'DE', 'VA', 'NC', 'SC', 'GA', 'FL']"
                elif state_focus == 'Midwest':
                    states_list = "['OH', 'IN', 'IL', 'MI', 'WI', 'MN', 'IA', 'MO', 'ND', 'SD', 'NE', 'KS']"
                elif state_focus == 'South':
                    states_list = "['TX', 'OK', 'AR', 'LA', 'MS', 'AL', 'TN', 'KY', 'WV']"
                
                # Find the full STATES definition and replace it
                states_definition = """STATES = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
          'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
          'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
          'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
          'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']"""
                
                modifications.append((states_definition, f"STATES = {states_list}"))
            
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
                    [sys.executable, 'CreditCardApplicationData.py'],
                    capture_output=True,
                    text=True,
                    timeout=300  # Add timeout to prevent hanging
                )
                
                if result.returncode != 0:
                    raise Exception(f"Script execution failed: {result.stderr}")
                
                # Read the generated CSV files
                dataframes = {}
                
                # Read applications
                if os.path.exists('applications.csv'):
                    df = pd.read_csv('applications.csv')
                    if 'ApplicationDate' in df.columns:
                        df['ApplicationDate'] = pd.to_datetime(df['ApplicationDate'])
                    dataframes['applications'] = df
                
                # Read accounts
                if os.path.exists('accounts.csv'):
                    df = pd.read_csv('accounts.csv')
                    # Convert date columns
                    date_columns = ['AccountOpenDate', 'ActivationDate', 'SnapshotDate', 'PaymentDueDateAtSnapshot']
                    for col in date_columns:
                        if col in df.columns:
                            df[col] = pd.to_datetime(df[col], errors='coerce')
                    dataframes['accounts'] = df
                
                # Read transactions
                if os.path.exists('transactions.csv'):
                    df = pd.read_csv('transactions.csv')
                    if 'TransactionDate' in df.columns:
                        df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
                    dataframes['transactions'] = df
                
                if not dataframes:
                    raise Exception("No data files were generated")
                
                return dataframes
                
            except subprocess.TimeoutExpired:
                raise Exception("Script execution timed out. Try reducing the number of cardholders or date range.")
            finally:
                os.chdir(original_dir)