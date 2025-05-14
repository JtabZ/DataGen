import pandas as pd
import numpy as np
import datetime
import random
import uuid
import hashlib

# --- Configuration ---
NUM_PRODUCTS = 15
NUM_TEAMS = 10
NUM_CAMPAIGNS = 10
NUM_CUSTOMERS = 5000 # Number of unique customer hashes to generate feedback/tickets for

# Define Date Range (Approx 3 years past, 1 year future from May 12, 2025)
CURRENT_DATE = datetime.date(2025, 5, 12)
START_DATE = CURRENT_DATE - datetime.timedelta(days=3*365)
END_DATE = CURRENT_DATE + datetime.timedelta(days=1*365) # END_DATE is a datetime.date object
DATE_RANGE = pd.date_range(START_DATE, END_DATE, freq='D')

def main():
    print(f"Generating data from {START_DATE} to {END_DATE}")

    # --- Helper Functions ---
    def generate_hashed_id(prefix, value):
        """Generates a consistent hashed ID for privacy simulation."""
        hash_object = hashlib.sha1(str(value).encode())
        return f"{prefix}_HASH_{hash_object.hexdigest()[:10]}"

    def simulate_trend_with_noise(base_value, trend_factor, noise_level, size):
        """Simulates a value with a general trend and daily noise."""
        trend = np.linspace(0, trend_factor * size, size)
        noise = np.random.normal(0, noise_level, size)
        simulated = base_value + trend + noise
        return np.maximum(0, simulated) # Ensure non-negative values

    def simulate_seasonal_multiplier(dates_series):
        """Applies a simple weekly seasonality (lower weekends)."""
        # Monday=0, Sunday=6
        day_of_week = dates_series.dt.dayofweek
        # Lower multiplier for Sat (5) and Sun (6)
        multiplier = np.where((day_of_week == 5) | (day_of_week == 6),
                            np.random.uniform(0.6, 0.8, len(dates_series)), # Weekend dip
                            np.random.uniform(0.9, 1.1, len(dates_series))) # Weekday variation
        return multiplier

    def generate_random_timestamp(start_date_dt_obj, end_date_dt_obj):
        """
        Generates a random timestamp within a date range.
        Accepts datetime.date or pandas.Timestamp for start_date_dt_obj and end_date_dt_obj.
        """
        # Convert pandas.Timestamp to datetime.date if necessary for timedelta compatibility
        if isinstance(start_date_dt_obj, pd.Timestamp):
            start_date_dt_obj = start_date_dt_obj.date()
        if isinstance(end_date_dt_obj, pd.Timestamp):
            end_date_dt_obj = end_date_dt_obj.date()

        time_between_dates = end_date_dt_obj - start_date_dt_obj
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates + 1) # Include end date
        random_date_val = start_date_dt_obj + datetime.timedelta(days=random_number_of_days)
        random_time_val = datetime.time(
            random.randint(0, 23),
            random.randint(0, 59),
            random.randint(0, 59)
        )
        return datetime.datetime.combine(random_date_val, random_time_val)

    # --- Dimension Table Generation ---

    # 1. Dim_Product
    print("Generating Dim_Product...")
    products_data = []
    product_names = ["QuantumLeap Platform", "MobileConnect App", "AI Insights Engine", "Core Infra Suite", "DataStream API", "SecureAuth Service", "Project Phoenix"]
    categories = ["B2B SaaS", "Mobile App", "AI Service", "Core Infrastructure", "API Service", "Security", "Internal Platform"]
    managers = ["Alice Wonderland", "Bob The Builder", "Charlie Chaplin", "Diana Prince"]
    segments = ["Enterprise", "SMB", "FinTech", "Healthcare", "Developer", "Internal"]
    priorities = ["High", "Medium", "Low"]

    for i in range(NUM_PRODUCTS):
        product_id = f"PROD{str(i+1).zfill(3)}"
        launch_offset_days = random.randint(60, 3*365 - 60)
        launch_date = START_DATE + datetime.timedelta(days=launch_offset_days)
        launch_date = min(launch_date, CURRENT_DATE - datetime.timedelta(days=60))


        products_data.append({
            "ProductID": product_id,
            "ProductName": product_names[i % len(product_names)] + (f" v{random.randint(1,3)}" if i % 2 == 0 else ""),
            "ProductCategory": random.choice(categories),
            "ProductManager": random.choice(managers),
            "LaunchDate": launch_date,
            "TargetMarketSegment": random.choice(segments),
            "StrategicPriority": random.choice(priorities)
        })
    dim_product = pd.DataFrame(products_data)
    PRODUCT_IDS = dim_product['ProductID'].tolist()
    print(f"Generated {len(dim_product)} products.")

    # 2. Dim_Team
    print("Generating Dim_Team...")
    teams_data = []
    team_names = ["Platform Core", "Mobile Innovators", "AI Research Guild", "Ops Guardians", "Customer Success NA", "Frontend Wizards"]
    leads = ["Charles Xavier", "Diana Prince", "Clark Kent", "Bruce Wayne"]
    methodologies = ["Agile Scrum", "Kanban", "Scrumban"]
    regions = ["NA", "EMEA", "APAC", "Global"]

    for i in range(NUM_TEAMS):
        teams_data.append({
            "TeamID": f"TEAM{str(i+1).zfill(3)}",
            "TeamName": team_names[i % len(team_names)],
            "TeamLeadName": random.choice(leads),
            "DevelopmentMethodology": random.choice(methodologies) if "Dev" in team_names[i % len(team_names)] or "Guild" in team_names[i % len(team_names)] or "Core" in team_names[i % len(team_names)] else None,
            "TeamRegion": random.choice(regions)
        })
    dim_team = pd.DataFrame(teams_data)
    TEAM_IDS = dim_team['TeamID'].tolist()
    print(f"Generated {len(dim_team)} teams.")

    # 3. Dim_Campaign
    print("Generating Dim_Campaign...")
    campaigns_data = []
    campaign_types = ["Digital Advertising", "Content Marketing", "Email Campaign", "Launch Event", "Webinar Series", "Partner Promotion"]
    campaign_name_templates = ["{} Growth Push", "{} Awareness Q{}", "{} User Acquisition", "{} Feature Launch"]

    for i in range(NUM_CAMPAIGNS):
        target_product_id = random.choice(PRODUCT_IDS)
        target_product_name = dim_product[dim_product['ProductID'] == target_product_id]['ProductName'].iloc[0].split(" v")[0]

        duration = random.randint(30, 90)
        max_start_offset = (END_DATE - START_DATE).days - duration - 1
        start_offset = random.randint(0, max_start_offset)
        campaign_start_date = START_DATE + datetime.timedelta(days=start_offset)
        campaign_end_date = campaign_start_date + datetime.timedelta(days=duration)

        quarter = (campaign_start_date.month - 1) // 3 + 1
        campaign_name = random.choice(campaign_name_templates).format(target_product_name, quarter)

        campaigns_data.append({
            "CampaignID": f"CAMP{str(i+1).zfill(3)}",
            "CampaignName": campaign_name,
            "CampaignStartDate": campaign_start_date,
            "CampaignEndDate": campaign_end_date,
            "CampaignType": random.choice(campaign_types),
            "TargetProductID": target_product_id,
            "CampaignSpend_USD": round(random.uniform(5000, 100000), 2)
        })
    dim_campaign = pd.DataFrame(campaigns_data)
    dim_campaign['CampaignStartDate'] = pd.to_datetime(dim_campaign['CampaignStartDate'])
    dim_campaign['CampaignEndDate'] = pd.to_datetime(dim_campaign['CampaignEndDate'])
    print(f"Generated {len(dim_campaign)} campaigns.")


    # --- Fact & Log Table Generation ---

    all_daily_metrics = []
    all_feedback_logs = []
    all_support_tickets = []

    customer_hashes = [generate_hashed_id("CUST", i) for i in range(NUM_CUSTOMERS)]

    event_dates = {}
    for pid in PRODUCT_IDS:
        event_dates[pid] = {}
        num_events = random.randint(1, 4)
        for _ in range(num_events):
            event_day_offset = random.randint(30, (END_DATE - START_DATE).days - 30)
            event_date = START_DATE + datetime.timedelta(days=event_day_offset)
            event_type = random.choice(["MAJOR_BUG", "MAJOR_FIX", "PERFORMANCE_ISSUE", "PERFORMANCE_FIX"])
            event_dates[pid][event_date] = event_type

    print("Generating Fact_Daily_Product_Metrics, Log_Customer_Feedback, Log_Support_Ticket...")
    for metric_date_ts in DATE_RANGE:
        metric_date_obj = metric_date_ts.date()

        for product_id in PRODUCT_IDS:
            product_info = dim_product[dim_product['ProductID'] == product_id].iloc[0]
            launch_date = product_info['LaunchDate']

            if metric_date_obj < launch_date:
                continue

            days_since_launch = (metric_date_obj - launch_date).days
            base_users = 50 + days_since_launch * random.uniform(0.5, 5)
            seasonal_mult = simulate_seasonal_multiplier(pd.Series([metric_date_ts]))[0]

            active_campaign_id = None
            campaign_lift = 1.0
            active_campaign = dim_campaign[
                (dim_campaign['TargetProductID'] == product_id) &
                (dim_campaign['CampaignStartDate'].dt.date <= metric_date_obj) &
                (dim_campaign['CampaignEndDate'].dt.date >= metric_date_obj)
            ]
            if not active_campaign.empty:
                active_campaign_id = active_campaign['CampaignID'].iloc[0]
                campaign_lift = random.uniform(1.1, 1.5)

            event_impact_multiplier = 1.0
            event_bug_spike = 0
            event_api_error_spike = 0
            event_uptime_dip = 0
            today_event = event_dates[product_id].get(metric_date_obj)

            if today_event in ["MAJOR_BUG", "PERFORMANCE_ISSUE"]:
                event_impact_multiplier = random.uniform(0.7, 0.9)
                event_bug_spike = random.randint(5, 15) if today_event == "MAJOR_BUG" else 0
                event_api_error_spike = random.uniform(2.0, 5.0) if today_event == "PERFORMANCE_ISSUE" else 0
                event_uptime_dip = random.uniform(0.1, 1.0) if today_event == "PERFORMANCE_ISSUE" else 0
            elif today_event in ["MAJOR_FIX", "PERFORMANCE_FIX"]:
                event_impact_multiplier = random.uniform(1.05, 1.15)

            active_users = int(max(0, simulate_trend_with_noise(base_users, 0.1, base_users * 0.05, 1)[0] * seasonal_mult * campaign_lift * event_impact_multiplier))
            new_signups = int(max(0, simulate_trend_with_noise(active_users * 0.01, 0.01, active_users * 0.005, 1)[0] * campaign_lift * event_impact_multiplier))
            avg_session = max(5.0, simulate_trend_with_noise(10, 0.005, 2, 1)[0] * event_impact_multiplier)
            feature_a_adopt = min(1.0, max(0, simulate_trend_with_noise(0.1 + days_since_launch * 0.0005, 0.0001, 0.05, 1)[0]))
            feature_b_adopt = min(1.0, max(0, simulate_trend_with_noise(0.05 + days_since_launch * 0.0002, 0.00005, 0.03, 1)[0]))
            conversion_rate = min(0.1, max(0.005, simulate_trend_with_noise(0.02, 0.00001, 0.005, 1)[0] * campaign_lift * event_impact_multiplier))
            uptime = max(98.0, min(100.0, simulate_trend_with_noise(99.95, 0, 0.05, 1)[0] - event_uptime_dip))
            bugs_opened = max(0, int(simulate_trend_with_noise(1, 0.001, 0.5, 1)[0] + event_bug_spike))
            bugs_resolved = max(0, int(simulate_trend_with_noise(0.8, 0.001, 0.4, 1)[0]))
            api_error_rate = max(0, min(10.0, simulate_trend_with_noise(0.2, 0.0001, 0.1, 1)[0] + event_api_error_spike))
            page_load_time = max(200, int(simulate_trend_with_noise(1500, -0.1, 100, 1)[0]))

            daily_metric_record = {
                "MetricDate": metric_date_obj,
                "ProductID": product_id,
                "CampaignID_Active": active_campaign_id,
                "ActiveUsers_Daily": active_users,
                "NewUserSignups_Daily": new_signups,
                "AvgSessionDuration_Minutes_Daily": round(avg_session, 2),
                "FeatureAdoptionRate_KeyFeatureA_Daily": round(feature_a_adopt, 4),
                "FeatureAdoptionRate_KeyFeatureB_Daily": round(feature_b_adopt, 4),
                "ConversionRate_WebsiteToTrial_Daily": round(conversion_rate, 4),
                "SystemUptime_Percentage_Daily": round(uptime, 3),
                "CriticalBugs_Opened_Daily": bugs_opened,
                "CriticalBugs_Resolved_Daily": bugs_resolved,
                "API_ErrorRate_Percentage_Daily": round(api_error_rate, 2),
                "AvgPageLoadTime_ms_Daily": page_load_time
            }
            all_daily_metrics.append(daily_metric_record)

            num_feedback = max(0, int(active_users * random.uniform(0.0001, 0.0005)))
            for _ in range(num_feedback):
                feedback_ts = generate_random_timestamp(metric_date_ts, metric_date_ts + datetime.timedelta(days=1) - datetime.timedelta(seconds=1))
                customer_hash = random.choice(customer_hashes)
                source = random.choice(["In-App Survey", "Email Survey", "Support Interaction", "App Store Review", "Website Form"])

                base_nps_prob = [0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.15, 0.2, 0.2, 0.25, 0.3]
                base_csat_prob = [0.05, 0.1, 0.15, 0.3, 0.4]
                
                nps_weights = list(base_nps_prob)
                csat_weights = list(base_csat_prob)

                if today_event in ["MAJOR_BUG", "PERFORMANCE_ISSUE"] or uptime < 99.5 or api_error_rate > 2.0:
                    for i in range(len(nps_weights)): nps_weights[i] *= (1.8 if i < 7 else 0.6)
                    for i in range(len(csat_weights)): csat_weights[i] *= (1.8 if i < 3 else 0.6)
                elif today_event in ["MAJOR_FIX", "PERFORMANCE_FIX"] or campaign_lift > 1.0:
                    for i in range(len(nps_weights)): nps_weights[i] *= (0.6 if i < 7 else 1.8)
                    for i in range(len(csat_weights)): csat_weights[i] *= (0.6 if i < 3 else 1.8)
                
                nps_weights = [max(0.01, w) for w in nps_weights]
                csat_weights = [max(0.01, w) for w in csat_weights]
                nps_score = random.choices(range(11), weights=nps_weights, k=1)[0]
                csat_score = random.choices(range(1, 6), weights=csat_weights, k=1)[0]
                ces_score = random.randint(1, 7)

                sentiment = "Negative" if nps_score <= 6 else ("Neutral" if nps_score <= 8 else "Positive")
                topics = []
                if sentiment == "Negative":
                    topics.append(random.choice(["Performance", "Bug", "Usability", "Missing Feature", "Support", "Price"]))
                    if bugs_opened > 2 and random.random() < 0.3: topics.append("Bug")
                    if avg_session < 8 and random.random() < 0.3: topics.append("Usability")
                    if page_load_time > 2000 and random.random() < 0.3 : topics.append("Performance")
                elif sentiment == "Positive":
                    topics.append(random.choice(["Ease of Use", "FeatureA", "Value", "Support", "Speed"]))
                    if feature_a_adopt > 0.5 and random.random() < 0.3: topics.append("FeatureA")

                feedback_record = {
                    "FeedbackID": f"FDBK_{uuid.uuid4().hex[:10]}",
                    "FeedbackTimestamp": feedback_ts,
                    "ProductID": product_id,
                    "CustomerID_Hashed": customer_hash,
                    "FeedbackSource": source,
                    "NPS_Score": nps_score,
                    "CSAT_Score": csat_score,
                    "CES_Score": ces_score,
                    "FeedbackText_Raw": f"{sentiment} feedback about {','.join(set(topics)) if topics else 'general use'}. Product: {product_id}",
                    "Sentiment_Automated": sentiment,
                    "KeyTopics_Automated": ','.join(set(topics)) if topics else None
                }
                all_feedback_logs.append(feedback_record)

            num_tickets = max(0, int(active_users * random.uniform(0.0002, 0.0008) + bugs_opened * random.uniform(0.1, 0.3)))
            for _ in range(num_tickets):
                creation_ts = generate_random_timestamp(metric_date_ts, metric_date_ts + datetime.timedelta(days=1) - datetime.timedelta(seconds=1))
                customer_hash = random.choice(customer_hashes)
                severity = random.choices(["Critical", "High", "Medium", "Low"], weights=[0.05, 0.15, 0.5, 0.3], k=1)[0]
                category = random.choice(["Bug Report", "Feature Request", "Billing Inquiry", "Usability Problem", "Account Access", "How-To Question"])
                if bugs_opened > 2 and random.random() < 0.5: category = "Bug Report"
                elif today_event == "MAJOR_BUG" and random.random() < 0.6: category = "Bug Report"


                status = random.choices(["Open", "In Progress", "Resolved", "Closed"], weights=[0.1, 0.2, 0.5, 0.2], k=1)[0]
                resolution_ts = None
                time_to_res = None
                first_resp_time = None

                if status in ["Resolved", "Closed"]:
                    resolution_delay_hours = random.uniform(0.5, 48) if severity != "Critical" else random.uniform(0.2, 6)
                    resolution_ts_candidate = creation_ts + datetime.timedelta(hours=resolution_delay_hours) # resolution_ts_candidate is datetime.datetime
                    
                    # Ensure resolution_ts_candidate's date part is not beyond END_DATE
                    if resolution_ts_candidate.date() > END_DATE: # CORRECTED: Compare with END_DATE directly
                        resolution_ts = datetime.datetime.combine(min(END_DATE, creation_ts.date() + datetime.timedelta(days=7)), 
                                                                datetime.time(random.randint(0,23),random.randint(0,59)))
                    else:
                        resolution_ts = resolution_ts_candidate

                    time_to_res = round(max(0.1, (resolution_ts - creation_ts).total_seconds() / 3600), 2)
                    first_resp_time = round(random.uniform(5, min(120, time_to_res * 60 if time_to_res > 0.1 else 120)), 1)
                elif status == "In Progress":
                    if random.random() < 0.9:
                        first_resp_time = round(random.uniform(5, 120), 1)

                ticket_record = {
                    "TicketID": f"SUP_{uuid.uuid4().hex[:10]}",
                    "CreationTimestamp": creation_ts,
                    "ProductID": product_id,
                    "CustomerID_Hashed": customer_hash,
                    "TeamID_Assigned": random.choice(TEAM_IDS) if random.random() < 0.8 else None,
                    "IssueCategory": category,
                    "TicketSeverity": severity,
                    "TicketStatus": status,
                    "ResolutionTimestamp": resolution_ts,
                    "TimeToResolution_Hours": time_to_res,
                    "FirstResponseTime_Minutes": first_resp_time
                }
                all_support_tickets.append(ticket_record)

        if metric_date_ts.day == 1 and metric_date_ts.month % 3 == 1:
            print(f"  Processed data up to {metric_date_obj}...")


    print("Converting generated lists to DataFrames...")
    fact_daily_metrics = pd.DataFrame(all_daily_metrics)
    log_customer_feedback = pd.DataFrame(all_feedback_logs)
    log_support_ticket = pd.DataFrame(all_support_tickets)

    print("Performing final data type conversions...")
    dim_product['LaunchDate'] = pd.to_datetime(dim_product['LaunchDate']).dt.date

    fact_daily_metrics['MetricDate'] = pd.to_datetime(fact_daily_metrics['MetricDate']).dt.date
    fact_daily_metrics = fact_daily_metrics.astype({
        "ProductID": "string", "CampaignID_Active": "string",
        "ActiveUsers_Daily": "int32", "NewUserSignups_Daily": "int32",
        "AvgSessionDuration_Minutes_Daily": "float64",
        "FeatureAdoptionRate_KeyFeatureA_Daily": "float64",
        "FeatureAdoptionRate_KeyFeatureB_Daily": "float64",
        "ConversionRate_WebsiteToTrial_Daily": "float64",
        "SystemUptime_Percentage_Daily": "float64",
        "CriticalBugs_Opened_Daily": "int32",
        "CriticalBugs_Resolved_Daily": "int32",
        "API_ErrorRate_Percentage_Daily": "float64",
        "AvgPageLoadTime_ms_Daily": "int32"
    })

    log_customer_feedback['FeedbackTimestamp'] = pd.to_datetime(log_customer_feedback['FeedbackTimestamp'])
    log_customer_feedback = log_customer_feedback.astype({
        "FeedbackID": "string", "ProductID": "string", "CustomerID_Hashed": "string",
        "FeedbackSource": "string", "NPS_Score": "Int64", "CSAT_Score": "Int64", "CES_Score": "Int64",
        "FeedbackText_Raw": "string", "Sentiment_Automated": "string", "KeyTopics_Automated": "string"
    })

    log_support_ticket['CreationTimestamp'] = pd.to_datetime(log_support_ticket['CreationTimestamp'])
    log_support_ticket['ResolutionTimestamp'] = pd.to_datetime(log_support_ticket['ResolutionTimestamp'], errors='coerce')
    log_support_ticket = log_support_ticket.astype({
        "TicketID": "string", "ProductID": "string", "CustomerID_Hashed": "string",
        "TeamID_Assigned": "string", "IssueCategory": "string", "TicketSeverity": "string",
        "TicketStatus": "string", "TimeToResolution_Hours": "float64", "FirstResponseTime_Minutes": "float64"
    })

    print("\n--- Generated DataFrames ---")
    print("\nDimension Tables:")
    print(f"Dim_Product Shape: {dim_product.shape}")
    print(dim_product.head())
    print(f"\nDim_Team Shape: {dim_team.shape}")
    print(dim_team.head())
    print(f"\nDim_Campaign Shape: {dim_campaign.shape}")
    print(dim_campaign.head())

    print("\nFact & Log Tables:")
    print(f"Fact_Daily_Product_Metrics Shape: {fact_daily_metrics.shape}")
    print(fact_daily_metrics.head())
    print(f"\nLog_Customer_Feedback Shape: {log_customer_feedback.shape}")
    print(log_customer_feedback.head())
    print(f"\nLog_Support_Ticket Shape: {log_support_ticket.shape}")
    print(log_support_ticket.head())

    # --- Optional: Save to CSV ---
    print("\nSaving DataFrames to CSV files...")
    dim_product.to_csv("dim_product.csv", index=False)
    dim_team.to_csv("dim_team.csv", index=False)
    dim_campaign.to_csv("dim_campaign.csv", index=False)
    fact_daily_metrics.to_csv("fact_daily_product_metrics.csv", index=False)
    log_customer_feedback.to_csv("log_customer_feedback.csv", index=False)
    log_support_ticket.to_csv("log_support_ticket.csv", index=False)
    print("CSV files saved.")

    print("\n--- Data Generation Complete ---")

# Only run if script is executed directly
if __name__ == "__main__":
    main()