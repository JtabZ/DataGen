# CBS Data Generator Suite

A Streamlit-based web application for generating synthetic data across various Consumer & Business Services (CBS) industries. Generate realistic test data for development, testing, and demonstration purposes.

## Features

- **Multiple Industry Generators**: Support for 6 different CBS sub-industries
- **Configurable Parameters**: Adjust data characteristics through an intuitive UI
- **Realistic Data**: Generates interconnected data with realistic patterns and relationships
- **Download Options**: Export individual CSV files or download all as a ZIP
- **Data Preview**: View sample data before downloading

## Available Generators

1. **Tech Product & Project Management** ✅
   - Product metrics and KPIs
   - Development team information
   - Marketing campaigns
   - Customer feedback and NPS scores
   - Support tickets

2. **Loan & Risk Performance** 🚧 (Coming Soon)
   - Loan portfolios
   - Risk metrics
   - Default rates
   - Payment histories

3. **Credit Card Applications** 🚧 (Coming Soon)
   - Application data
   - Approval rates
   - Usage patterns
   - Transaction history

4. **Marketing Data** 🚧 (Coming Soon)
   - Customer segments
   - Campaign performance
   - Attribution data
   - ROI metrics

5. **Tax Data** 🚧 (Coming Soon)
   - Tax returns
   - Deductions
   - Compliance data
   - Audit trails

6. **Financial Statements** 🚧 (Coming Soon)
   - Balance sheets
   - Income statements
   - Cash flow statements
   - Financial ratios

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd cbs-data-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Select a Generator**: Choose from the available data generators in the sidebar
2. **Configure Parameters**: Adjust settings like date ranges, record counts, and data characteristics
3. **Generate Data**: Click the "Generate Data" button
4. **Preview Results**: View sample data in the preview tabs
5. **Download**: Export individual CSV files or download all as a ZIP

## Project Structure

```
cbs-data-generator/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── scripts/
│   ├── __init__.py
│   ├── tech_metrics.py       # Tech company data generator
│   ├── loan_risk.py          # Loan data generator (placeholder)
│   ├── credit_card.py        # Credit card generator (placeholder)
│   ├── marketing.py          # Marketing generator (placeholder)
│   ├── tax_data.py           # Tax data generator (placeholder)
│   └── financial_statements.py # Financial generator (placeholder)
└── utils/
    ├── __init__.py
    └── helpers.py            # Common utility functions
```

## Configuration

Each generator has its own set of configurable parameters:

### Tech Product & Project Management
- Number of products, teams, campaigns, and customers
- Historical and future date ranges
- Bug frequency and growth trends
- Seasonal variations
- Optional data components (feedback, tickets)

## Adding New Generators

To add a new data generator:

1. Create a new Python file in the `scripts/` directory
2. Implement a generator class with:
   - `__init__` method accepting parameters
   - `get_config()` static method returning parameter configuration
   - `generate()` method returning a dictionary of DataFrames
3. Import the generator in `scripts/__init__.py`
4. Add the generator configuration to the `GENERATORS` dictionary in `app.py`

## Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy with one click

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-generator`)
3. Commit your changes (`git commit -am 'Add new generator'`)
4. Push to the branch (`git push origin feature/new-generator`)
5. Create a Pull Request

## License

[Your License]

## Contact

[Your Contact Information]