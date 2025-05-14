import pandas as pd
import numpy as np
import datetime
import random # For probabilistic choices

# --- Configuration ---
# Set the reference date for generation (Today)
TODAY = datetime.date(2025, 5, 12)
START_DATE = TODAY - datetime.timedelta(days=3*365)
END_DATE = TODAY + datetime.timedelta(days=1*365) # Data generation stops *before* this date

OUTPUT_FILENAME = "marketing_funnel_data_v3.csv" # Updated filename

# Dimensions
CHANNELS = ["Organic Search", "Paid Search", "Paid Social - ConnectSphere", "Paid Social - PixelVerse", "Email Marketing", "Referral", "Direct", "AI ContentSynergy"]
REGIONS = ["North America", "Europe", "APAC", "LATAM"]
PRODUCTS = ["AlphaSuite", "BetaPlatform", "GammaTools"] # Fictional product names

# --- Existing Added Dimensions ---
DEVICE_TYPES = ['Desktop', 'Mobile', 'Tablet']
AUDIENCE_SEGMENTS = ['New Visitor', 'Returning Visitor']
KEYWORD_THEMES = ['Brand', 'Non-Brand Generic', 'Non-Brand Feature', 'N/A'] # N/A for non-search channels

# --- NEW DIMENSIONS (v3) ---
CONTENT_TYPES = ['Blog Post', 'Landing Page', 'Video Ad', 'Product Page', 'Email Body', 'Social Post', 'N/A']
INTENT_STAGES = ['Awareness', 'Consideration', 'Conversion']
TIME_OF_DAY_BUCKETS = ['Morning (6-12)', 'Afternoon (12-18)', 'Evening (18-24)', 'Late Night (0-6)']


# --- Campaign Definitions (Same as v1/v2) ---
CAMPAIGNS = [
    # --- Past Campaigns ---
    {"id": "C001", "name": "AlphaSuite Q3 2022 Launch", "start_date": datetime.date(2022, 7, 1), "end_date": datetime.date(2022, 9, 30),
     "products": ["AlphaSuite"], "channels": ["Paid Search", "Email Marketing"], "imp_mult": 1.6, "lead_mult": 1.3, "spend_abs": 250, "ctr_abs": 0.006},
    {"id": "C002", "name": "End of Year Sale 2022", "start_date": datetime.date(2022, 11, 15), "end_date": datetime.date(2022, 12, 31),
     "products": [], "channels": ["Paid Search", "Email Marketing", "Paid Social - PixelVerse"], "imp_mult": 2.0, "lead_mult": 1.5, "spend_abs": 400, "ctr_abs": 0.008},
    {"id": "C003", "name": "BetaPlatform Awareness Q2 2023", "start_date": datetime.date(2023, 4, 1), "end_date": datetime.date(2023, 6, 30),
     "products": ["BetaPlatform"], "channels": ["Paid Social - PixelVerse", "Paid Search"], "imp_mult": 1.8, "lead_mult": 1.4, "spend_abs": 350, "ctr_abs": 0.007},
    {"id": "C004", "name": "Summer Slowdown Promo 2023", "start_date": datetime.date(2023, 7, 15), "end_date": datetime.date(2023, 8, 31), # Counteract seasonality
     "products": ["GammaTools"], "channels": ["Email Marketing", "Paid Social - PixelVerse"], "imp_mult": 1.3, "lead_mult": 1.6, "spend_abs": 150, "ctr_abs": 0.004},
    {"id": "C005", "name": "ConnectSphere Entry Q4 2023", "start_date": datetime.date(2023, 10, 1), "end_date": datetime.date(2023, 12, 31),
     "products": ["BetaPlatform", "GammaTools"], "channels": ["Paid Social - ConnectSphere"], "imp_mult": 2.5, "lead_mult": 1.7, "spend_abs": 300, "ctr_abs": 0.010}, # Launch campaign for this channel
    {"id": "C006", "name": "End of Year Sale 2024", "start_date": datetime.date(2024, 11, 15), "end_date": datetime.date(2024, 12, 31),
     "products": [], "channels": ["Paid Search", "Email Marketing", "Paid Social - ConnectSphere"], "imp_mult": 2.2, "lead_mult": 1.6, "spend_abs": 500, "ctr_abs": 0.009},
    {"id": "C007", "name": "GammaTools Feature Push Q1 2025", "start_date": datetime.date(2025, 2, 1), "end_date": datetime.date(2025, 4, 30),
     "products": ["GammaTools"], "channels": ["Paid Search", "Paid Social - ConnectSphere", "Direct"], "imp_mult": 1.7, "lead_mult": 1.8, "spend_abs": 400, "ctr_abs": 0.007},

    # --- Future Campaigns ---
    {"id": "C008", "name": "AI Synergy Beta Program Q3 2025", "start_date": datetime.date(2025, 8, 1), "end_date": datetime.date(2025, 10, 31),
     "products": ["BetaPlatform"], "channels": ["AI ContentSynergy", "Email Marketing"], "imp_mult": 3.0, "lead_mult": 2.0, "spend_abs": 200, "ctr_abs": 0.015}, # Drive adoption for new channel
    {"id": "C009", "name": "Global Summit Attendee Drive Oct 2025", "start_date": datetime.date(2025, 10, 1), "end_date": datetime.date(2025, 10, 31), # Short, intense
     "products": [], "channels": ["Email Marketing", "Paid Social - ConnectSphere", "Direct"], "imp_mult": 1.5, "lead_mult": 2.5, "spend_abs": 300, "ctr_abs": 0.005},
    {"id": "C010", "name": "End of Year Sale 2025", "start_date": datetime.date(2025, 11, 15), "end_date": datetime.date(2025, 12, 31),
     "products": [], "channels": ["Paid Search", "Email Marketing", "Paid Social - ConnectSphere", "AI ContentSynergy"], "imp_mult": 2.5, "lead_mult": 1.8, "spend_abs": 600, "ctr_abs": 0.010},
    {"id": "C011", "name": "AlphaSuite Refresh Q1 2026", "start_date": datetime.date(2026, 2, 1), "end_date": datetime.date(2026, 4, 30),
     "products": ["AlphaSuite"], "channels": ["Paid Search", "AI ContentSynergy", "Organic Search"], "imp_mult": 1.8, "lead_mult": 1.5, "spend_abs": 450, "ctr_abs": 0.008}, # Note: Spend boost on Organic is conceptual (e.g., content investment)
]

# --- Base Values & Conversion Rates (Same as v2) ---
BASE_METRICS = {
    "Organic Search": {"impressions": 24000, "ctr": 0.032, "spend_factor": 0},
    "Paid Search": {"impressions": 17000, "ctr": 0.042, "spend_factor": 0.025},
    "Paid Social - ConnectSphere": {"impressions": 0, "ctr": 0.020, "spend_factor": 0.015},
    "Paid Social - PixelVerse": {"impressions": 14000, "ctr": 0.016, "spend_factor": 0.020},
    "Email Marketing": {"impressions": 10000, "ctr": 0.050, "spend_factor": 0.002},
    "Referral": {"impressions": 5800, "ctr": 0.037, "spend_factor": 0},
    "Direct": {"impressions": 8800, "ctr": 0.062, "spend_factor": 0},
    "AI ContentSynergy": {"impressions": 0, "ctr": 0.027, "spend_factor": 0.030}
}
CONVERSION_RATES = { "lead_from_click": 0.06, "mql_from_lead": 0.35, "sql_from_mql": 0.45, "opp_from_sql": 0.55, "win_from_opp": 0.30 }

# --- Dimension Probabilities & Modifiers ---
DIMENSION_PROBS = {
    "DeviceType": { # (Same as v2)
        "Organic Search": {"Desktop": 0.5, "Mobile": 0.4, "Tablet": 0.1}, "Paid Search": {"Desktop": 0.55, "Mobile": 0.35, "Tablet": 0.1},
        "Paid Social - ConnectSphere": {"Desktop": 0.2, "Mobile": 0.7, "Tablet": 0.1}, "Paid Social - PixelVerse": {"Desktop": 0.25, "Mobile": 0.65, "Tablet": 0.1},
        "Email Marketing": {"Desktop": 0.6, "Mobile": 0.35, "Tablet": 0.05}, "Referral": {"Desktop": 0.6, "Mobile": 0.3, "Tablet": 0.1},
        "Direct": {"Desktop": 0.5, "Mobile": 0.4, "Tablet": 0.1}, "AI ContentSynergy": {"Desktop": 0.4, "Mobile": 0.5, "Tablet": 0.1},
    },
    "AudienceSegment": { "default": {"New Visitor": 0.75, "Returning Visitor": 0.25} }, # (Same as v2)
    "KeywordTheme": { # (Same as v2)
        "Organic Search": {"Brand": 0.25, "Non-Brand Generic": 0.50, "Non-Brand Feature": 0.25, "N/A": 0.0},
        "Paid Search": {"Brand": 0.30, "Non-Brand Generic": 0.40, "Non-Brand Feature": 0.30, "N/A": 0.0},
        "default": {"Brand": 0.0, "Non-Brand Generic": 0.0, "Non-Brand Feature": 0.0, "N/A": 1.0}
    },
    # --- NEW v3 Probabilities ---
    "ContentType": {
        "Organic Search": {"Blog Post": 0.4, "Landing Page": 0.3, "Product Page": 0.3, "Video Ad": 0.0, "Email Body": 0.0, "Social Post": 0.0, "N/A": 0.0},
        "Paid Search": {"Blog Post": 0.1, "Landing Page": 0.6, "Product Page": 0.3, "Video Ad": 0.0, "Email Body": 0.0, "Social Post": 0.0, "N/A": 0.0},
        "Paid Social - ConnectSphere": {"Blog Post": 0.1, "Landing Page": 0.3, "Product Page": 0.1, "Video Ad": 0.2, "Email Body": 0.0, "Social Post": 0.3, "N/A": 0.0},
        "Paid Social - PixelVerse": {"Blog Post": 0.1, "Landing Page": 0.4, "Product Page": 0.1, "Video Ad": 0.2, "Email Body": 0.0, "Social Post": 0.2, "N/A": 0.0},
        "Email Marketing": {"Blog Post": 0.0, "Landing Page": 0.4, "Product Page": 0.2, "Video Ad": 0.0, "Email Body": 0.4, "Social Post": 0.0, "N/A": 0.0}, # Email Body is the impression
        "Referral": {"Blog Post": 0.2, "Landing Page": 0.4, "Product Page": 0.4, "Video Ad": 0.0, "Email Body": 0.0, "Social Post": 0.0, "N/A": 0.0},
        "Direct": {"Blog Post": 0.1, "Landing Page": 0.3, "Product Page": 0.6, "Video Ad": 0.0, "Email Body": 0.0, "Social Post": 0.0, "N/A": 0.0},
        "AI ContentSynergy": {"Blog Post": 0.3, "Landing Page": 0.4, "Product Page": 0.2, "Video Ad": 0.1, "Email Body": 0.0, "Social Post": 0.0, "N/A": 0.0}, # Mix for AI channel
        "default": {"Blog Post": 0.0, "Landing Page": 0.0, "Product Page": 0.0, "Video Ad": 0.0, "Email Body": 0.0, "Social Post": 0.0, "N/A": 1.0}
    },
    "IntentStage": { # Simplified intent mapping based on channel/content
        "default": {"Awareness": 0.4, "Consideration": 0.4, "Conversion": 0.2} # General default mix
        # Could be refined: e.g., Product Page leans Conversion, Blog Post leans Awareness/Consideration
    },
    "TimeOfDayBucket": { # General distribution, could vary by channel (e.g. Social peaks evening)
        "default": {'Morning (6-12)': 0.25, 'Afternoon (12-18)': 0.35, 'Evening (18-24)': 0.30, 'Late Night (0-6)': 0.10}
    }
}

DIMENSION_MODIFIERS = {
    "DeviceType": { # (Same as v2)
        "Desktop": {"imp_mult": 1.0, "ctr_mult": 1.05, "conv_mult": 1.0}, "Mobile": {"imp_mult": 1.1, "ctr_mult": 0.90, "conv_mult": 0.95},
        "Tablet": {"imp_mult": 0.9, "ctr_mult": 0.95, "conv_mult": 1.0},
    },
    "AudienceSegment": { # (Same as v2)
        "New Visitor": {"imp_mult": 1.0, "ctr_mult": 0.9, "conv_mult": 0.85}, "Returning Visitor": {"imp_mult": 1.0, "ctr_mult": 1.2, "conv_mult": 1.3},
    },
    "KeywordTheme": { # (Same as v2)
        "Brand": {"imp_mult": 0.8, "ctr_mult": 2.5, "conv_mult": 1.5, "spend_factor_mult": 1.1},
        "Non-Brand Generic": {"imp_mult": 1.1, "ctr_mult": 0.8, "conv_mult": 0.9, "spend_factor_mult": 0.9},
        "Non-Brand Feature": {"imp_mult": 1.0, "ctr_mult": 1.0, "conv_mult": 1.1, "spend_factor_mult": 1.0},
        "N/A": {"imp_mult": 1.0, "ctr_mult": 1.0, "conv_mult": 1.0, "spend_factor_mult": 1.0},
    },
    # --- NEW v3 Modifiers ---
    "ContentType": {
        "Blog Post":        {"imp_mult": 1.0, "ctr_mult": 0.7, "conv_mult": 0.6}, # High volume, lower engagement/conv
        "Landing Page":     {"imp_mult": 1.0, "ctr_mult": 1.1, "conv_mult": 1.1}, # Good engagement/conv
        "Video Ad":         {"imp_mult": 1.2, "ctr_mult": 0.6, "conv_mult": 0.7}, # High imp, low CTR (view=imp), lower conv
        "Product Page":     {"imp_mult": 0.9, "ctr_mult": 1.2, "conv_mult": 1.4}, # Lower vol, high intent/conv
        "Email Body":       {"imp_mult": 1.0, "ctr_mult": 1.0, "conv_mult": 1.0}, # CTR is open/click, baseline conv
        "Social Post":      {"imp_mult": 1.1, "ctr_mult": 0.8, "conv_mult": 0.8}, # High imp, lower CTR/conv
        "N/A":              {"imp_mult": 1.0, "ctr_mult": 1.0, "conv_mult": 1.0},
    },
    "IntentStage": {
        "Awareness":        {"imp_mult": 1.1, "ctr_mult": 0.8, "conv_mult": 0.5}, # High imp, low CTR/Conv
        "Consideration":    {"imp_mult": 1.0, "ctr_mult": 1.0, "conv_mult": 1.0}, # Baseline
        "Conversion":       {"imp_mult": 0.9, "ctr_mult": 1.3, "conv_mult": 1.8}, # Lower imp, high CTR/Conv
    },
    "TimeOfDayBucket": { # Affects impression volume mainly
        "Morning (6-12)":   {"imp_mult": 0.9, "ctr_mult": 1.0, "conv_mult": 1.0},
        "Afternoon (12-18)":{"imp_mult": 1.1, "ctr_mult": 1.05, "conv_mult": 1.0}, # Peak activity?
        "Evening (18-24)":  {"imp_mult": 1.05, "ctr_mult": 0.95, "conv_mult": 1.0}, # High social?
        "Late Night (0-6)": {"imp_mult": 0.7, "ctr_mult": 0.9, "conv_mult": 0.9}, # Low activity
    }
}


# --- Helper Functions ---
def get_active_campaigns(current_date, channel, product):
    """Finds campaigns active on a given date for a specific channel/product."""
    # (Same as v2)
    active = []
    for campaign in CAMPAIGNS:
        is_active_date = campaign["start_date"] <= current_date <= campaign["end_date"]
        is_target_channel = not campaign["channels"] or channel in campaign["channels"]
        is_target_product = not campaign["products"] or product in campaign["products"]
        if is_active_date and is_target_channel and is_target_product:
            active.append(campaign)
    return active

def choose_dimension_value(category, channel):
    """Probabilistically chooses a value for a dimension based on channel or default."""
    # (Enhanced to handle new categories using defaults)
    if category == "KeywordTheme":
        probs = DIMENSION_PROBS[category].get(channel, DIMENSION_PROBS[category]["default"])
    elif category == "ContentType":
         probs = DIMENSION_PROBS[category].get(channel, DIMENSION_PROBS[category]["default"])
    elif category in ["AudienceSegment", "IntentStage", "TimeOfDayBucket"]:
        probs = DIMENSION_PROBS[category].get("default") # Using default for these
    else: # DeviceType
        probs = DIMENSION_PROBS[category].get(channel, list(DIMENSION_PROBS[category].values())[0])

    choices = list(probs.keys())
    weights = list(probs.values())
    total_weight = sum(weights)
    if not np.isclose(total_weight, 1.0):
        # print(f"Warning: Weights for {category}/{channel} do not sum to 1 ({total_weight}). Normalizing.")
        if total_weight == 0: # Avoid division by zero if all weights are somehow zero
             if choices: return random.choice(choices)
             else: return None # Should not happen with defined defaults
        weights = [w / total_weight for w in weights]

    weights = [max(0, w) for w in weights] # Ensure non-negative
    total_weight = sum(weights)
    if total_weight == 0:
        if choices: return random.choice(choices)
        else: return None
    weights = [w / total_weight for w in weights] # Re-normalize after clamping

    return random.choices(choices, weights=weights, k=1)[0]


def generate_data():
    """Generates the marketing funnel dataset with enhanced dimensions."""
    data = []
    current_date = START_DATE
    total_days = (END_DATE - START_DATE).days
    days_generated = 0

    print(f"Generating data from {START_DATE} to {END_DATE - datetime.timedelta(days=1)}...")

    while current_date < END_DATE:
        day_of_year = current_date.timetuple().tm_yday
        day_of_week = current_date.weekday()
        year = current_date.year

        # --- Global Factors ---
        growth_rate_per_day = 0.0005
        base_trend_factor = (1 + growth_rate_per_day) ** days_generated
        seasonal_factor = 1 + 0.15 * np.sin(2 * np.pi * (day_of_year + 75) / 365.25)
        weekly_factor = 1.0
        if day_of_week == 5: weekly_factor = 0.85
        elif day_of_week == 6: weekly_factor = 0.80

        for channel in CHANNELS:
            for region in REGIONS:
                product_focus_idx = (days_generated + hash(channel) + hash(region)) % len(PRODUCTS)
                product_focus = PRODUCTS[product_focus_idx]

                # --- Base Metrics ---
                base_imp = BASE_METRICS[channel]["impressions"]
                base_ctr = BASE_METRICS[channel]["ctr"]
                base_spend_factor = BASE_METRICS[channel]["spend_factor"]

                # Apply global factors
                current_impressions = base_imp * base_trend_factor * seasonal_factor * weekly_factor
                current_ctr = base_ctr
                current_spend_factor = base_spend_factor

                # --- Story Point / Channel Logic (Applied before dimension modifiers) ---
                # (Same logic as v2 for algorithm hit, ConnectSphere growth, PixelVerse decline, AI Synergy launch)
                algo_hit_start = datetime.date(2024, 3, 1); algo_hit_end = datetime.date(2024, 6, 30)
                algo_rec_start = datetime.date(2024, 7, 1); algo_rec_end = datetime.date(2024, 10, 31)
                organic_algo_imp_mult = 1.0; organic_algo_ctr_mult = 1.0
                if channel == "Organic Search":
                    if algo_hit_start <= current_date <= algo_hit_end:
                        organic_algo_imp_mult = 0.65; organic_algo_ctr_mult = 0.85
                    elif algo_rec_start <= current_date <= algo_rec_end:
                        recovery_progress = (current_date - algo_rec_start).days / (algo_rec_end - algo_rec_start).days
                        organic_algo_imp_mult = (0.65 + 0.30 * recovery_progress); organic_algo_ctr_mult = (0.85 + 0.13 * recovery_progress)
                    current_impressions *= organic_algo_imp_mult; current_ctr *= organic_algo_ctr_mult
                connectsphere_official_start = datetime.date(2023, 10, 1)
                if channel == "Paid Social - ConnectSphere":
                    if current_date < connectsphere_official_start: current_impressions = 0
                    else:
                        days_since_launch = (current_date - connectsphere_official_start).days
                        growth_factor = 1 / (1 + np.exp(-0.01 * (days_since_launch - 180)))
                        current_impressions = BASE_METRICS[channel]["impressions"] * growth_factor * base_trend_factor * seasonal_factor * weekly_factor
                        current_ctr *= (1 + 0.1 * growth_factor)
                pixelverse_decline_start = datetime.date(2024, 7, 1)
                if channel == "Paid Social - PixelVerse" and current_date >= pixelverse_decline_start:
                     days_since_decline = (current_date - pixelverse_decline_start).days
                     decline_factor = max(0.5, 1 - 0.0005 * days_since_decline)
                     current_impressions *= decline_factor; current_ctr *= max(0.7, 1 - 0.0003 * days_since_decline)
                ai_synergy_start = datetime.date(2025, 8, 1)
                if channel == "AI ContentSynergy":
                    if current_date < ai_synergy_start: current_impressions = 0
                    else:
                        days_since_launch = (current_date - ai_synergy_start).days
                        growth_factor = 1 / (1 + np.exp(-0.015 * (days_since_launch - 120)))
                        current_impressions = BASE_METRICS[channel]["impressions"] * growth_factor * base_trend_factor * seasonal_factor * weekly_factor
                        current_ctr *= (1 + 0.05 * growth_factor)

                # --- Regional Variations ---
                region_factors = {"North America": 1.1, "Europe": 1.0, "APAC": 0.8, "LATAM": 0.6}
                current_impressions *= region_factors.get(region, 1.0)

                # --- Assign Dimension Values for this Row ---
                assigned_device = choose_dimension_value("DeviceType", channel)
                assigned_audience = choose_dimension_value("AudienceSegment", channel)
                assigned_keyword_theme = choose_dimension_value("KeywordTheme", channel)
                # --- NEW v3 Assignments ---
                assigned_content_type = choose_dimension_value("ContentType", channel)
                assigned_intent_stage = choose_dimension_value("IntentStage", channel)
                assigned_time_bucket = choose_dimension_value("TimeOfDayBucket", channel)


                # --- Apply Dimension Modifiers ---
                device_mods = DIMENSION_MODIFIERS["DeviceType"][assigned_device]
                audience_mods = DIMENSION_MODIFIERS["AudienceSegment"][assigned_audience]
                keyword_mods = DIMENSION_MODIFIERS["KeywordTheme"][assigned_keyword_theme]
                # --- NEW v3 Modifiers ---
                content_mods = DIMENSION_MODIFIERS["ContentType"][assigned_content_type]
                intent_mods = DIMENSION_MODIFIERS["IntentStage"][assigned_intent_stage]
                time_mods = DIMENSION_MODIFIERS["TimeOfDayBucket"][assigned_time_bucket]

                # Apply modifiers multiplicatively
                current_impressions *= (device_mods["imp_mult"] * audience_mods["imp_mult"] * keyword_mods["imp_mult"] *
                                        content_mods["imp_mult"] * intent_mods["imp_mult"] * time_mods["imp_mult"])
                current_ctr *= (device_mods["ctr_mult"] * audience_mods["ctr_mult"] * keyword_mods["ctr_mult"] *
                                content_mods["ctr_mult"] * intent_mods["ctr_mult"] * time_mods["ctr_mult"])
                current_spend_factor *= keyword_mods["spend_factor_mult"] # Only keyword theme affects spend factor

                # Combine conversion multipliers from all dimensions
                base_conv_modifier = (device_mods["conv_mult"] * audience_mods["conv_mult"] * keyword_mods["conv_mult"] *
                                      content_mods["conv_mult"] * intent_mods["conv_mult"] * time_mods["conv_mult"])

                # --- Apply Campaign Effects ---
                active_campaigns = get_active_campaigns(current_date, channel, product_focus)
                campaign_names = "Organic/Baseline"
                campaign_spend_boost = 0
                campaign_lead_mult = 1.0

                if active_campaigns:
                    campaign_names_list = []
                    imp_multiplier_agg = 1.0; ctr_boost_agg = 0.0; lead_multiplier_agg = 1.0
                    for camp in active_campaigns:
                        campaign_names_list.append(camp["name"])
                        imp_multiplier_agg *= camp["imp_mult"]
                        ctr_boost_agg += camp["ctr_abs"]
                        campaign_spend_boost += camp["spend_abs"]
                        lead_multiplier_agg *= camp["lead_mult"]
                    current_impressions *= imp_multiplier_agg
                    current_ctr += ctr_boost_agg
                    campaign_lead_mult = lead_multiplier_agg
                    campaign_names = "; ".join(campaign_names_list)

                # --- Calculate Spend ---
                current_spend = (current_impressions * current_spend_factor) + campaign_spend_boost
                if base_spend_factor == 0 and campaign_spend_boost == 0: current_spend = 0

                # --- Add Noise & Final Calculations ---
                imp_noise = 1 + np.random.normal(0, 0.08); ctr_noise = 1 + np.random.normal(0, 0.05); spend_noise = 1 + np.random.normal(0, 0.10)
                final_impressions = max(0, int(current_impressions * imp_noise))
                final_ctr = max(0.0001, current_ctr * ctr_noise)
                final_spend = max(0, round(current_spend * spend_noise, 2))

                # --- Funnel Calculations ---
                clicks = min(final_impressions, max(0, int(final_impressions * final_ctr)))
                effective_lead_conv = CONVERSION_RATES["lead_from_click"] * base_conv_modifier * campaign_lead_mult
                effective_mql_conv = CONVERSION_RATES["mql_from_lead"] * base_conv_modifier
                effective_sql_conv = CONVERSION_RATES["sql_from_mql"] * base_conv_modifier
                effective_opp_conv = CONVERSION_RATES["opp_from_sql"] * base_conv_modifier
                effective_win_conv = CONVERSION_RATES["win_from_opp"] * base_conv_modifier
                leads = max(0, int(clicks * effective_lead_conv * (1 + np.random.normal(0, 0.06))))
                mqls = max(0, int(leads * effective_mql_conv * (1 + np.random.normal(0, 0.07))))
                sqls = max(0, int(mqls * effective_sql_conv * (1 + np.random.normal(0, 0.08))))
                opportunities = max(0, int(sqls * effective_opp_conv * (1 + np.random.normal(0, 0.09))))
                wins = max(0, int(opportunities * effective_win_conv * (1 + np.random.normal(0, 0.10))))
                leads = min(clicks, leads); mqls = min(leads, mqls); sqls = min(mqls, sqls)
                opportunities = min(sqls, opportunities); wins = min(opportunities, wins)

                # Only add row if there's some activity
                if final_impressions > 0 or final_spend > 0:
                    data.append({
                        "Date": current_date,
                        "Channel": channel,
                        "Region": region,
                        "ProductFocus": product_focus,
                        "DeviceType": assigned_device,
                        "AudienceSegment": assigned_audience,
                        "KeywordTheme": assigned_keyword_theme,
                        # --- NEW v3 COLUMNS ---
                        "ContentType": assigned_content_type,
                        "IntentStage": assigned_intent_stage,
                        "TimeOfDayBucket": assigned_time_bucket,
                        # --- END NEW ---
                        "CampaignNames": campaign_names,
                        "Impressions": final_impressions,
                        "Clicks": clicks,
                        "Spend": final_spend,
                        "Leads": leads,
                        "MQLs": mqls,
                        "SQLs": sqls,
                        "Opportunities": opportunities,
                        "Wins": wins,
                        "CTR": round(final_ctr, 5)
                    })

        # Increment day
        current_date += datetime.timedelta(days=1)
        days_generated += 1
        if days_generated % 90 == 0:
            progress = (days_generated / total_days) * 100
            print(f"Progress: {progress:.1f}% - Generated up to {current_date - datetime.timedelta(days=1)}")

    print("Data generation complete.")
    return pd.DataFrame(data)

# --- Main Execution ---
if __name__ == "__main__":
    df_marketing = generate_data()

    if not df_marketing.empty:
        print(f"\nGenerated {len(df_marketing)} rows of data.")
        df_marketing.to_csv(OUTPUT_FILENAME, index=False)
        print(f"Data saved to {OUTPUT_FILENAME}")

        print("\n--- Data Summary ---")
        print(df_marketing.head())
        print(f"\nDate range: {df_marketing['Date'].min()} to {df_marketing['Date'].max()}")
        print("\nColumns:", df_marketing.columns.tolist()) # Show new columns

        # Example aggregations
        df_marketing['Year'] = pd.to_datetime(df_marketing['Date']).dt.year
        print("\n--- Total Wins per Year ---")
        print(df_marketing.groupby('Year')['Wins'].sum())

        print("\n--- Wins by Content Type (Overall) ---") # Check new dimension
        print(df_marketing.groupby('ContentType')['Wins'].sum().sort_values(ascending=False))

        print("\n--- Leads by Intent Stage (Overall) ---") # Check new dimension
        print(df_marketing.groupby('IntentStage')['Leads'].sum().sort_values(ascending=False))

        print("\n--- Impressions by Time of Day (Overall) ---") # Check new dimension
        print(df_marketing.groupby('TimeOfDayBucket')['Impressions'].sum().sort_values(ascending=False))

    else:
        print("No data was generated. Check configuration and date ranges.")
