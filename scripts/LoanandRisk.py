import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)

# Company name components
company_prefixes = ['Global', 'Inter', 'Trans', 'Meta', 'Apex', 'Neo', 'Cyber', 'Tech']
company_suffixes = ['Corp', 'Systems', 'Solutions', 'Dynamics', 'Industries', 'Group', 'Holdings']
industries = ['Technology', 'Finance', 'Healthcare', 'Manufacturing', 'Energy', 'Retail', 'Logistics']
countries = ['USA', 'UK', 'Germany', 'France', 'Japan', 'Singapore', 'Australia', 'Canada']

def generate_company_profiles(num_companies=50):
    companies = []
    
    for id in range(num_companies):
        name = f"{random.choice(company_prefixes)}{random.choice(company_suffixes)}"
        industry = random.choice(industries)
        country = random.choice(countries)
        
        # Generate risk scores (1-100)
        financial_risk = random.randint(20, 90)
        compliance_risk = random.randint(15, 85)
        reputational_risk = random.randint(10, 95)
        operational_risk = random.randint(25, 88)
        
        # Calculate composite risk score with some randomization
        composite_risk = min(
            100,
            round((financial_risk * 0.3 + compliance_risk * 0.25 + 
                   reputational_risk * 0.2 + operational_risk * 0.25) * 
                  (0.9 + random.random() * 0.2))
        )
        
        companies.append({
            'id': id,
            'name': name,
            'industry': industry,
            'country': country,
            'financialRisk': financial_risk,
            'complianceRisk': compliance_risk,
            'reputationalRisk': reputational_risk,
            'operationalRisk': operational_risk,
            'compositeRisk': composite_risk
        })
    
    return pd.DataFrame(companies)

def generate_historical_data(companies_df):
    historical_data = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    for _, company in companies_df.iterrows():
        current_risk = company['compositeRisk']
        
        for idx, month in enumerate(months):
            # Add some random variation to risk scores over time
            current_risk = min(100, max(1, 
                current_risk + random.randint(-8, 8) + 
                (2 if idx <= 6 else -3)  # Slight downward trend in later months
            ))
            
            historical_data.append({
                'companyId': company['id'],
                'companyName': company['name'],
                'industry': company['industry'],
                'country': company['country'],
                'month': month,
                'monthIndex': idx + 1,
                'riskScore': current_risk
            })
    
    return pd.DataFrame(historical_data)

def generate_network_connections(companies_df):
    connections = []
    
    for _, company in companies_df.iterrows():
        # Each company has 2-5 connections
        num_connections = random.randint(2, 5)
        possible_connections = companies_df[companies_df['id'] != company['id']]
        
        for _ in range(num_connections):
            target = possible_connections.sample(n=1).iloc[0]
            strength = round(random.random(), 2)
            
            connections.append({
                'sourceId': company['id'],
                'sourceName': company['name'],
                'targetId': target['id'],
                'targetName': target['name'],
                'connectionStrength': strength,
                'riskPropagation': round(strength * company['compositeRisk'])
            })
    
    return pd.DataFrame(connections)

def main():
    # Generate company profiles
    companies_df = generate_company_profiles()
    
    # Generate historical data
    historical_df = generate_historical_data(companies_df)
    
    # Generate network connections
    connections_df = generate_network_connections(companies_df)
    
    # Save to CSV files
    companies_df.to_csv('company_profiles.csv', index=False)
    historical_df.to_csv('historical_risk.csv', index=False)
    connections_df.to_csv('network_connections.csv', index=False)
    
    print("Generated files:")
    print("1. company_profiles.csv")
    print("2. historical_risk.csv")
    print("3. network_connections.csv")

if __name__ == "__main__":
    main()