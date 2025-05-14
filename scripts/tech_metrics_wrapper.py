# scripts/tech_metrics_wrapper.py

import sys
import os
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import pandas as pd
from typing import Dict, Any
import tempfile
import shutil
import subprocess


class TechMetricsGenerator:
    """Wrapper for the original tech_metrics.py script"""
    
    def __init__(self, **params):
        """Initialize with parameters that will override script defaults"""
        self.params = params
        
    @staticmethod
    def get_config() -> Dict[str, Any]:
        """Return configuration for UI generation"""
        return {
            'name': 'Tech Product & Project Management',
            'description': 'Generate product metrics, team data, campaigns, customer feedback, and support tickets',
            'parameters': {
                'num_products': {
                    'type': 'number',
                    'label': 'Number of Products',
                    'default': 15,
                    'min': 1,
                    'max': 100,
                    'help': 'Number of unique products to generate'
                },
                'num_teams': {
                    'type': 'number',
                    'label': 'Number of Teams',
                    'default': 10,
                    'min': 1,
                    'max': 50,
                    'help': 'Number of development teams'
                },
                'num_campaigns': {
                    'type': 'number',
                    'label': 'Number of Campaigns',
                    'default': 10,
                    'min': 1,
                    'max': 100,
                    'help': 'Number of marketing campaigns'
                },
                'num_customers': {
                    'type': 'number',
                    'label': 'Number of Customers',
                    'default': 5000,
                    'min': 100,
                    'max': 50000,
                    'help': 'Number of unique customers'
                }
            }
        }
    
    def generate(self) -> Dict[str, pd.DataFrame]:
        """Run the original script and capture the generated DataFrames"""
        # Create a temporary directory for output files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy the original script to temp directory
            original_script = os.path.join(os.path.dirname(__file__), 'tech_metrics.py')
            temp_script = os.path.join(temp_dir, 'tech_metrics.py')
            
            # Read the original script
            with open(original_script, 'r') as f:
                script_content = f.read()
            
            # Modify the script to use our parameters
            modifications = f"""
# Configuration overrides
NUM_PRODUCTS = {self.params.get('num_products', 15)}
NUM_TEAMS = {self.params.get('num_teams', 10)}
NUM_CAMPAIGNS = {self.params.get('num_campaigns', 10)}
NUM_CUSTOMERS = {self.params.get('num_customers', 5000)}

"""
            # Replace the original configuration section
            script_content = script_content.replace("# --- Configuration ---", f"# --- Configuration ---\n{modifications}")
            
            # Save modified script
            with open(temp_script, 'w') as f:
                f.write(script_content)
            
            # Change to temp directory and run the script
            original_dir = os.getcwd()
            try:
                os.chdir(temp_dir)
                
                # Execute the script using subprocess to isolate it
                result = subprocess.run([sys.executable, 'tech_metrics.py'], 
                                      capture_output=True, 
                                      text=True)
                
                if result.returncode != 0:
                    print(f"Script error: {result.stderr}")
                    raise Exception(f"Script execution failed: {result.stderr}")
                
                # Read the generated CSV files
                dataframes = {}
                
                csv_files = {
                    'dim_product': 'dim_product.csv',
                    'dim_team': 'dim_team.csv',
                    'dim_campaign': 'dim_campaign.csv',
                    'fact_daily_metrics': 'fact_daily_product_metrics.csv',
                    'log_customer_feedback': 'log_customer_feedback.csv',
                    'log_support_ticket': 'log_support_ticket.csv'
                }
                
                for key, filename in csv_files.items():
                    file_path = os.path.join(temp_dir, filename)
                    if os.path.exists(file_path):
                        dataframes[key] = pd.read_csv(file_path)
                        print(f"Loaded {filename}: {len(dataframes[key])} rows")
                    else:
                        print(f"Warning: {filename} not found")
                
                if not dataframes:
                    raise Exception("No data files were generated")
                
                return dataframes
                
            finally:
                # Restore original directory
                os.chdir(original_dir)