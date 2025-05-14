# scripts/tech_metrics_wrapper.py

import sys
import os
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
import pandas as pd
from typing import Dict, Any


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
        # Import the original script here to avoid running it at module load time
        import importlib.util
        import tempfile
        
        # Load the original script
        script_path = os.path.join(os.path.dirname(__file__), 'tech_metrics.py')
        spec = importlib.util.spec_from_file_location("tech_metrics", script_path)
        tech_metrics = importlib.util.module_from_spec(spec)
        
        # Temporarily change the working directory to avoid saving files
        original_dir = os.getcwd()
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                os.chdir(temp_dir)
                
                # Capture stdout to suppress print statements
                with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
                    # Set configuration values in the module
                    tech_metrics.NUM_PRODUCTS = self.params.get('num_products', 15)
                    tech_metrics.NUM_TEAMS = self.params.get('num_teams', 10)
                    tech_metrics.NUM_CAMPAIGNS = self.params.get('num_campaigns', 10)
                    tech_metrics.NUM_CUSTOMERS = self.params.get('num_customers', 5000)
                    
                    # Execute the script
                    spec.loader.exec_module(tech_metrics)
                
                # Read the generated CSV files
                dataframes = {}
                
                if os.path.exists('dim_product.csv'):
                    dataframes['dim_product'] = pd.read_csv('dim_product.csv')
                if os.path.exists('dim_team.csv'):
                    dataframes['dim_team'] = pd.read_csv('dim_team.csv')
                if os.path.exists('dim_campaign.csv'):
                    dataframes['dim_campaign'] = pd.read_csv('dim_campaign.csv')
                if os.path.exists('fact_daily_product_metrics.csv'):
                    dataframes['fact_daily_metrics'] = pd.read_csv('fact_daily_product_metrics.csv')
                if os.path.exists('log_customer_feedback.csv'):
                    dataframes['log_customer_feedback'] = pd.read_csv('log_customer_feedback.csv')
                if os.path.exists('log_support_ticket.csv'):
                    dataframes['log_support_ticket'] = pd.read_csv('log_support_ticket.csv')
                
                return dataframes
                
        finally:
            # Restore original directory
            os.chdir(original_dir)