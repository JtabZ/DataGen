import subprocess
import tempfile
import os
import pandas as pd
import sys
from datetime import datetime

class TaxDataGenerator:
    def __init__(self, **params):
        """Initialize the Tax Data Generator with parameters."""
        self.params = params
    
    @staticmethod
    def get_config():
        """Return configuration for UI parameter generation."""
        return {
            'name': 'Tax Data',
            'description': 'Generate tax filing data with locations, returns, and customer information',
            'parameters': {
                'num_locations': {
                    'type': 'number',
                    'label': 'Number of Locations',
                    'min': 50,
                    'max': 500,
                    'default': 150,
                    'help': 'Number of tax service locations to generate'
                },
                'num_filings': {
                    'type': 'number',
                    'label': 'Number of Filings',
                    'min': 1000,
                    'max': 200000,
                    'default': 50000,
                    'help': 'Total number of tax filings to generate'
                },
                'current_date': {
                    'type': 'date',
                    'label': 'Current Date',
                    'default': datetime(2025, 4, 1),
                    'help': 'Current date for filtering filing dates'
                },
                'tax_years': {
                    'type': 'select',
                    'label': 'Tax Years Range',
                    'options': ['2022-2024', '2021-2023', '2023-2025', '2022-2025'],
                    'default_index': 0,
                    'help': 'Range of tax years to include in filings'
                },
                'region_focus': {
                    'type': 'select',
                    'label': 'Region Focus',
                    'options': ['All Regions', 'Northeast', 'South', 'Midwest', 'West'],
                    'default_index': 0,
                    'help': 'Focus on specific US regions or all regions'
                },
                'complexity_bias': {
                    'type': 'select',
                    'label': 'Complexity Bias',
                    'options': ['Balanced', 'More Simple', 'More Complex'],
                    'default_index': 0,
                    'help': 'Bias the distribution of return complexity levels'
                },
                'customer_type_ratio': {
                    'type': 'number',
                    'label': 'Returning Customer Ratio (%)',
                    'min': 20,
                    'max': 80,
                    'default': 50,
                    'help': 'Approximate percentage of returning customers'
                }
            }
        }
    
    def generate(self):
        """Execute the original script and return generated DataFrames."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy the original script to temp directory
            script_path = os.path.join(os.path.dirname(__file__), 'TaxData.py')
            temp_script_path = os.path.join(temp_dir, 'TaxData.py')
            
            # Read the original script
            with open(script_path, 'r') as f:
                script_content = f.read()
            
            # Modify configuration based on parameters
            modifications = []
            
            # Modify number of locations
            if 'num_locations' in self.params:
                num_locations = self.params['num_locations']
                modifications.append(
                    ('NUM_LOCATIONS = 150',
                     f'NUM_LOCATIONS = {num_locations}')
                )
            
            # Modify number of filings
            if 'num_filings' in self.params:
                num_filings = self.params['num_filings']
                modifications.append(
                    ('NUM_FILINGS = 50000',
                     f'NUM_FILINGS = {num_filings}')
                )
            
            # Modify current date
            if 'current_date' in self.params:
                current_date = self.params['current_date']
                date_str = f"datetime({current_date.year}, {current_date.month}, {current_date.day})"
                modifications.append(
                    ('CURRENT_DATE = datetime(2025, 4, 1)',
                     f'CURRENT_DATE = {date_str}')
                )
            
            # Modify tax years
            if self.params.get('tax_years'):
                tax_years_range = self.params['tax_years']
                if tax_years_range == '2022-2024':
                    tax_years_list = '[2022, 2023, 2024]'
                elif tax_years_range == '2021-2023':
                    tax_years_list = '[2021, 2022, 2023]'
                elif tax_years_range == '2023-2025':
                    tax_years_list = '[2023, 2024, 2025]'
                elif tax_years_range == '2022-2025':
                    tax_years_list = '[2022, 2023, 2024, 2025]'
                
                modifications.append(
                    ('TAX_YEARS = [2022, 2023, 2024]',
                     f'TAX_YEARS = {tax_years_list}')
                )
            
            # Filter by region if specified
            if self.params.get('region_focus') and self.params['region_focus'] != 'All Regions':
                region_focus = self.params['region_focus']
                
                # Filter states by region
                region_states = {
                    'Northeast': "['CT', 'ME', 'MA', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT']",
                    'South': "['DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX']",
                    'Midwest': "['IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI']",
                    'West': "['ID', 'MT', 'WY', 'CO', 'NM', 'AZ', 'UT', 'NV', 'CA', 'OR', 'WA']"
                }
                
                if region_focus in region_states:
                    # Add code to filter states after the states list is created
                    filter_code = f"""
# Filter states by region focus
states = {region_states[region_focus]}
# Update states_cities to only include selected states
filtered_states_cities = {{}}
for state in states:
    if state in states_cities:
        filtered_states_cities[state] = states_cities[state]
states_cities = filtered_states_cities
"""
                    script_content = script_content.replace(
                        'states = list(states_cities.keys())',
                        f'states = list(states_cities.keys())\n{filter_code}'
                    )
            
            # Modify complexity bias
            if self.params.get('complexity_bias'):
                complexity_bias = self.params['complexity_bias']
                if complexity_bias == 'More Simple':
                    # Adjust AGI distribution to favor lower incomes
                    modifications.append(
                        ('agi = max(1000, round(np.random.lognormal(mean=10.5, sigma=0.6), -2))',
                         'agi = max(1000, round(np.random.lognormal(mean=9.8, sigma=0.5), -2))')
                    )
                    # Adjust Schedule C probability
                    modifications.append(
                        ('schedule_c_prob = 0.1 + (0.2 if 20000 < agi < 100000 else 0)',
                         'schedule_c_prob = 0.05 + (0.1 if 20000 < agi < 100000 else 0)')
                    )
                elif complexity_bias == 'More Complex':
                    # Adjust AGI distribution to favor higher incomes
                    modifications.append(
                        ('agi = max(1000, round(np.random.lognormal(mean=10.5, sigma=0.6), -2))',
                         'agi = max(1000, round(np.random.lognormal(mean=11.2, sigma=0.7), -2))')
                    )
                    # Adjust Schedule C probability
                    modifications.append(
                        ('schedule_c_prob = 0.1 + (0.2 if 20000 < agi < 100000 else 0)',
                         'schedule_c_prob = 0.2 + (0.3 if 20000 < agi < 100000 else 0)')
                    )
            
            # Implement returning customer ratio
            if 'customer_type_ratio' in self.params:
                ratio = self.params['customer_type_ratio'] / 100.0
                # Add code to bias customer type assignment
                customer_logic = f"""
    # Modified customer type logic with custom ratio
    if first_seen_year is None:
        if random.random() < {ratio}:
            # Pretend they're returning by assigning an earlier year
            customer_type = 'Returning'
            customer_first_year[customer_proxy_key] = tax_year - 1
        else:
            customer_type = 'New'
            customer_first_year[customer_proxy_key] = tax_year
    elif tax_year == first_seen_year:
        customer_type = 'New'
    else:
        customer_type = 'Returning'
"""
                # Replace the original customer type logic
                script_content = script_content.replace(
                    """    first_seen_year = customer_first_year.get(customer_proxy_key)
    if first_seen_year is None:
        customer_type = 'New'
        customer_first_year[customer_proxy_key] = tax_year
    elif tax_year == first_seen_year:
        customer_type = 'New'
    else:
        customer_type = 'Returning'""",
                    f"""    first_seen_year = customer_first_year.get(customer_proxy_key)
{customer_logic}"""
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
                    [sys.executable, 'TaxData.py'],
                    capture_output=True,
                    text=True,
                    timeout=300  # Add timeout
                )
                
                if result.returncode != 0:
                    raise Exception(f"Script execution failed: {result.stderr}")
                
                # Read the generated CSV files
                dataframes = {}
                
                # Read locations
                if os.path.exists('locations.csv'):
                    dataframes['locations'] = pd.read_csv('locations.csv')
                
                # Read filings
                if os.path.exists('filings.csv'):
                    df = pd.read_csv('filings.csv')
                    # Convert date column
                    if 'Filing_Date' in df.columns:
                        df['Filing_Date'] = pd.to_datetime(df['Filing_Date'])
                    dataframes['filings'] = df
                
                if not dataframes:
                    raise Exception("No data files were generated")
                
                return dataframes
                
            except subprocess.TimeoutExpired:
                raise Exception("Script execution timed out. Try reducing the number of filings.")
            finally:
                os.chdir(original_dir)