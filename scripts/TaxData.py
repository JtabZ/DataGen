import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Configuration ---
NUM_LOCATIONS = 150
NUM_FILINGS = 50000 # Number of tax filings to generate
CURRENT_DATE = datetime(2025, 4, 1) # Set the current date for filtering filing dates
TAX_YEARS = [2022, 2023, 2024] # Tax years to include data for

# --- Data Definitions ---

# US States (excluding AK, HI) and sample cities
# Using state abbreviations for easier ID generation
states_cities = {
    'AL': ['Birmingham', 'Montgomery', 'Mobile', 'Huntsville'],
    'AZ': ['Phoenix', 'Tucson', 'Mesa', 'Chandler'],
    'AR': ['Little Rock', 'Fort Smith', 'Fayetteville', 'Springdale'],
    'CA': ['Los Angeles', 'San Diego', 'San Jose', 'San Francisco', 'Fresno', 'Sacramento'],
    'CO': ['Denver', 'Colorado Springs', 'Aurora', 'Fort Collins'],
    'CT': ['Bridgeport', 'New Haven', 'Hartford', 'Stamford'],
    'DE': ['Wilmington', 'Dover'],
    'FL': ['Jacksonville', 'Miami', 'Tampa', 'Orlando', 'St. Petersburg'],
    'GA': ['Atlanta', 'Augusta', 'Columbus', 'Savannah'],
    'ID': ['Boise', 'Nampa', 'Meridian'],
    'IL': ['Chicago', 'Aurora', 'Naperville', 'Joliet', 'Rockford', 'Springfield', 'Bolingbrook'], # Added Bolingbrook
    'IN': ['Indianapolis', 'Fort Wayne', 'Evansville', 'South Bend'],
    'IA': ['Des Moines', 'Cedar Rapids', 'Davenport', 'Sioux City'],
    'KS': ['Wichita', 'Overland Park', 'Kansas City', 'Topeka'],
    'KY': ['Louisville', 'Lexington', 'Bowling Green'],
    'LA': ['New Orleans', 'Baton Rouge', 'Shreveport', 'Lafayette'],
    'ME': ['Portland', 'Lewiston'],
    'MD': ['Baltimore', 'Frederick', 'Rockville'],
    'MA': ['Boston', 'Worcester', 'Springfield', 'Cambridge'],
    'MI': ['Detroit', 'Grand Rapids', 'Warren', 'Sterling Heights'],
    'MN': ['Minneapolis', 'Saint Paul', 'Rochester'],
    'MS': ['Jackson', 'Gulfport', 'Southaven'],
    'MO': ['Kansas City', 'Saint Louis', 'Springfield', 'Columbia'],
    'MT': ['Billings', 'Missoula', 'Great Falls'],
    'NE': ['Omaha', 'Lincoln', 'Bellevue'],
    'NV': ['Las Vegas', 'Henderson', 'Reno'],
    'NH': ['Manchester', 'Nashua', 'Concord'],
    'NJ': ['Newark', 'Jersey City', 'Paterson', 'Elizabeth'],
    'NM': ['Albuquerque', 'Las Cruces', 'Rio Rancho'],
    'NY': ['New York City', 'Buffalo', 'Rochester', 'Yonkers', 'Syracuse'],
    'NC': ['Charlotte', 'Raleigh', 'Greensboro', 'Durham'],
    'ND': ['Fargo', 'Bismarck', 'Grand Forks'],
    'OH': ['Columbus', 'Cleveland', 'Cincinnati', 'Toledo', 'Akron'],
    'OK': ['Oklahoma City', 'Tulsa', 'Norman'],
    'OR': ['Portland', 'Salem', 'Eugene'],
    'PA': ['Philadelphia', 'Pittsburgh', 'Allentown', 'Erie'],
    'RI': ['Providence', 'Warwick', 'Cranston'],
    'SC': ['Columbia', 'Charleston', 'North Charleston'],
    'SD': ['Sioux Falls', 'Rapid City'],
    'TN': ['Nashville', 'Memphis', 'Knoxville', 'Chattanooga'],
    'TX': ['Houston', 'San Antonio', 'Dallas', 'Austin', 'Fort Worth'],
    'UT': ['Salt Lake City', 'West Valley City', 'Provo'],
    'VT': ['Burlington', 'South Burlington'],
    'VA': ['Virginia Beach', 'Norfolk', 'Chesapeake', 'Richmond'],
    'WA': ['Seattle', 'Spokane', 'Tacoma', 'Vancouver'],
    'WV': ['Charleston', 'Huntington'],
    'WI': ['Milwaukee', 'Madison', 'Green Bay'],
    'WY': ['Cheyenne', 'Casper']
}
states = list(states_cities.keys())

regions = ['Northeast', 'South', 'Midwest', 'West']
location_types = ['Franchise', 'Corporate', 'Retail Kiosk']
filing_statuses = ['Single', 'Married Filing Jointly', 'Head of Household', 'Married Filing Separately']
complexity_levels = ['Simple', 'Moderate', 'Complex']
yes_no = ['Yes', 'No']
lead_sources = ['Walk-In', 'Website', 'Referral', 'Mailer', 'Social_Media_Ad', 'Prior_Customer']
filing_methods = ['In-Person', 'Drop-Off', 'Online Assist'] # Added from previous thought

# --- Helper Functions ---
def generate_zip_code(state):
    # Basic placeholder: Generate a random 5-digit zip.
    # A real implementation might use state-specific ranges.
    return str(random.randint(10000, 99999)).zfill(5)

def generate_filing_date(tax_year, current_date):
    """Generates a plausible filing date between Jan 1 and Apr 15 of the following year."""
    filing_start_year = tax_year + 1
    start_date = datetime(filing_start_year, 1, 1)
    # Filing deadline is typically April 15th
    default_end_date = datetime(filing_start_year, 4, 15)

    # For the most recent tax year, don't generate dates beyond the current date
    if filing_start_year == current_date.year:
        end_date = min(default_end_date, current_date)
    else:
        end_date = default_end_date

    # Ensure start_date is not after end_date (can happen if current_date is before Jan 1)
    if start_date > end_date:
         # Handle edge case if script run early in the year before filings start
         # Or if tax_year is too far in future (shouldn't happen with TAX_YEARS list)
         return end_date # Or handle error appropriately

    # Generate random date within the range
    random_days = random.randint(0, (end_date - start_date).days)
    filing_date = start_date + timedelta(days=random_days)

    # Simulate peak filing times (more filings Feb-Apr)
    # Simple approach: higher chance of later dates
    if random.random() < 0.7: # 70% chance to be after Feb 1st
       min_peak_date = datetime(filing_start_year, 2, 1)
       if min_peak_date > start_date and min_peak_date < end_date:
           peak_days = (end_date - min_peak_date).days
           if peak_days > 0:
               random_peak_days = random.randint(0, peak_days)
               filing_date = min_peak_date + timedelta(days=random_peak_days)

    return filing_date.date()


# --- Generate Location_Info Table ---
print("Generating Locations...")
locations_data = []
location_ids = set() # Ensure uniqueness

# Assign states to regions (approximate)
state_to_region = {}
# Simplified mapping (adjust as needed for accuracy)
for state in states:
    if state in ['CT', 'ME', 'MA', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT']:
        state_to_region[state] = 'Northeast'
    elif state in ['DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX']:
        state_to_region[state] = 'South'
    elif state in ['IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI']:
        state_to_region[state] = 'Midwest'
    else: # ID, MT, WY, CO, NM, AZ, UT, NV, CA, OR, WA
        state_to_region[state] = 'West'


location_counter = {} # To number locations within a city (e.g., Chicago-1, Chicago-2)

while len(locations_data) < NUM_LOCATIONS:
    state = random.choice(states)
    city = random.choice(states_cities[state])
    city_abbr = city.replace(" ", "")[:5].upper() # Abbreviation for ID

    # Increment counter for this city
    city_key = f"{state}-{city_abbr}"
    location_counter[city_key] = location_counter.get(city_key, 0) + 1
    loc_num = location_counter[city_key]

    location_id = f"LOC-{state}-{city_abbr}-{str(loc_num).zfill(2)}"

    if location_id not in location_ids:
        location_ids.add(location_id)
        locations_data.append({
            'Location_ID': location_id,
            'Location_Name': f"{city} #{loc_num}",
            'City': city,
            'State': state,
            'Zip_Code': generate_zip_code(state),
            'Region': state_to_region[state],
            'Location_Type': random.choices(location_types, weights=[0.6, 0.3, 0.1], k=1)[0], # Franchise more common
            'Target_Returns_Season': random.randint(500, 5000) # Example target range
        })

locations_df = pd.DataFrame(locations_data)
print(f"Generated {len(locations_df)} unique locations.")

# --- Generate Filing_Data Table ---
print("Generating Filings...")
filings_data = []
customer_first_year = {} # Track first time a customer (proxy) is seen

# Get list of valid Location IDs
valid_location_ids = locations_df['Location_ID'].tolist()

for i in range(NUM_FILINGS):
    if (i + 1) % 5000 == 0:
        print(f"  Generating filing {i+1}/{NUM_FILINGS}...")

    tax_year = random.choice(TAX_YEARS)
    filing_date = generate_filing_date(tax_year, CURRENT_DATE)

    # Assign location and get location details
    location_id = random.choice(valid_location_ids)
    location_info = locations_df[locations_df['Location_ID'] == location_id].iloc[0]

    # Generate customer details
    # Bias customer state towards location state, but allow others
    customer_state = random.choices([location_info['State'], random.choice(states)], weights=[0.8, 0.2], k=1)[0]
    customer_zip = generate_zip_code(customer_state)
    customer_birth_year = random.randint(1940, 2005)

    # Customer Type Logic
    customer_proxy_key = f"{customer_zip}-{customer_birth_year}" # Simple proxy for unique customer
    first_seen_year = customer_first_year.get(customer_proxy_key)
    if first_seen_year is None:
        customer_type = 'New'
        customer_first_year[customer_proxy_key] = tax_year
    elif tax_year == first_seen_year:
        customer_type = 'New'
    else:
        customer_type = 'Returning'

    # Simulate AGI (log-normal distribution often used for income)
    # Adjust parameters for desired income range/skewness
    agi = max(1000, round(np.random.lognormal(mean=10.5, sigma=0.6), -2)) # Mean around $36k, adjust sigma for spread

    # Filing status (slightly weighted)
    filing_status = random.choices(filing_statuses, weights=[0.35, 0.35, 0.25, 0.05], k=1)[0]

    # Schedule C usage (more likely for certain AGIs, but random chance)
    schedule_c_prob = 0.1 + (0.2 if 20000 < agi < 100000 else 0) # Base 10% + 20% if mid-range AGI
    schedule_c_used = 'Yes' if random.random() < schedule_c_prob else 'No'

    # Determine Complexity
    if schedule_c_used == 'Yes' or agi > 150000:
        complexity = 'Complex'
    elif agi < 40000 and schedule_c_used == 'No':
        complexity = 'Simple'
    else:
        complexity = 'Moderate'

    # Generate Service Fee based on Complexity
    if complexity == 'Simple':
        base_fee = random.uniform(50, 150)
    elif complexity == 'Moderate':
        base_fee = random.uniform(150, 350)
    else: # Complex
        base_fee = random.uniform(350, 700)
    # Add slight AGI influence and noise
    service_fee = round(base_fee + (agi * 0.001) + random.uniform(-20, 20), 2)
    service_fee = max(40.00, service_fee) # Minimum fee

    # Generate Refund/Owed Amount (Simplified Logic)
    # More likely refund for HoH, lower AGI. More likely owed for higher AGI.
    refund_chance = 0.6 # Base chance of refund
    if filing_status == 'Head of Household': refund_chance += 0.15
    if agi < 30000: refund_chance += 0.1
    if agi > 100000: refund_chance -= 0.2
    if schedule_c_used == 'Yes': refund_chance -= 0.1 # Self-employed often owe

    if random.random() < refund_chance:
        # Generate Refund Amount
        # Larger refunds possible for lower AGI / HoH
        max_refund = 1000 + (50000 / max(10000, agi)) * 2000
        if filing_status == 'Head of Household': max_refund *= 1.5
        refund_owed = round(random.uniform(100, max(500, max_refund)), 2)
    else:
        # Generate Owed Amount
        max_owed = 500 + (agi / 150000) * 5000
        refund_owed = round(random.uniform(-max(200, max_owed), -50), 2) # Negative value

    # Lead Source (adjust weights if needed)
    # If returning, more likely 'Prior_Customer'
    if customer_type == 'Returning' and random.random() < 0.8:
         lead_source = 'Prior_Customer'
    else:
         lead_source = random.choices(lead_sources[:-1], weights=[0.3, 0.3, 0.15, 0.15, 0.1], k=1)[0] # Exclude Prior_Customer initially


    filings_data.append({
        'Filing_ID': f"F{str(tax_year+1)[-2:]}-{str(i+1).zfill(6)}", # e.g., F25-000001
        'Location_ID': location_id,
        'Filing_Date': filing_date,
        'Tax_Year': tax_year,
        'Service_Fee_USD': service_fee,
        'Filing_Status': filing_status,
        'Adjusted_Gross_Income': agi,
        'Refund_Owed_Amount_USD': refund_owed,
        'Schedule_C_Used': schedule_c_used,
        'Return_Complexity': complexity,
        'Customer_Zip_Code': customer_zip,
        'Customer_State': customer_state,
        'Customer_Type': customer_type,
        'Lead_Source': lead_source
        # Removed other schedule flags, birth year, filing method etc. based on final 2-table design
    })

filings_df = pd.DataFrame(filings_data)
print(f"Generated {len(filings_df)} filings.")

# --- Save to CSV ---
locations_filename = 'locations.csv'
filings_filename = 'filings.csv'

locations_df.to_csv(locations_filename, index=False)
filings_df.to_csv(filings_filename, index=False)

print(f"\nMock data saved to:")
print(f"- {locations_filename}")
print(f"- {filings_filename}")
