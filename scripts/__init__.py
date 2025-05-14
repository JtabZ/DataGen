# scripts/__init__.py
"""
CBS Data Generator Scripts Package

Contains all data generation scripts for different CBS industry use cases.
"""

from .tech_metrics_wrapper import TechMetricsGenerator
from .marketing_wrapper import MarketingDataGenerator
from .loan_risk_wrapper import LoanRiskGenerator

# Future imports will be added here as scripts are created
# from .loan_risk import LoanRiskGenerator
# from .credit_card import CreditCardGenerator
# from .marketing import MarketingDataGenerator
# from .tax_data import TaxDataGenerator
# from .financial_statements import FinancialStatementsGenerator

__all__ = ['TechMetricsGenerator', 'MarketingDataGenerator', 'LoanRiskGenerator']