# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Installation
```bash
pip install -r requirements.txt
jupyter notebook EDA.ipynb
```

### Running Analysis
- Execute all cells in `EDA.ipynb` to reproduce the complete analysis
- Data loads automatically from `ecommerce_data/` directory
- No build or test commands - this is an exploratory data analysis project

## Architecture Overview

### Data Structure
This project analyzes e-commerce transaction data using a star schema with six interconnected CSV datasets:

**Core Transaction Tables:**
- `orders_dataset.csv` (10K orders) - Central fact table with order lifecycle
- `order_items_dataset.csv` (16K items) - Line items with pricing data

**Dimensional Tables:**
- `products_dataset.csv` (6K products) - Product catalog with 13 categories
- `customers_dataset.csv` (8K customers) - Geographic customer data
- `order_reviews_dataset.csv` (9K reviews) - Customer satisfaction ratings  
- `order_payments_dataset.csv` (14K payments) - Payment transaction details

**Key Relationships:**
- Orders ↔ OrderItems ↔ Reviews (via `order_id`)
- Orders ↔ Customers (via `customer_id`)
- OrderItems ↔ Products (via `product_id`)

### Analysis Workflow
1. **Data Loading**: Load all 6 CSV files using pandas
2. **Data Merging**: Create `sales_data` by joining orders + order_items tables
3. **Filtering**: Filter for `order_status == 'delivered'` only (revenue analysis scope)
4. **Feature Engineering**: Add year, month, delivery_speed derived columns
5. **Business Metrics**: Calculate revenue, growth rates, geographic distribution
6. **Visualization**: Generate matplotlib/plotly charts for insights

## Code Architecture

### Current Structure
- **Single Notebook Approach**: All analysis contained in `EDA.ipynb`  
- **Linear Execution**: Cells execute sequentially to build analysis dataset
- **Inline Calculations**: Business metrics calculated directly in notebook cells

### Critical Data Patterns
- **Revenue Analysis Scope**: Only 'delivered' orders included (15,095 of 16,047 total)
- **Time Filtering**: Hardcoded 2022/2023 comparison using `.apply(lambda t: t.year)`
- **Geographic Analysis**: US state-level aggregation with Plotly choropleth maps
- **Customer Satisfaction**: 1-5 star review scores correlated with delivery speed

### Known Code Quality Issues
- Multiple `SettingWithCopyWarning` from DataFrame slice assignments
- Use `.loc[]` instead of direct assignment on filtered DataFrames
- Example fix: `sales_delivered.loc[:, 'year'] = ...` instead of `sales_delivered['year'] = ...`

## Key Business Context

### Current Findings (2022-2023)
- **Revenue**: $3.36M in 2023 (down 2.5% from 2022)
- **Order Volume**: 4,635 delivered orders in 2023  
- **Average Order Value**: $724.98
- **Customer Satisfaction**: 4.10/5.0 average review score
- **Delivery Performance**: 8-day average, faster delivery correlates with higher ratings

### Analysis Scope
- **Date Range**: 2022-2023 data with year-over-year comparison
- **Order Status Filter**: Revenue calculations use 'delivered' orders only
- **Geographic Coverage**: All US states represented in dataset
- **Product Categories**: 13 categories analyzed for performance

## Development Notes

### Data Loading Pattern
```python
orders = pd.read_csv('ecommerce_data/orders_dataset.csv')
order_items = pd.read_csv('ecommerce_data/order_items_dataset.csv')
# Merge for analysis
sales_data = pd.merge(left=order_items[cols], right=orders[cols], on='order_id')
```

### Visualization Stack
- **Matplotlib/Seaborn**: Static charts (revenue trends, distributions)
- **Plotly**: Interactive maps and complex visualizations
- **Pandas .plot()**: Quick exploratory charts

### Future Refactoring Targets
- Extract reusable functions for data loading and metric calculations
- Make date ranges configurable instead of hardcoded
- Create modular structure with separate `.py` files for business logic
- Fix pandas warnings with proper DataFrame assignment methods