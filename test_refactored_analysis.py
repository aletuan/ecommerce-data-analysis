"""
Test Script for EDA_Refactored.ipynb Verification

This script tests all the key components that would be executed in the refactored notebook
to verify that the analysis works correctly with the existing data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_loader import EcommerceDataLoader, load_and_process_data, get_data_summary
from business_metrics import BusinessMetricsCalculator, MetricsVisualizer

def test_refactored_analysis():
    """Test the complete refactored analysis workflow"""
    
    # Analysis Configuration (matches notebook)
    ANALYSIS_YEAR = 2023
    COMPARISON_YEAR = 2022
    ANALYSIS_MONTH = None
    ORDER_STATUS = 'delivered'
    DATA_PATH = 'ecommerce_data/'
    COLOR_PALETTE = 'viridis'
    
    print("=" * 60)
    print("REFACTORED E-COMMERCE ANALYSIS TEST")
    print("=" * 60)
    
    # Step 1: Load and process data
    print("\n1. Loading and processing data...")
    loader, processed_data = load_and_process_data(DATA_PATH)
    get_data_summary(processed_data)
    
    # Step 2: Create analysis dataset
    print("\n2. Creating analysis dataset...")
    sales_data = loader.create_sales_dataset(
        year_filter=[ANALYSIS_YEAR, COMPARISON_YEAR] if COMPARISON_YEAR else [ANALYSIS_YEAR],
        month_filter=ANALYSIS_MONTH,
        status_filter=ORDER_STATUS
    )
    
    products_df = loader.get_product_categories()
    customers_df = loader.get_customer_geography()
    reviews_df = loader.get_review_scores()
    
    print(f"Analysis dataset: {len(sales_data):,} records")
    print(f"Date range: {sales_data['order_purchase_timestamp'].min().date()} to {sales_data['order_purchase_timestamp'].max().date()}")
    
    # Step 3: Calculate business metrics
    print("\n3. Calculating business metrics...")
    metrics_calculator = BusinessMetricsCalculator(sales_data)
    
    # Revenue metrics
    revenue_metrics = metrics_calculator.calculate_revenue_metrics(ANALYSIS_YEAR, COMPARISON_YEAR)
    
    # Comprehensive report
    comprehensive_report = metrics_calculator.generate_comprehensive_report(
        current_year=ANALYSIS_YEAR,
        previous_year=COMPARISON_YEAR,
        products_df=products_df,
        customers_df=customers_df,
        reviews_df=reviews_df
    )
    
    # Step 4: Display summary
    print("\n4. Business Summary:")
    metrics_calculator.print_summary_report(comprehensive_report)
    
    # Step 5: Test visualization initialization
    print("\n5. Testing visualization components...")
    visualizer = MetricsVisualizer(comprehensive_report, COLOR_PALETTE)
    print("✅ Visualizations initialized (plots not generated in test mode)")
    
    # Step 6: Results validation
    print("\n6. Validating key results...")
    expected_results = {
        'total_revenue_2023': 3360294.74,
        'total_orders_2023': 4635,
        'revenue_growth_rate': -2.5,
        'total_categories': 13
    }
    
    actual_results = {
        'total_revenue_2023': revenue_metrics['total_revenue'],
        'total_orders_2023': revenue_metrics['total_orders'],
        'revenue_growth_rate': round(revenue_metrics['revenue_growth_rate'], 1),
        'total_categories': comprehensive_report['product_metrics']['total_categories']
    }
    
    print("\nResults Validation:")
    all_passed = True
    for metric, expected in expected_results.items():
        actual = actual_results[metric]
        passed = abs(actual - expected) < 0.01 if isinstance(expected, float) else actual == expected
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {metric}: Expected {expected}, Got {actual} - {status}")
        if not passed:
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    try:
        success = test_refactored_analysis()
        print("\n" + "=" * 60)
        if success:
            print("🎉 ALL TESTS PASSED! EDA_Refactored.ipynb is ready to use.")
        else:
            print("❌ Some tests failed. Please check the implementation.")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()