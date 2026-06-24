# 📊 Retail Sales Analytics Dashboard

An end-to-end Retail Sales Analytics project developed using **Python, Pandas, Plotly, and Streamlit**. This project focuses on transforming raw retail sales data into actionable business insights through data cleaning, exploratory data analysis (EDA), KPI reporting, and an interactive dashboard.

---

## 🚀 Project Overview

This project was completed as part of my **Junior Data Analyst Internship at ProDevInfo Solutions**.

The objective was to clean and analyze retail sales data from 2021–2024, calculate key business KPIs, identify sales patterns, and build an interactive dashboard that supports data-driven decision-making.

---

## 🎯 Project Objectives

* Clean and preprocess raw retail sales data.
* Analyze sales trends and business performance.
* Calculate important business KPIs.
* Identify customer and regional sales patterns.
* Develop an interactive dashboard for business monitoring.
* Generate actionable business insights and recommendations.

---

## 🛠️ Technologies Used

* Python
* Pandas
* NumPy
* Plotly
* Streamlit
* Jupyter Notebook

---

## 📂 Project Structure

```text
Internship_project/
│
├── app.py
├── retail_sales_analysis.ipynb
├── retail_sales.csv
├── retail_sales_cleaned.csv
├── README.md
├── requirements.txt
├── Retail_Sales_Analytics_Dashboard_Presentation.pptx
└── Internship Project_Retail Sales Analytics & Dashboard.docx
```

---

## 📁 Dataset Information

### Raw Dataset

`retail_sales.csv`

The dataset contains retail transaction records from 2021 to 2024, including:

* Order ID
* Order Date
* Customer Information
* Product Category
* Product Sub-Category
* Region
* Segment
* Sales
* Profit
* Quantity
* Return Status

### Cleaned Dataset

`retail_sales_cleaned.csv`

After preprocessing, the cleaned dataset was used for analysis and dashboard development.

---

## 🧹 Data Cleaning & Preprocessing

The following preprocessing steps were performed:

* Removed duplicate records
* Handled missing values
* Standardized date formats (YYYY-MM-DD)
* Converted monetary columns into numerical format
* Fixed inconsistent category and segment values
* Standardized returned status values
* Validated quantity fields
* Exported cleaned dataset for analysis

---

## 📓 Jupyter Notebook Analysis

File: `retail_sales_analysis.ipynb`

The notebook contains complete analytical workflows including:

### Exploratory Data Analysis (EDA)

#### Monthly Sales Trend Analysis

* Identified seasonal sales patterns
* Analyzed sales fluctuations over time

#### Sales & Profit by Region

* Compared regional performance
* Evaluated profit contribution by region

#### Sales by Category & Sub-Category

* Identified top-performing product groups
* Compared category-level sales performance

#### Year-over-Year Growth Analysis

* Measured annual business growth
* Evaluated sales performance trends across years

---

## 📈 KPI Analysis

The following KPIs were calculated:

### Revenue Metrics

* Total Revenue
* Total Profit
* Profit Margin

### Customer Metrics

* Top 10 Customers
* Repeat Customer Rate

### Sales Metrics

* Average Order Value (AOV)
* Return Rate
* Total Orders

---

## 📊 Interactive Dashboard

File: `app.py`

The Streamlit dashboard provides real-time business insights through interactive visualizations.

### Dashboard Features

#### KPI Cards

* Total Revenue
* Total Profit
* Total Orders
* Average Order Value (AOV)

#### Interactive Filters

* Date Range
* Region
* Category
* Segment

#### Visualizations

* Monthly Sales Trend
* Sales by Category
* Sales by Region
* Top 10 Customers
* Filtered Data Table

#### Export Feature

* Download filtered dataset as CSV

---

## 📋 Key Business Insights

### 1. Strong Seasonal Sales Patterns

Monthly trend analysis revealed recurring sales peaks, indicating seasonal demand fluctuations.

### 2. Technology Category Dominates Revenue

Technology products generated the highest overall sales revenue among all categories.

### 3. Regional Performance Differences

Certain regions consistently outperformed others, highlighting opportunities for regional growth strategies.

### 4. Customer Revenue Concentration

A small group of customers contributed a significant portion of total revenue.

### 5. Business Growth Over Time

Year-over-year analysis showed overall business growth and increasing sales performance.

---

## 💡 Recommendations

* Increase investment in high-performing product categories.
* Improve marketing efforts in lower-performing regions.
* Implement customer retention programs for top customers.
* Optimize inventory planning based on seasonal demand patterns.
* Monitor return rates to improve profitability.

---

## ▶️ Installation

### Clone Repository

```bash
git clone https://github.com/nihal-mhd/Retail-Sales-Analytics-Dashboard.git
```

### Move to Project Directory

```bash
cd Retail-Sales-Analytics-Dashboard
```

### Install Dependencies

```bash
pip install pandas numpy plotly streamlit
```

### Run Dashboard

```bash
streamlit run app.py
```

---

## 🔮 Future Enhancements

* Sales Forecasting using Machine Learning
* Customer Segmentation Analysis
* Advanced KPI Monitoring
* Product Recommendation System
* Cloud Deployment
* Real-Time Database Integration

---

## 👨‍💻 Internship Details

**Intern:** Nihal Muhammed V

**Role:** Junior Data Analyst Intern

**Organization:** ProDevInfo Solutions

**Mentor:** Abdul Vahab P

---

## 📬 Author

**Nihal Muhammed V**

GitHub: https://github.com/nihal-mhd

---

## ⭐ Project Outcome

Successfully developed a complete Retail Sales Analytics solution involving data cleaning, exploratory data analysis, KPI reporting, business insight generation, and an interactive Streamlit dashboard to support data-driven decision-making.
