"""
E-commerce Business Intelligence Dashboard

A professional Streamlit dashboard for e-commerce data analysis with interactive
filtering and comprehensive business metrics visualization.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings

# Import custom modules
from data_loader import EcommerceDataLoader, load_and_process_data
from business_metrics import BusinessMetricsCalculator

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="E-commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f2937;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        margin-bottom: 0.5rem;
    }
    
    .trend-positive {
        color: #10b981;
        font-size: 0.875rem;
    }
    
    .trend-negative {
        color: #ef4444;
        font-size: 0.875rem;
    }
    
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .bottom-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
    }
    
    .stars {
        color: #fbbf24;
        font-size: 1.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the e-commerce data"""
    try:
        loader, processed_data = load_and_process_data('ecommerce_data/')
        return loader, processed_data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

def format_number(num, prefix="$"):
    """Format numbers for display (e.g., $300K, $2M)"""
    if num >= 1_000_000:
        return f"{prefix}{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{prefix}{num/1_000:.0f}K"
    else:
        return f"{prefix}{num:.0f}"

def format_percentage(num):
    """Format percentage with proper sign and color"""
    if num >= 0:
        return f"↑ +{num:.2f}%", "trend-positive"
    else:
        return f"↓ {num:.2f}%", "trend-negative"

def create_revenue_trend_chart(sales_data, current_year, previous_year):
    """Create revenue trend line chart with current and previous year comparison"""
    
    # Current year data
    current_data = sales_data[sales_data['order_year'] == current_year]
    current_monthly = current_data.groupby('order_month')['price'].sum().reset_index()
    current_monthly['formatted_revenue'] = current_monthly['price'].apply(lambda x: format_number(x))
    
    # Previous year data
    previous_data = sales_data[sales_data['order_year'] == previous_year]
    previous_monthly = previous_data.groupby('order_month')['price'].sum().reset_index()
    previous_monthly['formatted_revenue'] = previous_monthly['price'].apply(lambda x: format_number(x))
    
    fig = go.Figure()
    
    # Current year line (solid)
    fig.add_trace(go.Scatter(
        x=current_monthly['order_month'],
        y=current_monthly['price'],
        mode='lines+markers',
        name=f'{current_year}',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=6),
        customdata=current_monthly['formatted_revenue'],
        hovertemplate='Month: %{x}<br>Revenue: %{customdata}<extra></extra>'
    ))
    
    # Previous year line (dashed)
    fig.add_trace(go.Scatter(
        x=previous_monthly['order_month'],
        y=previous_monthly['price'],
        mode='lines+markers',
        name=f'{previous_year}',
        line=dict(color='#94a3b8', width=2, dash='dash'),
        marker=dict(size=4),
        customdata=previous_monthly['formatted_revenue'],
        hovertemplate='Month: %{x}<br>Revenue: %{customdata}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Monthly Revenue Trend',
        xaxis_title='Month',
        yaxis_title='Revenue',
        showlegend=True,
        height=400,
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(
            showgrid=True, 
            gridwidth=1, 
            gridcolor='rgba(0,0,0,0.1)',
            tickformat='$.0s'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_category_chart(product_metrics):
    """Create top 10 categories bar chart with blue gradient"""
    
    top_10 = product_metrics['category_performance'].head(10)
    
    # Create blue gradient colors (darker for higher values)
    colors = px.colors.sequential.Blues_r[:len(top_10)]
    
    fig = go.Figure(data=[
        go.Bar(
            y=top_10.index,
            x=top_10['total_revenue'],
            orientation='h',
            marker=dict(color=colors),
            customdata=[format_number(x) for x in top_10['total_revenue']],
            hovertemplate='Category: %{y}<br>Revenue: %{customdata}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Top 10 Product Categories',
        xaxis_title='Revenue',
        yaxis_title='Category',
        height=400,
        xaxis=dict(tickformat='$.0s'),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_choropleth_map(geographic_metrics):
    """Create US choropleth map for revenue by state"""
    
    state_data = geographic_metrics['state_performance'].reset_index()
    
    fig = px.choropleth(
        state_data,
        locations='customer_state',
        color='total_revenue',
        locationmode='USA-states',
        scope='usa',
        title='Revenue by State',
        color_continuous_scale='Blues',
        hover_data={
            'total_revenue': ':$,.0f',
            'total_orders': ':,',
            'avg_order_value': ':$,.0f'
        }
    )
    
    fig.update_layout(
        height=400,
        geo=dict(showframe=False, showcoastlines=True),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_satisfaction_delivery_chart(experience_metrics):
    """Create satisfaction vs delivery time bar chart"""
    
    delivery_satisfaction = experience_metrics['delivery_satisfaction_correlation']
    
    # Order the categories properly
    categories = ['1-3 days', '4-7 days', '8+ days']
    values = [delivery_satisfaction.get(cat, 0) for cat in categories]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker=dict(color='#3b82f6'),
            hovertemplate='Delivery Time: %{x}<br>Avg Rating: %{y:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Customer Satisfaction vs Delivery Time',
        xaxis_title='Delivery Time',
        yaxis_title='Average Review Score',
        height=400,
        yaxis=dict(range=[0, 5]),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def main():
    """Main dashboard application"""
    
    # Load data
    loader, processed_data = load_data()
    
    if loader is None or processed_data is None:
        st.error("Failed to load data. Please check your data files.")
        return
    
    # Debug info (can be removed in production)
    with st.expander("Debug Info", expanded=False):
        st.write(f"Datasets loaded: {list(processed_data.keys())}")
        st.write(f"Orders shape: {processed_data['orders'].shape}")
        st.write(f"Available years: {sorted(processed_data['orders']['order_year'].dropna().unique())}")
    
    # Header with title and date filter
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown('<div class="main-header">E-commerce Analytics Dashboard</div>', 
                   unsafe_allow_html=True)
    
    with col2:
        # Get available years from data
        available_years = sorted(processed_data['orders']['order_year'].dropna().unique())
        current_year = st.selectbox(
            "Select Year",
            available_years,
            index=len(available_years)-1 if available_years else 0,
            key="year_filter"
        )
    
    # Determine previous year for comparison
    previous_year = current_year - 1 if current_year - 1 in available_years else None
    
    # Create filtered sales dataset
    years_to_include = [current_year, previous_year] if previous_year else [current_year]
    sales_data = loader.create_sales_dataset(
        year_filter=years_to_include,
        status_filter='delivered'
    )
    
    if sales_data.empty:
        st.warning(f"No data available for {current_year}")
        return
    
    # Get supporting datasets
    try:
        products_df = loader.get_product_categories()
        customers_df = loader.get_customer_geography()
        reviews_df = loader.get_review_scores()
        
        # Calculate metrics
        metrics_calculator = BusinessMetricsCalculator(sales_data)
        
        # Generate comprehensive report
        comprehensive_report = metrics_calculator.generate_comprehensive_report(
            current_year=current_year,
            previous_year=previous_year,
            products_df=products_df,
            customers_df=customers_df,
            reviews_df=reviews_df
        )
        
    except Exception as e:
        st.error(f"Error generating metrics: {e}")
        st.stop()
    
    # Extract metrics for easier access
    revenue_metrics = comprehensive_report['revenue_metrics']
    product_metrics = comprehensive_report.get('product_metrics', {})
    geographic_metrics = comprehensive_report.get('geographic_metrics', {})
    experience_metrics = comprehensive_report.get('customer_experience_metrics', {})
    
    # KPI Cards Row
    st.markdown("### Key Performance Indicators")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        try:
            total_revenue = revenue_metrics.get('total_revenue', 0)
            revenue_growth = revenue_metrics.get('revenue_growth_rate', 0)
            trend_text, trend_class = format_percentage(revenue_growth)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Revenue</div>
                <div class="metric-value">{format_number(total_revenue)}</div>
                <div class="{trend_class}">{trend_text}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error displaying revenue KPI: {e}")
    
    with kpi2:
        try:
            monthly_growth = revenue_metrics.get('monthly_growth_trend', 0)
            trend_text, trend_class = format_percentage(monthly_growth)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Monthly Growth</div>
                <div class="metric-value">{monthly_growth:+.2f}%</div>
                <div class="{trend_class}">{trend_text}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error displaying monthly growth KPI: {e}")
    
    with kpi3:
        try:
            aov = revenue_metrics.get('average_order_value', 0)
            aov_growth = revenue_metrics.get('aov_growth_rate', 0)
            trend_text, trend_class = format_percentage(aov_growth)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Average Order Value</div>
                <div class="metric-value">{format_number(aov)}</div>
                <div class="{trend_class}">{trend_text}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error displaying AOV KPI: {e}")
    
    with kpi4:
        try:
            total_orders = revenue_metrics.get('total_orders', 0)
            order_growth = revenue_metrics.get('order_growth_rate', 0)
            trend_text, trend_class = format_percentage(order_growth)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Orders</div>
                <div class="metric-value">{total_orders:,}</div>
                <div class="{trend_class}">{trend_text}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error displaying orders KPI: {e}")
    
    # Charts Grid (2x2)
    st.markdown("### Business Analytics")
    
    chart_row1_col1, chart_row1_col2 = st.columns(2)
    
    with chart_row1_col1:
        try:
            if previous_year:
                revenue_chart = create_revenue_trend_chart(sales_data, current_year, previous_year)
                st.plotly_chart(revenue_chart, use_container_width=True)
            else:
                st.info("Previous year data not available for trend comparison")
        except Exception as e:
            st.error(f"Error creating revenue chart: {e}")
    
    with chart_row1_col2:
        try:
            if product_metrics and 'category_performance' in product_metrics:
                category_chart = create_category_chart(product_metrics)
                st.plotly_chart(category_chart, use_container_width=True)
            else:
                st.info("Product metrics not available")
        except Exception as e:
            st.error(f"Error creating category chart: {e}")
    
    chart_row2_col1, chart_row2_col2 = st.columns(2)
    
    with chart_row2_col1:
        try:
            if geographic_metrics and 'state_performance' in geographic_metrics:
                map_chart = create_choropleth_map(geographic_metrics)
                st.plotly_chart(map_chart, use_container_width=True)
            else:
                st.info("Geographic metrics not available")
        except Exception as e:
            st.error(f"Error creating geographic map: {e}")
    
    with chart_row2_col2:
        try:
            if experience_metrics and 'delivery_satisfaction_correlation' in experience_metrics:
                satisfaction_chart = create_satisfaction_delivery_chart(experience_metrics)
                st.plotly_chart(satisfaction_chart, use_container_width=True)
            else:
                st.info("Customer experience metrics not available")
        except Exception as e:
            st.error(f"Error creating satisfaction chart: {e}")
    
    # Bottom Row - Delivery and Review Cards
    st.markdown("### Customer Experience")
    bottom_col1, bottom_col2 = st.columns(2)
    
    with bottom_col1:
        try:
            if experience_metrics and 'delivery' in experience_metrics:
                avg_delivery = experience_metrics['delivery']['average_delivery_days']
                # Calculate delivery trend (mock calculation since we don't have historical delivery data)
                delivery_trend = 0.0  # Would be calculated from historical data
                trend_text, trend_class = format_percentage(delivery_trend)
                
                st.markdown(f"""
                <div class="bottom-card">
                    <div class="metric-label">Average Delivery Time</div>
                    <div class="metric-value">{avg_delivery:.1f} days</div>
                    <div class="{trend_class}">{trend_text}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Delivery metrics not available")
        except Exception as e:
            st.error(f"Error displaying delivery metrics: {e}")
    
    with bottom_col2:
        try:
            if experience_metrics and 'satisfaction' in experience_metrics:
                avg_rating = experience_metrics['satisfaction']['average_review_score']
                stars = "★" * int(round(avg_rating)) + "☆" * (5 - int(round(avg_rating)))
                
                st.markdown(f"""
                <div class="bottom-card">
                    <div class="metric-value">{avg_rating:.2f}/5.0</div>
                    <div class="stars">{stars}</div>
                    <div class="metric-label">Average Review Score</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Review metrics not available")
        except Exception as e:
            st.error(f"Error displaying review metrics: {e}")
    
    # Footer with data info
    st.markdown("---")
    st.markdown(f"**Data Range:** {sales_data['order_purchase_timestamp'].min().strftime('%B %Y')} - "
               f"{sales_data['order_purchase_timestamp'].max().strftime('%B %Y')} | "
               f"**Total Records:** {len(sales_data):,} | "
               f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if __name__ == "__main__":
    main()