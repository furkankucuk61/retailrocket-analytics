# Retailrocket – E-Commerce Customer Behavior & Conversion Analysis

## Project Overview

This project analyzes e-commerce customer behavior using the Retailrocket Recommender System Dataset.

The main goal is to understand how visitors interact with products, identify conversion funnel drop-offs, segment customers based on their behavior, and evaluate product and category performance.

The analysis was conducted using Python, Pandas, NumPy, Matplotlib, and Seaborn.

## Business Objectives

- Analyze customer interactions across product views, add-to-cart events, and transactions.
- Measure customer-level and session-level conversion rates.
- Build an ordered conversion funnel.
- Identify daily and weekly behavioral patterns.
- Segment customers based on engagement and purchasing behavior.
- Identify products with high views but low cart activity.
- Identify products with high cart activity but low purchase activity.
- Compare product and category performance.

## Dataset

**Source:** [Retailrocket Recommender System Dataset – Kaggle](https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset)

The dataset contains e-commerce event records, product properties, and category information.

Main event types:
- `view`
- `addtocart`
- `transaction`

The raw dataset is not included in this repository. Download it from Kaggle and place the files in `data/raw/`.

Expected raw files:
- `events.csv`
- `item_properties_part1.csv`
- `item_properties_part2.csv`
- `category_tree.csv`

## Key Findings

### Conversion Analysis

- Total sessions: **1,761,675**
- Sessions with purchases: **14,297**
- Session conversion rate: **0.81%**
- Total customers: **1,407,580**
- Purchasing customers: **11,719**
- Customer conversion rate: **0.83%**

### Ordered Session Funnel

The ordered funnel uses the first recorded timestamp of each event type within a session.

| Funnel Stage | Sessions |
|---|---:|
| View | 1,755,781 |
| Add to Cart After View | 35,830 |
| Transaction After Add to Cart | 10,410 |

- View-to-cart conversion: **2.04%**
- Cart-to-purchase conversion: **29.05%**
- End-to-end ordered conversion: **0.59%**

### Customer Segmentation

| Segment | Customers | Share |
|---|---:|---:|
| Product Browsers | 1,368,715 | 97.24% |
| Cart Abandoners | 27,146 | 1.93% |
| Purchasers | 11,719 | 0.83% |

Highly engaged customers had a purchase rate of approximately **5.53%**, compared with approximately **0.05%** among customers with lower engagement.

This is an observed association and does not establish causation.

### Product and Category Analysis

- Total products observed: **235,061**
- Products with category information: **185,246**
- Category coverage: **78.82%**
- Category 959 had the highest transaction event volume among the analyzed categories, with **532 transactions**.

Product opportunity analysis also identifies:
- Products with high views but relatively low add-to-cart activity.
- Products with high add-to-cart activity but relatively low purchase activity.

## Methodology

1. Data loading and initial profiling
2. Data quality checks
3. Timestamp conversion and feature engineering
4. Session identification using a 30-minute inactivity threshold
5. Customer-level and session-level analysis
6. Event-presence and ordered conversion funnel analysis
7. Daily and weekday performance analysis
8. Customer segmentation
9. Product and category performance analysis
10. Product opportunity analysis
11. Data visualization and report generation

## Project Structure

```text
retailrocket-analytics/
│
├── data/
│   ├── raw/                 # Downloaded source data (not tracked)
│   └── processed/           # Generated datasets (not tracked)
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   └── 03_customer_behavior.ipynb
│
├── src/
│   ├── data_loading.py
│   ├── data_cleaning.py
│   ├── data_quality.py
│   ├── feature_engineering.py
│   ├── analysis.py
│   ├── ordered_funnel.py
│   ├── daily_analysis.py
│   ├── visualization.py
│   ├── customer_segmentation.py
│   ├── customer_segmentation_visualization.py
│   ├── product_analysis.py
│   ├── product_visualization.py
│   └── product_opportunity_analysis.py
│
├── reports/                 # Generated analysis reports
├── images/                  # Generated charts
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/furkankucuk61/retailrocket-analytics.git
cd retailrocket-analytics
```

Create and activate a virtual environment:

**Windows PowerShell**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Download the dataset from Kaggle and place the four source CSV files in `data/raw/`.

## Running the Analysis

Run the Python scripts from the project root directory.

Example:

```bash
python src/data_loading.py
python src/data_quality.py
python src/feature_engineering.py
python src/analysis.py
python src/ordered_funnel.py
python src/daily_analysis.py
python src/visualization.py
python src/customer_segmentation.py
python src/customer_segmentation_visualization.py
python src/product_analysis.py
python src/product_visualization.py
python src/product_opportunity_analysis.py
```

Some scripts depend on output files created by earlier steps, so run them in the order shown.

## Tools and Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook
- Git and GitHub

## Limitations

- The dataset does not provide reliable sales revenue or advertising cost information; therefore, revenue, profit, and ROAS are not calculated.
- Sessions are inferred using a 30-minute inactivity threshold.
- Timestamps are analyzed in UTC.
- The first and last dates in the dataset may represent partial days.
- The ordered funnel is based on the first timestamp of each event type within a session; it is not a complete reconstruction of every event sequence.
- Some products do not have category information.
- Event counts and unique customer counts represent different metrics and should not be interpreted interchangeably.

## Author

**Furkan Küçük**

GitHub: [furkankucuk61](https://github.com/furkankucuk61)

---

*This project was developed as a practical data analytics portfolio project, focusing on customer behavior, conversion analysis, segmentation, and product performance.*
