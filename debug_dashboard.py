#!/usr/bin/env python3
"""
Debug script to identify issues with dashboard data boxes.
This script mimics the dashboard data processing to find where data might be missing.
"""

def debug_dashboard_data():
    print("=== DEBUGGING DASHBOARD DATA FLOW ===\n")
    
    try:
        from data_loader import EcommerceDataLoader, load_and_process_data
        from business_metrics import BusinessMetricsCalculator
        
        # 1. Test data loading
        print("1. Testing data loading...")
        loader, processed_data = load_and_process_data('ecommerce_data/')
        
        if processed_data is None:
            print("❌ Failed to load processed_data")
            return
            
        # Check available years
        available_years = sorted(processed_data['orders']['order_year'].dropna().unique())
        print(f"✅ Available years: {available_years}")
        
        # 2. Test sales data creation for current year
        current_year = 2023
        previous_year = 2022
        
        print(f"\n2. Testing sales data creation for {current_year}...")
        years_to_include = [current_year, previous_year]
        sales_data = loader.create_sales_dataset(
            year_filter=years_to_include,
            status_filter='delivered'
        )
        
        if sales_data.empty:
            print(f"❌ No sales data for {current_year}")
            return
            
        print(f"✅ Sales data loaded: {len(sales_data)} records")
        print(f"   Date range: {sales_data['order_purchase_timestamp'].min()} to {sales_data['order_purchase_timestamp'].max()}")
        
        # 3. Test supporting datasets
        print(f"\n3. Testing supporting datasets...")
        products_df = loader.get_product_categories()
        customers_df = loader.get_customer_geography()
        reviews_df = loader.get_review_scores()
        
        print(f"   Products: {len(products_df)} records")
        print(f"   Customers: {len(customers_df)} records")
        print(f"   Reviews: {len(reviews_df)} records")
        
        # 4. Test metrics calculation
        print(f"\n4. Testing metrics calculation...")
        metrics_calculator = BusinessMetricsCalculator(sales_data)
        
        # Test revenue metrics
        revenue_metrics = metrics_calculator.calculate_revenue_metrics(current_year, previous_year)
        print(f"✅ Revenue metrics:")
        print(f"   Total Revenue: ${revenue_metrics['total_revenue']:,.2f}")
        print(f"   Total Orders: {revenue_metrics['total_orders']:,}")
        print(f"   AOV: ${revenue_metrics['average_order_value']:.2f}")
        if 'revenue_growth_rate' in revenue_metrics:
            print(f"   Revenue Growth: {revenue_metrics['revenue_growth_rate']:.2f}%")
        
        # 5. Test comprehensive report generation
        print(f"\n5. Testing comprehensive report...")
        try:
            comprehensive_report = metrics_calculator.generate_comprehensive_report(
                current_year=current_year,
                previous_year=previous_year,
                products_df=products_df,
                customers_df=customers_df,
                reviews_df=reviews_df
            )
            
            print("✅ Comprehensive report sections:")
            for key in comprehensive_report.keys():
                if key != 'data_summary':
                    print(f"   - {key}: {'✅ Available' if comprehensive_report[key] else '❌ Empty'}")
            
            # 6. Test specific metrics that might be causing blank boxes
            print(f"\n6. Testing specific dashboard metrics...")
            
            # Test product metrics
            if 'product_metrics' in comprehensive_report and comprehensive_report['product_metrics']:
                product_metrics = comprehensive_report['product_metrics']
                print(f"   Product categories: {product_metrics['total_categories']}")
                print(f"   Top category: {product_metrics['category_performance'].index[0] if not product_metrics['category_performance'].empty else 'None'}")
            else:
                print("   ❌ Product metrics missing or empty")
            
            # Test geographic metrics  
            if 'geographic_metrics' in comprehensive_report and comprehensive_report['geographic_metrics']:
                geo_metrics = comprehensive_report['geographic_metrics']
                print(f"   States: {geo_metrics['total_states']}")
                print(f"   Top state: {geo_metrics['state_performance'].index[0] if not geo_metrics['state_performance'].empty else 'None'}")
            else:
                print("   ❌ Geographic metrics missing or empty")
            
            # Test customer experience metrics
            if 'customer_experience_metrics' in comprehensive_report and comprehensive_report['customer_experience_metrics']:
                exp_metrics = comprehensive_report['customer_experience_metrics']
                print(f"   Total reviews: {exp_metrics['total_reviews']}")
                print(f"   Avg rating: {exp_metrics['satisfaction']['average_review_score']:.2f}")
                print(f"   Avg delivery: {exp_metrics['delivery']['average_delivery_days']:.1f} days")
            else:
                print("   ❌ Customer experience metrics missing or empty")
                
        except Exception as e:
            print(f"❌ Error generating comprehensive report: {e}")
            import traceback
            traceback.print_exc()
            
        print(f"\n=== DEBUG COMPLETE ===")
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_dashboard_data()