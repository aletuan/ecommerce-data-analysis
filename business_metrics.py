"""
Business Metrics Calculation Module for E-commerce Analysis

This module provides functions for calculating key business metrics including
revenue analysis, product performance, geographic insights, and customer satisfaction.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional, Union
from datetime import datetime


class BusinessMetricsCalculator:
    """
    A class for calculating comprehensive business metrics from e-commerce data.
    
    This class provides methods for revenue analysis, product performance,
    geographic distribution, and customer satisfaction metrics.
    """
    
    def __init__(self, sales_data: pd.DataFrame):
        """
        Initialize the metrics calculator with sales data.
        
        Args:
            sales_data (pd.DataFrame): Processed sales dataset from data_loader
        """
        self.sales_data = sales_data.copy()
        self.metrics_cache = {}
        
    def calculate_revenue_metrics(self, current_year: int, previous_year: Optional[int] = None) -> Dict:
        """
        Calculate comprehensive revenue metrics.
        
        Args:
            current_year (int): Year to analyze
            previous_year (Optional[int]): Previous year for comparison
            
        Returns:
            Dict: Revenue metrics including total revenue, growth, AOV, etc.
        """
        current_data = self.sales_data[self.sales_data['order_year'] == current_year]
        
        metrics = {
            'current_year': current_year,
            'total_revenue': current_data['price'].sum(),
            'total_orders': current_data['order_id'].nunique(),
            'total_items': len(current_data),
            'average_order_value': current_data.groupby('order_id')['price'].sum().mean(),
            'average_item_price': current_data['price'].mean(),
            'monthly_revenue': current_data.groupby('order_month')['price'].sum().to_dict()
        }
        
        # Add growth metrics if previous year provided
        if previous_year:
            previous_data = self.sales_data[self.sales_data['order_year'] == previous_year]
            if not previous_data.empty:
                prev_revenue = previous_data['price'].sum()
                prev_orders = previous_data['order_id'].nunique()
                prev_aov = previous_data.groupby('order_id')['price'].sum().mean()
                
                metrics.update({
                    'previous_year': previous_year,
                    'previous_revenue': prev_revenue,
                    'previous_orders': prev_orders,
                    'previous_aov': prev_aov,
                    'revenue_growth_rate': ((metrics['total_revenue'] - prev_revenue) / prev_revenue) * 100,
                    'order_growth_rate': ((metrics['total_orders'] - prev_orders) / prev_orders) * 100,
                    'aov_growth_rate': ((metrics['average_order_value'] - prev_aov) / prev_aov) * 100
                })
        
        # Calculate monthly growth trend
        monthly_revenue_series = pd.Series(metrics['monthly_revenue']).sort_index()
        monthly_growth = monthly_revenue_series.pct_change().mean() * 100
        metrics['monthly_growth_trend'] = monthly_growth
        
        self.metrics_cache['revenue'] = metrics
        return metrics
    
    def calculate_product_metrics(self, products_df: pd.DataFrame) -> Dict:
        """
        Calculate product performance metrics.
        
        Args:
            products_df (pd.DataFrame): Products dataset with category information
            
        Returns:
            Dict: Product performance metrics by category
        """
        # Merge sales data with product categories
        sales_with_categories = pd.merge(
            self.sales_data,
            products_df,
            on='product_id',
            how='left'
        )
        
        # Calculate category metrics
        category_metrics = sales_with_categories.groupby('product_category_name').agg({
            'price': ['sum', 'mean', 'count'],
            'order_id': 'nunique',
            'product_id': 'nunique'
        }).round(2)
        
        category_metrics.columns = ['total_revenue', 'avg_item_price', 'total_items', 'total_orders', 'unique_products']
        category_metrics = category_metrics.sort_values('total_revenue', ascending=False)
        
        # Calculate market share
        total_revenue = category_metrics['total_revenue'].sum()
        category_metrics['revenue_share_pct'] = (category_metrics['total_revenue'] / total_revenue * 100).round(2)
        
        metrics = {
            'category_performance': category_metrics,
            'top_categories': category_metrics.head(10),
            'total_categories': len(category_metrics),
            'revenue_concentration': category_metrics['revenue_share_pct'].head(5).sum()
        }
        
        self.metrics_cache['products'] = metrics
        return metrics
    
    def calculate_geographic_metrics(self, customers_df: pd.DataFrame) -> Dict:
        """
        Calculate geographic performance metrics.
        
        Args:
            customers_df (pd.DataFrame): Customers dataset with location data
            
        Returns:
            Dict: Geographic performance metrics by state
        """
        # Merge sales data with customer geography
        sales_with_geography = pd.merge(
            self.sales_data[['order_id', 'customer_id', 'price']].drop_duplicates(),
            customers_df,
            on='customer_id',
            how='left'
        )
        
        # Calculate state-level metrics
        state_metrics = sales_with_geography.groupby('customer_state').agg({
            'price': 'sum',
            'order_id': 'nunique',
            'customer_id': 'nunique'
        }).round(2)
        
        state_metrics.columns = ['total_revenue', 'total_orders', 'unique_customers']
        state_metrics = state_metrics.sort_values('total_revenue', ascending=False)
        
        # Calculate additional metrics
        state_metrics['avg_order_value'] = (state_metrics['total_revenue'] / state_metrics['total_orders']).round(2)
        state_metrics['revenue_per_customer'] = (state_metrics['total_revenue'] / state_metrics['unique_customers']).round(2)
        
        total_revenue = state_metrics['total_revenue'].sum()
        state_metrics['revenue_share_pct'] = (state_metrics['total_revenue'] / total_revenue * 100).round(2)
        
        metrics = {
            'state_performance': state_metrics,
            'top_states': state_metrics.head(10),
            'total_states': len(state_metrics),
            'geographic_concentration': state_metrics['revenue_share_pct'].head(10).sum()
        }
        
        self.metrics_cache['geography'] = metrics
        return metrics
    
    def calculate_customer_satisfaction_metrics(self, reviews_df: pd.DataFrame) -> Dict:
        """
        Calculate customer satisfaction and delivery metrics.
        
        Args:
            reviews_df (pd.DataFrame): Reviews dataset with scores
            
        Returns:
            Dict: Customer satisfaction and delivery performance metrics
        """
        # Merge sales data with reviews
        sales_with_reviews = pd.merge(
            self.sales_data,
            reviews_df,
            on='order_id',
            how='left'
        )
        
        # Remove duplicates for order-level analysis
        order_level_data = sales_with_reviews[['order_id', 'delivery_days', 'review_score']].drop_duplicates()
        
        # Calculate satisfaction metrics
        satisfaction_metrics = {
            'average_review_score': order_level_data['review_score'].mean(),
            'review_score_distribution': order_level_data['review_score'].value_counts(normalize=True).sort_index(),
            'high_satisfaction_rate': (order_level_data['review_score'] >= 4).mean() * 100,
            'low_satisfaction_rate': (order_level_data['review_score'] <= 2).mean() * 100
        }
        
        # Calculate delivery metrics
        delivery_metrics = {
            'average_delivery_days': order_level_data['delivery_days'].mean(),
            'median_delivery_days': order_level_data['delivery_days'].median(),
            'fast_delivery_rate': (order_level_data['delivery_days'] <= 3).mean() * 100,
            'slow_delivery_rate': (order_level_data['delivery_days'] > 10).mean() * 100
        }
        
        # Analyze delivery speed vs satisfaction
        def categorize_delivery_speed(days):
            if pd.isna(days):
                return 'Unknown'
            elif days <= 3:
                return '1-3 days'
            elif days <= 7:
                return '4-7 days'
            else:
                return '8+ days'
        
        order_level_data['delivery_category'] = order_level_data['delivery_days'].apply(categorize_delivery_speed)
        delivery_satisfaction = order_level_data.groupby('delivery_category')['review_score'].mean()
        
        metrics = {
            'satisfaction': satisfaction_metrics,
            'delivery': delivery_metrics,
            'delivery_satisfaction_correlation': delivery_satisfaction.to_dict(),
            'total_reviews': len(order_level_data.dropna(subset=['review_score']))
        }
        
        self.metrics_cache['customer_experience'] = metrics
        return metrics
    
    def generate_comprehensive_report(self, 
                                    current_year: int,
                                    previous_year: Optional[int] = None,
                                    products_df: Optional[pd.DataFrame] = None,
                                    customers_df: Optional[pd.DataFrame] = None,
                                    reviews_df: Optional[pd.DataFrame] = None) -> Dict:
        """
        Generate a comprehensive business metrics report.
        
        Args:
            current_year (int): Year to analyze
            previous_year (Optional[int]): Previous year for comparison
            products_df (Optional[pd.DataFrame]): Products dataset
            customers_df (Optional[pd.DataFrame]): Customers dataset
            reviews_df (Optional[pd.DataFrame]): Reviews dataset
            
        Returns:
            Dict: Comprehensive metrics report
        """
        report = {
            'analysis_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'data_summary': {
                'total_records': len(self.sales_data),
                'date_range': {
                    'start': self.sales_data['order_purchase_timestamp'].min(),
                    'end': self.sales_data['order_purchase_timestamp'].max()
                },
                'years_available': sorted(self.sales_data['order_year'].unique())
            }
        }
        
        # Calculate all metrics
        report['revenue_metrics'] = self.calculate_revenue_metrics(current_year, previous_year)
        
        if products_df is not None:
            report['product_metrics'] = self.calculate_product_metrics(products_df)
            
        if customers_df is not None:
            report['geographic_metrics'] = self.calculate_geographic_metrics(customers_df)
            
        if reviews_df is not None:
            report['customer_experience_metrics'] = self.calculate_customer_satisfaction_metrics(reviews_df)
        
        return report
    
    def print_summary_report(self, report: Dict) -> None:
        """
        Print a formatted summary of the business metrics report.
        
        Args:
            report (Dict): Comprehensive metrics report
        """
        print("=" * 60)
        print(f"BUSINESS METRICS SUMMARY - {report['revenue_metrics']['current_year']}")
        print("=" * 60)
        
        # Revenue Performance
        revenue = report['revenue_metrics']
        print(f"\nREVENUE PERFORMANCE:")
        print(f"  Total Revenue: ${revenue['total_revenue']:,.2f}")
        print(f"  Total Orders: {revenue['total_orders']:,}")
        print(f"  Average Order Value: ${revenue['average_order_value']:.2f}")
        
        if 'revenue_growth_rate' in revenue:
            growth_symbol = "+" if revenue['revenue_growth_rate'] >= 0 else ""
            print(f"  Revenue Growth: {growth_symbol}{revenue['revenue_growth_rate']:.1f}%")
        
        # Product Performance
        if 'product_metrics' in report:
            products = report['product_metrics']
            print(f"\nPRODUCT PERFORMANCE:")
            print(f"  Total Categories: {products['total_categories']}")
            print(f"  Top 5 Revenue Concentration: {products['revenue_concentration']:.1f}%")
            print(f"  Top Category: {products['top_categories'].index[0]}")
        
        # Customer Satisfaction
        if 'customer_experience_metrics' in report:
            experience = report['customer_experience_metrics']
            print(f"\nCUSTOMER SATISFACTION:")
            print(f"  Average Review Score: {experience['satisfaction']['average_review_score']:.2f}/5.0")
            print(f"  High Satisfaction (4+): {experience['satisfaction']['high_satisfaction_rate']:.1f}%")
            
            print(f"\nDELIVERY PERFORMANCE:")
            print(f"  Average Delivery Time: {experience['delivery']['average_delivery_days']:.1f} days")
            print(f"  Fast Delivery (≤3 days): {experience['delivery']['fast_delivery_rate']:.1f}%")


class MetricsVisualizer:
    """
    A class for creating business-oriented visualizations from metrics data.
    """
    
    def __init__(self, report: Dict, color_palette: str = 'viridis'):
        """
        Initialize the visualizer with metrics report.
        
        Args:
            report (Dict): Comprehensive metrics report
            color_palette (str): Color palette for visualizations
        """
        self.report = report
        self.color_palette = color_palette
        
        # Set professional style
        plt.style.use('default')
        sns.set_palette(color_palette)
        
    def plot_revenue_trend(self, figsize: Tuple[int, int] = (12, 6)) -> plt.Figure:
        """
        Create a revenue trend visualization.
        
        Args:
            figsize: Figure size tuple
            
        Returns:
            plt.Figure: Revenue trend plot
        """
        revenue_data = self.report['revenue_metrics']['monthly_revenue']
        
        fig, ax = plt.subplots(figsize=figsize)
        months = sorted(revenue_data.keys())
        revenues = [revenue_data[month] for month in months]
        
        ax.plot(months, revenues, marker='o', linewidth=2, markersize=6)
        ax.fill_between(months, revenues, alpha=0.3)
        
        ax.set_title(f"Monthly Revenue Trend - {self.report['revenue_metrics']['current_year']}", 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Revenue ($)", fontsize=12)
        ax.grid(True, alpha=0.3)
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        return fig
    
    def plot_category_performance(self, top_n: int = 10, figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
        """
        Create a product category performance visualization.
        
        Args:
            top_n: Number of top categories to show
            figsize: Figure size tuple
            
        Returns:
            plt.Figure: Category performance plot
        """
        if 'product_metrics' not in self.report:
            raise ValueError("Product metrics not available in report")
            
        category_data = self.report['product_metrics']['category_performance'].head(top_n)
        
        fig, ax = plt.subplots(figsize=figsize)
        
        bars = ax.barh(range(len(category_data)), category_data['total_revenue'])
        ax.set_yticks(range(len(category_data)))
        ax.set_yticklabels(category_data.index)
        
        ax.set_title(f"Top {top_n} Product Categories by Revenue - {self.report['revenue_metrics']['current_year']}", 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel("Revenue ($)", fontsize=12)
        ax.grid(True, alpha=0.3, axis='x')
        
        # Format x-axis as currency
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                   f'${width:,.0f}', ha='left', va='center', fontsize=10)
        
        plt.tight_layout()
        return fig
    
    def plot_geographic_distribution(self) -> go.Figure:
        """
        Create an interactive geographic distribution map.
        
        Returns:
            go.Figure: Plotly choropleth map
        """
        if 'geographic_metrics' not in self.report:
            raise ValueError("Geographic metrics not available in report")
            
        state_data = self.report['geographic_metrics']['state_performance'].reset_index()
        
        fig = px.choropleth(
            state_data,
            locations='customer_state',
            color='total_revenue',
            locationmode='USA-states',
            scope='usa',
            title=f'Revenue by State - {self.report["revenue_metrics"]["current_year"]}',
            color_continuous_scale='Reds',
            hover_data={'total_orders': True, 'avg_order_value': True}
        )
        
        fig.update_layout(
            title_font_size=16,
            title_x=0.5,
            geo=dict(showframe=False, showcoastlines=True)
        )
        
        return fig
    
    def plot_satisfaction_distribution(self, figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
        """
        Create a customer satisfaction distribution visualization.
        
        Args:
            figsize: Figure size tuple
            
        Returns:
            plt.Figure: Satisfaction distribution plot
        """
        if 'customer_experience_metrics' not in self.report:
            raise ValueError("Customer experience metrics not available in report")
            
        satisfaction_data = self.report['customer_experience_metrics']['satisfaction']['review_score_distribution']
        
        fig, ax = plt.subplots(figsize=figsize)
        
        bars = ax.bar(satisfaction_data.index, satisfaction_data.values * 100)
        
        ax.set_title(f"Customer Satisfaction Distribution - {self.report['revenue_metrics']['current_year']}", 
                    fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel("Review Score", fontsize=12)
        ax.set_ylabel("Percentage of Orders (%)", fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add percentage labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height,
                   f'{height:.1f}%', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        return fig