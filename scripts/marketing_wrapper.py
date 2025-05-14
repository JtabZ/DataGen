import subprocess
import tempfile
import os
import pandas as pd
import sys
from datetime import datetime

class MarketingDataGenerator:
    def __init__(self, **params):
        """Initialize the Marketing Data Generator with parameters."""
        self.params = params
    
    @staticmethod
    def get_config():
        """Return configuration for UI parameter generation."""
        return {
            'name': 'Marketing Funnel Data',
            'description': 'Generate marketing funnel data with channels, campaigns, and conversion metrics',
            'parameters': {
                'num_days': {
                    'type': 'number',
                    'label': 'Number of Days to Generate',
                    'min': 30,
                    'max': 1500,
                    'default': 365,
                    'help': 'Number of days of data to generate'
                },
                'start_date': {
                    'type': 'date',
                    'label': 'Start Date',
                    'default': datetime(2023, 1, 1),
                    'help': 'Starting date for data generation'
                },
                'end_date': {
                    'type': 'date',
                    'label': 'End Date',
                    'default': datetime(2025, 12, 31),
                    'help': 'Ending date for data generation'
                },
                'include_future_campaigns': {
                    'type': 'boolean',
                    'label': 'Include Future Campaigns',
                    'default': True,
                    'help': 'Include campaigns scheduled for future dates'
                },
                'channel_focus': {
                    'type': 'select',
                    'label': 'Channel Focus',
                    'options': ['All Channels', 'Organic', 'Paid', 'Email', 'Social'],
                    'default_index': 0,
                    'help': 'Focus on specific marketing channels'
                }
            }
        }
    
    def generate(self):
        """Execute the original script and return generated DataFrames."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Copy the original script to temp directory
            script_path = os.path.join(os.path.dirname(__file__), 'MarketingFunnelData.py')
            temp_script_path = os.path.join(temp_dir, 'MarketingFunnelData.py')
            
            # Read the original script
            with open(script_path, 'r') as f:
                script_content = f.read()
            
            # Modify configuration based on parameters
            modifications = []
            
            # Modify date range if specified
            if 'start_date' in self.params:
                start_date_str = self.params['start_date'].strftime("%Y, %m, %d")
                modifications.append(
                    ('START_DATE = TODAY - datetime.timedelta(days=3*365)',
                     f'START_DATE = datetime.date({start_date_str})')
                )
            
            if 'end_date' in self.params:
                end_date_str = self.params['end_date'].strftime("%Y, %m, %d")
                modifications.append(
                    ('END_DATE = TODAY + datetime.timedelta(days=1*365)',
                     f'END_DATE = datetime.date({end_date_str})')
                )
            
            # Handle channel focus
            if self.params.get('channel_focus') and self.params['channel_focus'] != 'All Channels':
                channel_focus = self.params['channel_focus']
                if channel_focus == 'Organic':
                    new_channels = ["Organic Search", "Referral", "Direct"]
                elif channel_focus == 'Paid':
                    new_channels = ["Paid Search", "Paid Social - ConnectSphere", "Paid Social - PixelVerse"]
                elif channel_focus == 'Email':
                    new_channels = ["Email Marketing"]
                elif channel_focus == 'Social':
                    new_channels = ["Paid Social - ConnectSphere", "Paid Social - PixelVerse"]
                
                channels_str = str(new_channels)
                modifications.append(
                    ('CHANNELS = ["Organic Search", "Paid Search", "Paid Social - ConnectSphere", "Paid Social - PixelVerse", "Email Marketing", "Referral", "Direct", "AI ContentSynergy"]',
                     f'CHANNELS = {channels_str}')
                )
            
            # Filter out future campaigns if requested
            if not self.params.get('include_future_campaigns', True):
                modifications.append(
                    ('# --- Future Campaigns ---',
                     '# --- Future Campaigns --- (Disabled)\n    """\n')
                )
                # Find and comment out future campaigns
                future_campaign_start = script_content.find('# --- Future Campaigns ---')
                if future_campaign_start != -1:
                    future_campaign_end = script_content.find(']', future_campaign_start)
                    if future_campaign_end != -1:
                        # Comment out the future campaigns section
                        before = script_content[:future_campaign_start]
                        future_section = script_content[future_campaign_start:future_campaign_end]
                        after = script_content[future_campaign_end:]
                        
                        # Comment out the future campaigns
                        commented_section = '\n'.join(['    # ' + line for line in future_section.split('\n')])
                        script_content = before + commented_section + '\n    # End commented section\n' + after
            
            # Apply modifications
            for old_text, new_text in modifications:
                script_content = script_content.replace(old_text, new_text)
            
            # Change output filename
            script_content = script_content.replace(
                'OUTPUT_FILENAME = "marketing_funnel_data_v3.csv"',
                'OUTPUT_FILENAME = "marketing_funnel_data.csv"'
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
                    [sys.executable, 'MarketingFunnelData.py'],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    raise Exception(f"Script execution failed: {result.stderr}")
                
                # Read the generated CSV file
                csv_path = os.path.join(temp_dir, 'marketing_funnel_data.csv')
                
                if not os.path.exists(csv_path):
                    raise Exception("CSV file was not generated")
                
                # Read the CSV
                df = pd.read_csv(csv_path)
                
                # Convert date column to datetime if it exists
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'])
                
                # Return as a dictionary with a single DataFrame
                return {
                    'marketing_funnel_data': df
                }
                
            finally:
                os.chdir(original_dir)