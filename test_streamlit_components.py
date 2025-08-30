#!/usr/bin/env python3
"""
Test individual dashboard components to identify rendering issues.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from data_loader import EcommerceDataLoader, load_and_process_data
from business_metrics import BusinessMetricsCalculator

def test_dashboard_components():
    print("=== TESTING INDIVIDUAL DASHBOARD COMPONENTS ===\n")
    
    # Load data
    loader, processed_data = load_and_process_data('ecommerce_data/')
    current_year = 2023
    previous_year = 2022
    
    sales_data = loader.create_sales_dataset(
        year_filter=[current_year, previous_year],
        status_filter='delivered'
    )
    
    products_df = loader.get_product_categories()
    customers_df = loader.get_customer_geography()
    reviews_df = loader.get_review_scores()
    
    metrics_calculator = BusinessMetricsCalculator(sales_data)
    
    comprehensive_report = metrics_calculator.generate_comprehensive_report(
        current_year=current_year,
        previous_year=previous_year,
        products_df=products_df,
        customers_df=customers_df,
        reviews_df=reviews_df
    )
    
    # Test format_number function
    print("1. Testing format_number function...")
    def format_number(num, prefix="$"):
        if num >= 1_000_000:
            return f"{prefix}{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{prefix}{num/1_000:.0f}K"
        else:
            return f"{prefix}{num:.0f}"
    
    test_values = [3360294.74, 724.98, 4635]
    for val in test_values:
        formatted = format_number(val)
        print(f"   {val} -> {formatted}")
    
    # Test format_percentage function
    print("\n2. Testing format_percentage function...")
    def format_percentage(num):
        if num >= 0:
            return f"↑ +{num:.2f}%", "trend-positive"
        else:
            return f"↓ {num:.2f}%", "trend-negative"
    
    test_percentages = [2.5, -2.46, 0.0]
    for pct in test_percentages:
        text, css_class = format_percentage(pct)
        print(f"   {pct}% -> {text} ({css_class})")
    
    # Test KPI metrics extraction
    print("\n3. Testing KPI metrics extraction...")
    revenue_metrics = comprehensive_report['revenue_metrics']
    
    print(f"   Total Revenue: {revenue_metrics.get('total_revenue', 'MISSING')}")
    print(f"   Monthly Growth: {revenue_metrics.get('monthly_growth_trend', 'MISSING')}")
    print(f"   AOV: {revenue_metrics.get('average_order_value', 'MISSING')}")
    print(f"   Total Orders: {revenue_metrics.get('total_orders', 'MISSING')}")
    print(f"   Revenue Growth: {revenue_metrics.get('revenue_growth_rate', 'MISSING')}")
    print(f"   AOV Growth: {revenue_metrics.get('aov_growth_rate', 'MISSING')}")
    print(f"   Order Growth: {revenue_metrics.get('order_growth_rate', 'MISSING')}")
    
    # Test chart data preparation
    print("\n4. Testing chart data preparation...")
    
    # Revenue trend data
    current_data = sales_data[sales_data['order_year'] == current_year]
    previous_data = sales_data[sales_data['order_year'] == previous_year]
    
    current_monthly = current_data.groupby('order_month')['price'].sum().reset_index()
    previous_monthly = previous_data.groupby('order_month')['price'].sum().reset_index()
    
    print(f"   Current year monthly data: {len(current_monthly)} months")
    print(f"   Previous year monthly data: {len(previous_monthly)} months")
    
    # Product categories data
    if 'product_metrics' in comprehensive_report:
        product_metrics = comprehensive_report['product_metrics']
        top_10 = product_metrics['category_performance'].head(10)
        print(f"   Top 10 categories: {len(top_10)} records")
        print(f"   Top category: {top_10.index[0] if not top_10.empty else 'NONE'}")
    
    # Geographic data
    if 'geographic_metrics' in comprehensive_report:
        geographic_metrics = comprehensive_report['geographic_metrics']
        state_data = geographic_metrics['state_performance'].reset_index()
        print(f"   State data: {len(state_data)} states")
        print(f"   Required columns: {list(state_data.columns)}")
    
    # Customer experience data
    if 'customer_experience_metrics' in comprehensive_report:
        experience_metrics = comprehensive_report['customer_experience_metrics']
        delivery_satisfaction = experience_metrics.get('delivery_satisfaction_correlation', {})
        print(f"   Delivery satisfaction data: {len(delivery_satisfaction)} categories")
        print(f"   Categories: {list(delivery_satisfaction.keys())}")
        
        # Check delivery and satisfaction metrics
        satisfaction = experience_metrics.get('satisfaction', {})
        delivery = experience_metrics.get('delivery', {})
        
        print(f"   Avg review score: {satisfaction.get('average_review_score', 'MISSING')}")
        print(f"   Avg delivery days: {delivery.get('average_delivery_days', 'MISSING')}")
    
    print("\n=== COMPONENT TESTING COMPLETE ===")

if __name__ == "__main__":
    test_dashboard_components()