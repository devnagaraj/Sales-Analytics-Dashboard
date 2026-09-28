# 📊 Sales Analytics Dashboard

> An end-to-end interactive business intelligence dashboard built with Python, Streamlit, and Plotly – analysing Superstore retail sales data to surface actionable insights.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Project Objective

Retail businesses generate enormous amounts of transactional data. Without proper analysis, valuable insights remain hidden. This project transforms raw Superstore sales data into an interactive dashboard that enables business stakeholders to:

- Track KPIs (Sales, Profit, Orders, Margin) at a glance
- Identify top-performing products, customers, and regions
- Understand the impact of discounting on profitability
- Forecast future sales using Machine Learning

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏠 **KPI Overview** | Total Sales, Profit, Orders, Avg Order Value, Profit Margin |
| 📈 **Sales Analysis** | Monthly/Yearly trends, category & sub-category breakdown |
| 💰 **Profit Analysis** | Profit trends, discount impact, loss-making products |
| 🌍 **Regional Analysis** | Sales & profit by region, state-level breakdown |
| 📦 **Product Analysis** | Top products, Sales vs Profit scatter, treemap |
| 👥 **Customer Analysis** | Top customers, segment analysis |
| 🔮 **ML Forecasting** | Linear Regression sales forecast with metrics (MAE, RMSE, R²) |
| 🎛 **Dynamic Filters** | Filter by Year, Region, Category, Segment |

---

## 🗂 Project Structure

```
Sales-Analytics-Dashboard/
├── app.py                        # Main Streamlit application
├── requirements.txt              # Python dependencies
├── README.md
├── .gitignore
├── LICENSE
│
├── data/
│   └── superstore.csv            # Kaggle dataset (optional – app works without it)
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py            # Load CSV or generate sample data
│   ├── data_cleaning.py          # Clean, validate, add time columns
│   ├── analysis.py               # Business logic & aggregations
│   └── visualization.py          # Reusable Plotly chart functions
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── reports/                      # Auto-saved charts from notebook
├── screenshots/
├── deployment/
│   └── DEPLOY.md
└── .streamlit/
    └── config.toml               # Theme configuration
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/Sales-Analytics-Dashboard.git
cd Sales-Analytics-Dashboard
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the dashboard
```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

> **No dataset needed!** The app auto-generates realistic sample data if `data/superstore.csv` is missing.

### 5. (Optional) Add real Kaggle data
Download `Sample - Superstore.csv` from [Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final), rename it `superstore.csv`, and place it in the `data/` folder.

---

## 🛠 Tech Stack

| Tool | Purpose |
|------|---------|
| **Python 3.11** | Core programming language |
| **Pandas** | Data manipulation & aggregation |
| **NumPy** | Numerical operations |
| **Plotly** | Interactive charts |
| **Streamlit** | Web dashboard framework |
| **Scikit-learn** | Linear Regression forecasting |
| **Matplotlib** | Static charts in notebook |

---

## 📸 Screenshots

> Add screenshots to the `screenshots/` folder after running the app and update below.

| Dashboard Home | Sales Analysis |
|---|---|
| *(screenshot)* | *(screenshot)* |

---

## 🔮 Machine Learning – Sales Forecasting

The Forecast tab trains a **Linear Regression** model on historical monthly sales:

- 80/20 train-test split
- Evaluation: MAE, RMSE, R² Score
- Projects N months into the future (configurable via slider)

**Future improvements:** ARIMA, Facebook Prophet, LSTM.

---

## 📈 Key Business Insights (Sample Data)

1. **Technology** generates the highest revenue but **Office Supplies** has better margin efficiency.
2. **High discounts (>30%)** consistently produce negative profit – a major business risk.
3. The **West** and **East** regions lead in total sales.
4. **Consumer** segment contributes ~50% of total revenue.

---

## 🚢 Deployment

See [`deployment/DEPLOY.md`](deployment/DEPLOY.md) for step-by-step Streamlit Cloud deployment.

**Live demo:** [your-app-link-here]

---

## 🔧 Future Improvements

- [ ] Power BI dashboard version
- [ ] ARIMA / Prophet forecasting
- [ ] Customer churn prediction (classification)
- [ ] Product recommendation engine
- [ ] PDF report export
- [ ] Real-time data via database connection

---

## 👤 Author

**Your Name**
- GitHub: [@your_username](https://github.com/your_username)
- LinkedIn: [your-profile](https://linkedin.com/in/your-profile)

---

## 📄 License

This project is licensed under the MIT License – see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- Dataset: [Superstore Sales – Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- Dashboard framework: [Streamlit](https://streamlit.io)
- Charts: [Plotly](https://plotly.com)
