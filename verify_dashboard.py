#!/usr/bin/env python3
"""
Verification script to ensure the dashboard can be imported and basic functions work.
"""

def verify_dashboard():
    print("=== VERIFYING DASHBOARD FUNCTIONALITY ===\n")
    
    try:
        # Test imports
        print("1. Testing imports...")
        import streamlit as st
        from dashboard import (
            load_data, format_number, format_percentage,
            create_revenue_trend_chart, create_category_chart,
            create_choropleth_map, create_satisfaction_delivery_chart
        )
        print("✅ All dashboard functions imported successfully")
        
        # Test utility functions
        print("\n2. Testing utility functions...")
        
        # Test format_number
        assert format_number(3360294.74) == "$3.4M"
        assert format_number(724.98) == "$725"
        assert format_number(4635) == "$5K"
        print("✅ format_number working correctly")
        
        # Test format_percentage
        trend_text, trend_class = format_percentage(2.5)
        assert trend_text == "↑ +2.50%" and trend_class == "trend-positive"
        
        trend_text, trend_class = format_percentage(-2.46)
        assert trend_text == "↓ -2.46%" and trend_class == "trend-negative"
        print("✅ format_percentage working correctly")
        
        print("\n3. Testing data loading...")
        # This will use the cached data loader
        from data_loader import load_and_process_data
        from business_metrics import BusinessMetricsCalculator
        
        loader, processed_data = load_and_process_data('ecommerce_data/')
        if processed_data is None:
            print("❌ Data loading failed")
            return False
        
        sales_data = loader.create_sales_dataset(
            year_filter=[2023, 2022],
            status_filter='delivered'
        )
        
        if sales_data.empty:
            print("❌ Sales data empty")
            return False
        
        print("✅ Data loading successful")
        
        print("\n4. Testing chart functions...")
        
        # Test chart creation with actual data
        products_df = loader.get_product_categories()
        customers_df = loader.get_customer_geography()
        reviews_df = loader.get_review_scores()
        
        metrics_calculator = BusinessMetricsCalculator(sales_data)
        comprehensive_report = metrics_calculator.generate_comprehensive_report(
            current_year=2023,
            previous_year=2022,
            products_df=products_df,
            customers_df=customers_df,
            reviews_df=reviews_df
        )
        
        # Test each chart function
        revenue_chart = create_revenue_trend_chart(sales_data, 2023, 2022)
        print("✅ Revenue trend chart created")
        
        product_metrics = comprehensive_report['product_metrics']
        category_chart = create_category_chart(product_metrics)
        print("✅ Category chart created")
        
        geographic_metrics = comprehensive_report['geographic_metrics']
        map_chart = create_choropleth_map(geographic_metrics)
        print("✅ Choropleth map created")
        
        experience_metrics = comprehensive_report['customer_experience_metrics']
        satisfaction_chart = create_satisfaction_delivery_chart(experience_metrics)
        print("✅ Satisfaction chart created")
        
        print(f"\n=== DASHBOARD VERIFICATION COMPLETE ===")
        print("✅ Dashboard is ready to run!")
        print("🚀 Start with: streamlit run dashboard.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    verify_dashboard()