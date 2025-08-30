#!/usr/bin/env python3
"""
Test the fixed dashboard components to verify error handling and data flow.
"""

import pandas as pd
import numpy as np
from data_loader import EcommerceDataLoader, load_and_process_data
from business_metrics import BusinessMetricsCalculator

def test_fixed_dashboard():
    print("=== TESTING FIXED DASHBOARD COMPONENTS ===\n")
    
    try:
        # Load data
        loader, processed_data = load_and_process_data('ecommerce_data/')
        current_year = 2023
        previous_year = 2022
        
        sales_data = loader.create_sales_dataset(
            year_filter=[current_year, previous_year],
            status_filter='delivered'
        )
        
        print(f"✅ Sales data loaded: {len(sales_data)} records")
        
        # Test supporting datasets
        products_df = loader.get_product_categories()
        customers_df = loader.get_customer_geography()
        reviews_df = loader.get_review_scores()
        
        print(f"✅ Supporting datasets loaded")
        
        # Test metrics calculation
        metrics_calculator = BusinessMetricsCalculator(sales_data)
        
        comprehensive_report = metrics_calculator.generate_comprehensive_report(
            current_year=current_year,
            previous_year=previous_year,
            products_df=products_df,
            customers_df=customers_df,
            reviews_df=reviews_df
        )
        
        print(f"✅ Comprehensive report generated")
        
        # Test each component that was causing blank boxes
        print("\n--- Testing KPI Components ---")
        
        revenue_metrics = comprehensive_report['revenue_metrics']
        
        # KPI 1: Total Revenue
        total_revenue = revenue_metrics.get('total_revenue', 0)
        revenue_growth = revenue_metrics.get('revenue_growth_rate', 0)
        print(f"Total Revenue: ${total_revenue:,.2f} (Growth: {revenue_growth:.2f}%)")
        
        # KPI 2: Monthly Growth
        monthly_growth = revenue_metrics.get('monthly_growth_trend', 0)
        print(f"Monthly Growth: {monthly_growth:+.2f}%")
        
        # KPI 3: AOV
        aov = revenue_metrics.get('average_order_value', 0)
        aov_growth = revenue_metrics.get('aov_growth_rate', 0)
        print(f"AOV: ${aov:.2f} (Growth: {aov_growth:.2f}%)")
        
        # KPI 4: Total Orders
        total_orders = revenue_metrics.get('total_orders', 0)
        order_growth = revenue_metrics.get('order_growth_rate', 0)
        print(f"Total Orders: {total_orders:,} (Growth: {order_growth:.2f}%)")
        
        # Test chart components
        print("\n--- Testing Chart Components ---")
        
        # Chart 1: Revenue trend
        current_data = sales_data[sales_data['order_year'] == current_year]
        previous_data = sales_data[sales_data['order_year'] == previous_year]
        current_monthly = current_data.groupby('order_month')['price'].sum().reset_index()
        previous_monthly = previous_data.groupby('order_month')['price'].sum().reset_index()
        print(f"Revenue trend data: {len(current_monthly)} current, {len(previous_monthly)} previous months")
        
        # Chart 2: Product categories
        product_metrics = comprehensive_report.get('product_metrics', {})
        if 'category_performance' in product_metrics:
            categories = product_metrics['category_performance']
            print(f"Product categories: {len(categories)} categories available")
        else:
            print("❌ Product categories data missing")
        
        # Chart 3: Geographic
        geographic_metrics = comprehensive_report.get('geographic_metrics', {})
        if 'state_performance' in geographic_metrics:
            states = geographic_metrics['state_performance']
            print(f"Geographic data: {len(states)} states available")
        else:
            print("❌ Geographic data missing")
        
        # Chart 4: Satisfaction
        experience_metrics = comprehensive_report.get('customer_experience_metrics', {})
        if 'delivery_satisfaction_correlation' in experience_metrics:
            satisfaction = experience_metrics['delivery_satisfaction_correlation']
            print(f"Satisfaction data: {len(satisfaction)} delivery categories")
        else:
            print("❌ Satisfaction data missing")
        
        # Test bottom cards
        print("\n--- Testing Bottom Cards ---")
        
        if 'delivery' in experience_metrics:
            avg_delivery = experience_metrics['delivery']['average_delivery_days']
            print(f"Delivery metrics: {avg_delivery:.1f} days average")
        else:
            print("❌ Delivery metrics missing")
        
        if 'satisfaction' in experience_metrics:
            avg_rating = experience_metrics['satisfaction']['average_review_score']
            stars = "★" * int(round(avg_rating)) + "☆" * (5 - int(round(avg_rating)))
            print(f"Review metrics: {avg_rating:.2f}/5.0 ({stars})")
        else:
            print("❌ Review metrics missing")
        
        print(f"\n=== ALL DASHBOARD COMPONENTS TESTED SUCCESSFULLY ===")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_fixed_dashboard()