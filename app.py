import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import zipfile
import io
import base64
from scripts.tech_metrics_wrapper import TechMetricsGenerator
from scripts.marketing_wrapper import MarketingDataGenerator  # Import the new generator

# Page configuration
st.set_page_config(
    page_title="CBS Data Generator Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .generator-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #E2E8F0;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">CBS Data Generator Suite</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Generate realistic synthetic data for Consumer & Business Services</p>', unsafe_allow_html=True)

# Initialize session state
if 'generated_data' not in st.session_state:
    st.session_state.generated_data = None
if 'generator_instance' not in st.session_state:
    st.session_state.generator_instance = None

# Define available generators
GENERATORS = {
    "tech_metrics": {
        "name": "Tech Product & Project Management",
        "description": "Generate product metrics, team data, campaigns, customer feedback, and support tickets",
        "icon": "💻",
        "generator_class": TechMetricsGenerator,
        "available": True
    },
    "loan_risk": {
        "name": "Loan & Risk Performance",
        "description": "Generate loan portfolios, risk metrics, default rates, and payment histories",
        "icon": "💰",
        "generator_class": None,  # Placeholder
        "available": False
    },
    "credit_card": {
        "name": "Credit Card Applications",
        "description": "Generate credit card application data, approval rates, and usage patterns",
        "icon": "💳",
        "generator_class": None,  # Placeholder
        "available": False
    },
    "marketing": {
        "name": "Marketing Data",
        "description": "Generate marketing funnel data with channels, campaigns, and conversion metrics",
        "icon": "📈",
        "generator_class": MarketingDataGenerator,
        "available": True
    },
    "tax_data": {
        "name": "Tax Data",
        "description": "Generate tax returns, deductions, and compliance data",
        "icon": "📋",
        "generator_class": None,  # Placeholder
        "available": False
    },
    "financial_statements": {
        "name": "Financial Statements",
        "description": "Generate balance sheets, income statements, and cash flow data",
        "icon": "📊",
        "generator_class": None,  # Placeholder
        "available": False
    }
}

# Sidebar for generator selection
with st.sidebar:
    st.header("Select Data Generator")
    
    # Create selection buttons for each generator
    selected_generator = None
    for key, gen_info in GENERATORS.items():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.write(gen_info["icon"])
        with col2:
            if st.button(
                gen_info["name"],
                key=f"btn_{key}",
                disabled=not gen_info["available"],
                use_container_width=True
            ):
                selected_generator = key
                st.session_state.selected_generator = key
    
    # Get the selected generator from session state
    if 'selected_generator' in st.session_state:
        selected_generator = st.session_state.selected_generator

# Main content area
if selected_generator:
    gen_info = GENERATORS[selected_generator]
    
    # Generator header
    col1, col2 = st.columns([1, 11])
    with col1:
        st.write(gen_info["icon"])
    with col2:
        st.header(gen_info["name"])
    
    st.write(gen_info["description"])
    
    if gen_info["available"]:
        # Initialize generator
        generator_class = gen_info["generator_class"]
        
        # Parameter configuration section
        st.subheader("Configuration Parameters")
        
        # Get parameter configuration from generator
        param_config = generator_class.get_config()
        
        # Create dynamic form based on parameter configuration
        params = {}
        
        # Organize parameters into columns for better layout
        col1, col2, col3 = st.columns(3)
        
        param_items = list(param_config['parameters'].items())
        for idx, (param_name, param_info) in enumerate(param_items):
            # Distribute parameters across columns
            with [col1, col2, col3][idx % 3]:
                if param_info['type'] == 'number':
                    params[param_name] = st.number_input(
                        param_info.get('label', param_name.replace('_', ' ').title()),
                        min_value=param_info.get('min', 0),
                        max_value=param_info.get('max', 1000000),
                        value=param_info.get('default', 10),
                        help=param_info.get('help', '')
                    )
                elif param_info['type'] == 'date':
                    params[param_name] = st.date_input(
                        param_info.get('label', param_name.replace('_', ' ').title()),
                        value=param_info.get('default', datetime.now().date()),
                        help=param_info.get('help', '')
                    )
                elif param_info['type'] == 'select':
                    params[param_name] = st.selectbox(
                        param_info.get('label', param_name.replace('_', ' ').title()),
                        options=param_info.get('options', []),
                        index=param_info.get('default_index', 0),
                        help=param_info.get('help', '')
                    )
                elif param_info['type'] == 'boolean':
                    params[param_name] = st.checkbox(
                        param_info.get('label', param_name.replace('_', ' ').title()),
                        value=param_info.get('default', False),
                        help=param_info.get('help', '')
                    )
        
        # Generate button
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            generate_button = st.button("🚀 Generate Data", type="primary", use_container_width=True)
        
        # Generate data when button is clicked
        if generate_button:
            with st.spinner("Generating data... This may take a moment."):
                try:
                    # Create generator instance with parameters
                    generator = generator_class(**params)
                    
                    # Generate data
                    generated_data = generator.generate()
                    
                    # Store in session state
                    st.session_state.generated_data = generated_data
                    st.session_state.generator_instance = generator
                    
                    st.success("✅ Data generated successfully!")
                    
                except Exception as e:
                    st.error(f"Error generating data: {str(e)}")
                    st.exception(e)
        
        # Display results if data has been generated
        if st.session_state.generated_data:
            st.subheader("Generated Data")
            
            # Create tabs for different dataframes
            dataframes = st.session_state.generated_data
            tab_names = list(dataframes.keys())
            tabs = st.tabs(tab_names)
            
            for idx, (tab_name, df) in enumerate(dataframes.items()):
                with tabs[idx]:
                    # Show dataframe info
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Rows", f"{len(df):,}")
                    with col2:
                        st.metric("Columns", f"{len(df.columns):,}")
                    with col3:
                        memory_usage = df.memory_usage(deep=True).sum() / 1024**2
                        st.metric("Memory", f"{memory_usage:.1f} MB")
                    
                    # Show sample data
                    st.write("**Sample Data (first 10 rows):**")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    # Show data types
                    with st.expander("Data Types"):
                        st.write(df.dtypes)
            
            # Download section
            st.subheader("Download Generated Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Individual CSV downloads
                st.write("**Download Individual Files:**")
                for name, df in dataframes.items():
                    csv = df.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="{name}.csv">📥 Download {name}.csv</a>'
                    st.markdown(href, unsafe_allow_html=True)
            
            with col2:
                # ZIP download
                st.write("**Download All Files (ZIP):**")
                
                # Create ZIP file in memory
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    for name, df in dataframes.items():
                        csv_buffer = io.StringIO()
                        df.to_csv(csv_buffer, index=False)
                        zip_file.writestr(f"{name}.csv", csv_buffer.getvalue())
                
                zip_buffer.seek(0)
                
                st.download_button(
                    label="📦 Download All (ZIP)",
                    data=zip_buffer.getvalue(),
                    file_name=f"{selected_generator}_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    type="primary"
                )
    else:
        st.info("🚧 This generator is coming soon! Check back later.")
else:
    # Welcome screen when no generator is selected
    st.info("👈 Select a data generator from the sidebar to get started")
    
    # Show available generators in a grid
    st.subheader("Available Generators")
    
    cols = st.columns(3)
    for idx, (key, gen_info) in enumerate(GENERATORS.items()):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f"""
                <div class="generator-card">
                    <h3>{gen_info["icon"]} {gen_info["name"]}</h3>
                    <p>{gen_info["description"]}</p>
                    <p><strong>Status:</strong> {"✅ Available" if gen_info["available"] else "🚧 Coming Soon"}</p>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #64748B;">
        CBS Data Generator Suite | Generate synthetic data for testing and development
    </div>
    """,
    unsafe_allow_html=True
)