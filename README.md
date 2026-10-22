# E-Commerce Sales & Customer Analytics Dashboard

An interactive Streamlit dashboard for exploring e-commerce revenue, profit, orders, customers, products, and customer segments using Python.

> **Data note:** This project uses synthetic/demo data, not verified transactions from a real business. The dataset is useful for demonstrating analytics workflows, but its results must not be presented as real commercial performance. Profit values are simulated and should not be treated as accounting figures.

## What it does

- Filters records by order date, state, product category, and customer segment.
- Summarizes revenue, orders, unique customers, profit, and profit margin.
- Visualizes monthly revenue and profit trends.
- Compares sales by category, state, product, and customer segment.
- Shows average order value, units sold, and a top-products table.
- Lets users inspect the filtered records.

## Technology

- Python
- Streamlit
- Pandas
- NumPy
- Plotly

## Run locally

### 1. Clone the repository

```bash
git clone https://github.com/waridverma6-YLE/ecommerce-sales-dashboard.git
cd ecommerce-sales-dashboard
```

### 2. Create and activate a virtual environment

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies and launch

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print a local URL, typically `http://localhost:8501`.

## Data and methodology

The dashboard reads `data/ecommerce_sales.csv`. If that file is unavailable, the application generates a reproducible synthetic dataset with 1,000 rows and writes it to the `data/` directory.

Core measures:

| Measure | Definition used in this project |
| --- | --- |
| Revenue | Sum of `Sales` |
| Orders | Distinct `Order_ID` count |
| Customers | Distinct `Customer_ID` count in the filtered data |
| Profit | Sum of the supplied `Profit` field |
| Profit margin | Total profit divided by total revenue |
| Average order value | Total revenue divided by distinct orders |

These definitions are suitable for this demonstration dataset. Real-world analysis may require a documented order-level grain, treatment of returns/discounts/tax/shipping, and a finance-approved profit definition.

## Project structure

```text
ecommerce-sales-dashboard/
├── app.py
├── data/
│   └── ecommerce_sales.csv
├── requirements.txt
└── README.md
```

## Known limitations

- The dataset is synthetic; patterns and insights are illustrative only.
- The current application contains most dashboard logic in `app.py`; splitting data preparation, KPI calculations, and chart construction into testable modules is a planned improvement.
- Automated tests and CI checks are not yet documented as part of this project.

## Roadmap

- [ ] Add unit tests for KPI calculations and filtering.
- [ ] Validate required columns, missing values, and data types at load time.
- [ ] Separate data preparation and metric calculations from the Streamlit UI.
- [ ] Add screenshots and a verified hosted demo.
- [ ] Add automated checks with GitHub Actions.

## Author

**Warid Verma** — [GitHub profile](https://github.com/waridverma6-YLE)

This project is a learning portfolio project demonstrating a basic end-to-end business analytics workflow.
