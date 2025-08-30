# E-commerce Data Analysis

A comprehensive data analysis project for e-commerce sales data, providing insights into revenue trends, product performance, geographic distribution, and customer satisfaction metrics using Python and Jupyter notebooks.

## Overview

This project analyzes e-commerce transaction data to provide business insights through exploratory data analysis. The analysis covers:

- **Revenue Analysis**: Year-over-year growth, monthly trends, and average order values
- **Product Performance**: Sales by category and product distribution
- **Geographic Analysis**: Revenue distribution across US states with interactive maps  
- **Customer Experience**: Delivery performance and review score analysis

## Project Structure

```
ecommerce-data-analysis/
├── EDA.ipynb               # Main analysis notebook
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── prompt.md              # Project prompt and requirements
└── ecommerce_data/        # Data directory
    ├── orders_dataset.csv          # Order transactions and status
    ├── order_items_dataset.csv     # Individual items per order
    ├── products_dataset.csv        # Product catalog and categories  
    ├── customers_dataset.csv       # Customer geographic data
    ├── order_reviews_dataset.csv   # Customer reviews and ratings
    └── order_payments_dataset.csv  # Payment information
```

## Key Findings

### Revenue Performance (2022-2023)
- **Total Revenue 2023**: $3.36M (down 2.5% from 2022)
- **Average Order Value**: $724.98 
- **Monthly Growth Trend**: -0.39% average monthly decline in 2023
- **Total Orders**: 4,635 delivered orders in 2023

### Product Categories
- **Top Performing Categories**: Analysis shows revenue distribution across 13 product categories
- **Product Catalog**: 6,000 unique products analyzed
- **Category Diversity**: Balanced distribution across electronics, home goods, books, etc.

### Geographic Distribution  
- **Market Coverage**: Sales across all US states
- **Interactive Mapping**: Choropleth visualization of revenue by state
- **Regional Performance**: State-level revenue and order analysis

### Customer Experience
- **Average Review Score**: 4.10/5.0 (2023)  
- **Delivery Performance**: Average 8 days delivery time
- **Satisfaction Rate**: Majority of customers rate 4-5 stars
- **Delivery Impact**: Faster delivery (1-3 days) correlates with higher review scores (4.19 vs 4.11)

## Installation and Usage

### Prerequisites
- Python 3.8 or higher
- Jupyter Notebook or JupyterLab

### Setup Steps

1. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Choose your analysis approach**:

   **Option A: Refactored Analysis (Recommended)**
   ```bash
   jupyter notebook EDA_Refactored.ipynb
   ```

   **Option B: Original Analysis**
   ```bash
   jupyter notebook EDA.ipynb
   ```

3. **Configure your analysis** (EDA_Refactored.ipynb only):
   - Set `ANALYSIS_YEAR` and `COMPARISON_YEAR` in the configuration cell
   - Optionally filter by specific month or change order status
   - Run all cells to generate comprehensive analysis

## Refactored Analysis Features

### New Modular Structure
- **data_loader.py**: Handles data loading, processing, and filtering
- **business_metrics.py**: Calculates business metrics and creates visualizations  
- **EDA_Refactored.ipynb**: Main analysis notebook with improved structure

### Key Improvements
- **Configurable Analysis**: Easily change analysis parameters without code modification
- **Professional Documentation**: Clear sections with business context and data dictionary
- **Reusable Functions**: Modular code that can be applied to different datasets
- **Enhanced Visualizations**: Business-ready charts with proper formatting
- **No Pandas Warnings**: All DataFrame operations use proper assignment methods
- **Strategic Insights**: Automated generation of business recommendations

## Analysis Components

### Data Sources
The analysis processes six interconnected datasets:
- **Orders**: Transaction records with timestamps and status
- **Order Items**: Individual products within each order with pricing
- **Products**: Product catalog with categories and specifications
- **Customers**: Customer location data (city, state, zip code)
- **Reviews**: Customer feedback and ratings (1-5 scale)
- **Payments**: Payment method and transaction details

### Analysis Workflow (Refactored)
1. **Configuration**: Set analysis parameters (year, month, order status)
2. **Data Processing**: Automated loading and processing with data quality checks
3. **Business Metrics**: Calculate comprehensive KPIs using reusable functions
4. **Visualizations**: Generate professional charts with consistent formatting
5. **Strategic Insights**: Automated recommendations based on data patterns

### Original Analysis Workflow
1. **Data Loading**: Load and examine all CSV datasets
2. **Data Merging**: Join tables to create comprehensive sales dataset  
3. **Revenue Analysis**: Calculate 2022 vs 2023 performance metrics
4. **Product Analysis**: Analyze category performance and distribution
5. **Geographic Analysis**: Map sales across US states with choropleth visualization
6. **Customer Experience**: Correlate delivery times with review scores

## Technical Details

### Dependencies
```
pandas>=1.5.0     # Data manipulation and analysis
numpy>=1.21.0     # Numerical computing
matplotlib>=3.5.0 # Static visualizations
seaborn>=0.11.0   # Statistical visualization
plotly>=5.0.0     # Interactive visualizations
streamlit>=1.28.0 # Web app framework
jupyter>=1.0.0    # Notebook environment
ipykernel>=6.0.0 # Jupyter kernel
```

### Data Schema
- **orders_dataset.csv**: 16,047 orders from 2022-2023
- **order_items_dataset.csv**: 16,047 line items with pricing
- **products_dataset.csv**: 6,000 products across 13 categories
- **customers_dataset.csv**: Customer geographic information
- **order_reviews_dataset.csv**: Customer ratings and feedback
- **order_payments_dataset.csv**: Payment transaction details

### Visualizations Generated
1. **Revenue Trends**: Monthly revenue comparison between 2022 and 2023
2. **Product Categories**: Horizontal bar chart of top-performing categories
3. **Geographic Distribution**: Interactive US choropleth map using Plotly
4. **Review Scores**: Distribution of customer satisfaction ratings
5. **Delivery Analysis**: Correlation between delivery speed and satisfaction

### Code Quality Notes
✅ **Refactored Version (EDA_Refactored.ipynb):**
- No pandas warnings - all DataFrame operations use proper methods
- Modular structure with separate .py files for reusable functions
- Configurable parameters for flexible analysis
- Professional documentation and visualizations

⚠️ **Original Version (EDA.ipynb) Known Issues:**
- Multiple `SettingWithCopyWarning` in notebook cells (lines involving DataFrame slices)
- Consider using `.loc[]` for DataFrame assignments to avoid warnings
- All analysis contained in single notebook - could benefit from modular structure

## Business Insights

### Revenue Trends
- Revenue declined 2.5% from 2022 to 2023 despite stable order volumes
- Monthly growth rate averaged -0.39% throughout 2023
- Average order value remained stable at ~$725

### Product Performance
- 13 distinct product categories analyzed
- Category performance varies significantly (visualized in horizontal bar chart)
- Product catalog contains 6,000 unique items

### Geographic Patterns  
- Sales distributed across all US states
- State-level performance visualized with interactive choropleth mapping
- Geographic analysis reveals regional sales concentration patterns

### Customer Satisfaction
- Overall satisfaction high at 4.10/5.0 average
- 50% of customers give 5-star reviews
- Faster delivery (1-3 days) correlates with higher satisfaction scores
- Average delivery time of 8 days suggests optimization opportunity

## Future Enhancements

### Potential Improvements
1. **Code Quality**: Fix pandas warnings by using proper DataFrame assignment methods
2. **Modularization**: Extract reusable functions into separate Python modules
3. **Data Validation**: Add explicit data quality checks and missing value handling
4. **Time Series**: Implement more sophisticated time series analysis and forecasting
5. **Customer Segmentation**: Develop customer cohort and segmentation analysis
6. **Interactive Dashboard**: Create Streamlit or Dash web interface for dynamic exploration

### Extension Opportunities  
- Real-time data pipeline integration
- Machine learning models for demand forecasting
- A/B testing analysis framework
- Advanced statistical analysis (correlation, regression)
- Integration with business intelligence tools

## Contributing

To extend or improve this analysis:
1. Fork the repository and create a feature branch
2. Follow existing code style and add appropriate documentation  
3. Test changes thoroughly with the provided datasets
4. Submit pull request with clear description of changes

## License

This project is provided for educational and analytical purposes. Data appears to be synthetic/sample data suitable for learning and demonstration.