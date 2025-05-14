import subprocess
import tempfile
import os
import pandas as pd
import sys
from datetime import datetime

class LoanRiskGenerator:
    def __init__(self, **params):
        """Initialize the Loan & Risk Data Generator with parameters."""
        self.params = params
    
    @staticmethod
    def get_config():
        """Return configuration for UI parameter generation."""
        return {
            'name': 'Loan & Risk Performance',
            'description': 'Generate company risk profiles, historical risk data, and network connections',
            'parameters': {
                'num_companies': {
                    'type': 'number',
                    'label': 'Number of Companies',
                    'min': 10,
                    'max': 500,
                    'default': 50,
                    'help': 'Number of companies to generate profiles for'
                },
                'include_historical': {
                    'type': 'boolean',
                    'label': 'Include Historical Data',
                    'default': True,
                    'help': 'Generate 12 months of historical risk data for each company'
                },
                'include_network': {
                    'type': 'boolean',
                    'label': 'Include Network Connections',
                    'default': True,
                    'help': 'Generate network connections between companies'
                },
                'risk_trend': {
                    'type': 'select',
                    'label': 'Risk Trend Direction',
                    'options': ['Stable', 'Increasing', 'Decreasing'],
                    'default_index': 0,
                    'help': 'Overall trend direction for risk scores over time'
                },
                'industry_focus': {
                    'type': 'select',
                    'label': 'Industry Focus',
                    'options': ['All Industries', 'Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Energy', 'Retail', 'Logistics'],
                    'default_index': 0,
                    'help': 'Focus on specific industry or all industries'
                }
            }
        }
    
    def generate(self):
        """Execute the original script and return generated DataFrames."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy the original script to temp directory
            script_path = os.path.join(os.path.dirname(__file__), 'LoanandRisk.py')
            temp_script_path = os.path.join(temp_dir, 'LoanandRisk.py')
            
            # Read the original script
            with open(script_path, 'r') as f:
                script_content = f.read()
            
            # Modify configuration based on parameters
            modifications = []
            
            # Modify number of companies
            if 'num_companies' in self.params:
                num_companies = self.params['num_companies']
                modifications.append(
                    ('def generate_company_profiles(num_companies=50):',
                     f'def generate_company_profiles(num_companies={num_companies}):')
                )
            
            # Filter by industry if specified
            if self.params.get('industry_focus') and self.params['industry_focus'] != 'All Industries':
                industry_focus = self.params['industry_focus']
                # Modify the industries list to only include the selected industry
                modifications.append(
                    ('industries = [\'Technology\', \'Finance\', \'Healthcare\', \'Manufacturing\', \'Energy\', \'Retail\', \'Logistics\']',
                     f'industries = [\'{industry_focus}\']')
                )
            
            # Modify risk trend if specified
            if self.params.get('risk_trend'):
                trend = self.params['risk_trend']
                if trend == 'Increasing':
                    # Change the trend logic in historical data
                    modifications.append(
                        ('(2 if idx <= 6 else -3)  # Slight downward trend in later months',
                         '(3 if idx <= 6 else 1)  # Increasing trend')
                    )
                elif trend == 'Decreasing':
                    modifications.append(
                        ('(2 if idx <= 6 else -3)  # Slight downward trend in later months',
                         '(-1 if idx <= 6 else -4)  # Decreasing trend')
                    )
            
            # Apply modifications
            for old_text, new_text in modifications:
                script_content = script_content.replace(old_text, new_text)
            
            # Conditionally exclude generating certain datasets
            if not self.params.get('include_historical', True):
                # Comment out historical data generation
                script_content = script_content.replace(
                    '# Generate historical data\n    historical_df = generate_historical_data(companies_df)',
                    '# Generate historical data (disabled)\n    # historical_df = generate_historical_data(companies_df)\n    historical_df = pd.DataFrame()'
                )
                script_content = script_content.replace(
                    'historical_df.to_csv(\'historical_risk.csv\', index=False)',
                    '# historical_df.to_csv(\'historical_risk.csv\', index=False)'
                )
            
            if not self.params.get('include_network', True):
                # Comment out network connections generation
                script_content = script_content.replace(
                    '# Generate network connections\n    connections_df = generate_network_connections(companies_df)',
                    '# Generate network connections (disabled)\n    # connections_df = generate_network_connections(companies_df)\n    connections_df = pd.DataFrame()'
                )
                script_content = script_content.replace(
                    'connections_df.to_csv(\'network_connections.csv\', index=False)',
                    '# connections_df.to_csv(\'network_connections.csv\', index=False)'
                )
            
            # Write modified script
            with open(temp_script_path, 'w') as f:
                f.write(script_content)
            
            # Change to temp directory and execute script
            original_dir = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                # Execute the script
                result = subprocess.run(
                    [sys.executable, 'LoanandRisk.py'],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    raise Exception(f"Script execution failed: {result.stderr}")
                
                # Read the generated CSV files
                dataframes = {}
                
                # Always read company profiles
                if os.path.exists('company_profiles.csv'):
                    dataframes['company_profiles'] = pd.read_csv('company_profiles.csv')
                
                # Conditionally read other files
                if self.params.get('include_historical', True) and os.path.exists('historical_risk.csv'):
                    dataframes['historical_risk'] = pd.read_csv('historical_risk.csv')
                
                if self.params.get('include_network', True) and os.path.exists('network_connections.csv'):
                    dataframes['network_connections'] = pd.read_csv('network_connections.csv')
                
                if not dataframes:
                    raise Exception("No data files were generated")
                
                return dataframes
                
            finally:
                os.chdir(original_dir)