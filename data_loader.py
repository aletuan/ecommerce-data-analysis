"""
Data Loading and Processing Module for E-commerce Analysis

This module provides functions for loading, cleaning, and processing e-commerce datasets
including orders, products, customers, and reviews data.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional, Union
import warnings

# Suppress pandas warnings for cleaner output
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)


class EcommerceDataLoader:
    """
    A class for loading and processing e-commerce datasets.
    
    This class handles the loading of multiple CSV files and provides methods
    for creating analysis-ready datasets with proper data types and relationships.
    """
    
    def __init__(self, data_path: str = 'ecommerce_data/'):
        """
        Initialize the data loader with the path to data files.
        
        Args:
            data_path (str): Path to directory containing CSV files
        """
        self.data_path = data_path
        self.raw_data = {}
        self.processed_data = {}
        
    def load_raw_data(self) -> Dict[str, pd.DataFrame]:
        """
        Load all raw CSV files into DataFrames.
        
        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing all loaded datasets
        """
        datasets = {
            'orders': 'orders_dataset.csv',
            'order_items': 'order_items_dataset.csv', 
            'products': 'products_dataset.csv',
            'customers': 'customers_dataset.csv',
            'reviews': 'order_reviews_dataset.csv',
            'payments': 'order_payments_dataset.csv'
        }
        
        for name, filename in datasets.items():
            filepath = f"{self.data_path}{filename}"
            self.raw_data[name] = pd.read_csv(filepath)
            print(f"Loaded {name}: {len(self.raw_data[name]):,} records")
            
        return self.raw_data
    
    def process_datetime_columns(self) -> None:
        """Convert string datetime columns to pandas datetime objects."""
        datetime_columns = {
            'orders': ['order_purchase_timestamp', 'order_approved_at', 
                      'order_delivered_carrier_date', 'order_delivered_customer_date',
                      'order_estimated_delivery_date'],
            'reviews': ['review_creation_date', 'review_answer_timestamp']
        }
        
        for dataset_name, columns in datetime_columns.items():
            if dataset_name in self.raw_data:
                for col in columns:
                    if col in self.raw_data[dataset_name].columns:
                        self.raw_data[dataset_name][col] = pd.to_datetime(
                            self.raw_data[dataset_name][col], errors='coerce'
                        )
    
    def add_derived_columns(self) -> None:
        """Add useful derived columns for analysis."""
        if 'orders' in self.raw_data:
            # Add year and month columns for filtering
            orders_df = self.raw_data['orders'].copy()
            orders_df['order_year'] = orders_df['order_purchase_timestamp'].dt.year
            orders_df['order_month'] = orders_df['order_purchase_timestamp'].dt.month
            orders_df['order_day'] = orders_df['order_purchase_timestamp'].dt.day
            orders_df['order_weekday'] = orders_df['order_purchase_timestamp'].dt.day_name()
            
            # Calculate delivery time in days
            orders_df['delivery_days'] = (
                orders_df['order_delivered_customer_date'] - 
                orders_df['order_purchase_timestamp']
            ).dt.days
            
            self.processed_data['orders'] = orders_df
        
        # Copy other datasets to processed_data
        for name, df in self.raw_data.items():
            if name != 'orders':
                self.processed_data[name] = df.copy()
    
    def create_sales_dataset(self, 
                           year_filter: Optional[Union[int, list]] = None,
                           month_filter: Optional[Union[int, list]] = None,
                           status_filter: str = 'delivered') -> pd.DataFrame:
        """
        Create a comprehensive sales dataset by joining orders and order_items.
        
        Args:
            year_filter: Year(s) to filter data. Can be int or list of ints
            month_filter: Month(s) to filter data. Can be int or list of ints  
            status_filter: Order status to filter ('delivered', 'shipped', etc.)
            
        Returns:
            pd.DataFrame: Merged and filtered sales dataset
        """
        # Get base datasets
        orders = self.processed_data['orders'].copy()
        order_items = self.processed_data['order_items'].copy()
        
        # Apply filters
        if status_filter:
            orders = orders[orders['order_status'] == status_filter]
            
        if year_filter is not None:
            if isinstance(year_filter, (int, np.integer)):
                year_filter = [year_filter]
            orders = orders[orders['order_year'].isin(year_filter)]
            
        if month_filter is not None:
            if isinstance(month_filter, (int, np.integer)):
                month_filter = [month_filter]
            orders = orders[orders['order_month'].isin(month_filter)]
        
        # Merge datasets
        sales_data = pd.merge(
            left=order_items[['order_id', 'order_item_id', 'product_id', 'price', 'freight_value']],
            right=orders[['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp',
                         'order_delivered_customer_date', 'order_year', 'order_month', 'delivery_days']],
            on='order_id',
            how='inner'
        )
        
        print(f"Created sales dataset: {len(sales_data):,} records")
        if year_filter:
            print(f"Filtered to year(s): {year_filter}")
        if month_filter:
            print(f"Filtered to month(s): {month_filter}")
        if status_filter:
            print(f"Filtered to status: {status_filter}")
            
        return sales_data
    
    def get_product_categories(self) -> pd.DataFrame:
        """
        Get product category information merged with sales data.
        
        Returns:
            pd.DataFrame: Products dataset with category information
        """
        return self.processed_data['products'][['product_id', 'product_category_name']].copy()
    
    def get_customer_geography(self) -> pd.DataFrame:
        """
        Get customer geographic information.
        
        Returns:
            pd.DataFrame: Customers dataset with location data
        """
        return self.processed_data['customers'][['customer_id', 'customer_state', 'customer_city']].copy()
    
    def get_review_scores(self) -> pd.DataFrame:
        """
        Get review scores and feedback data.
        
        Returns:
            pd.DataFrame: Reviews dataset with scores and timestamps
        """
        return self.processed_data['reviews'][['order_id', 'review_score', 'review_creation_date']].copy()
    
    def process_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Complete data processing pipeline.
        
        Returns:
            Dict[str, pd.DataFrame]: All processed datasets
        """
        print("Processing e-commerce datasets...")
        self.load_raw_data()
        self.process_datetime_columns()
        self.add_derived_columns()
        print("Data processing completed successfully!")
        return self.processed_data


def load_and_process_data(data_path: str = 'ecommerce_data/') -> Tuple[EcommerceDataLoader, Dict[str, pd.DataFrame]]:
    """
    Convenience function to load and process all e-commerce data.
    
    Args:
        data_path (str): Path to directory containing CSV files
        
    Returns:
        Tuple[EcommerceDataLoader, Dict[str, pd.DataFrame]]: Loader instance and processed data
    """
    loader = EcommerceDataLoader(data_path)
    processed_data = loader.process_all_data()
    return loader, processed_data


def get_data_summary(processed_data: Dict[str, pd.DataFrame]) -> None:
    """
    Print summary statistics for all datasets.
    
    Args:
        processed_data: Dictionary of processed DataFrames
    """
    print("\n" + "="*50)
    print("E-COMMERCE DATA SUMMARY")
    print("="*50)
    
    for name, df in processed_data.items():
        print(f"\n{name.upper()}:")
        print(f"  Records: {len(df):,}")
        print(f"  Columns: {len(df.columns)}")
        
        # Show unique values for key columns
        if name == 'orders':
            print(f"  Unique orders: {df['order_id'].nunique():,}")
            print(f"  Order statuses: {df['order_status'].nunique()}")
            print(f"  Date range: {df['order_purchase_timestamp'].min().date()} to {df['order_purchase_timestamp'].max().date()}")
        elif name == 'products':
            print(f"  Unique products: {df['product_id'].nunique():,}")
            print(f"  Product categories: {df['product_category_name'].nunique()}")
        elif name == 'customers':
            print(f"  Unique customers: {df['customer_id'].nunique():,}")
            print(f"  States: {df['customer_state'].nunique()}")
        elif name == 'reviews':
            print(f"  Average review score: {df['review_score'].mean():.2f}/5.0")
            print(f"  Review score range: {df['review_score'].min()}-{df['review_score'].max()}")