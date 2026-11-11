# FoodX — Big Data Analytics for Food Delivery

FoodX analyses food-delivery order history to understand demand patterns, restaurant performance, delivery operations, customer segments, and restaurant recommendations.

## Project components

- **PySpark + Spark SQL:** data loading, cleaning, and analytical queries.
- **Demand analysis:** hourly and day-of-week order patterns.
- **Restaurant and delivery analysis:** order volume, order value, ratings, kitchen preparation time (KPT), rider wait, and distance.
- **K-Means (Spark MLlib):** customer segmentation using order frequency, spending, average order value, and discounts.
- **ALS (Spark MLlib):** collaborative-filtering restaurant recommendations.
- **Streamlit + Plotly:** interactive dashboard using exported result CSVs.

## Repository layout

The current GitHub upload stores the notebook, raw dataset, and result CSVs in the repository root:

```text
FoodX_Big_Data_Analytics/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── FoodX_Big_Data_Analytics.ipynb
├── order_history_kaggle_data.csv
├── daily_demand.csv
├── hourly_demand.csv
├── restaurant_analysis.csv
├── delivery_analysis.csv
├── customer_segments.csv
└── recommendations.csv
```

The dashboard also supports the alternative `data/results/` location for result CSVs and `data/raw/` for the source dataset.

## Run the dashboard locally

Use Python 3.10 or newer.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

The dashboard opens in your browser. It looks for the six result CSVs beside `app.py` first, then checks `data/results/`.

## Re-run the analytics

Open `FoodX_Big_Data_Analytics.ipynb` in Google Colab, upload the raw CSV when prompted, and run the notebook cells in order. The notebook uses PySpark and exports the analytical result tables. Its Colab-specific upload/download cells are intended for Colab; local execution may require adapting those cells.

## Important notes

- The dashboard displays exported analytical results; it does not retrain K-Means or ALS when the app starts.
- Run the notebook to regenerate result CSVs after changing the source data or model settings.
- The raw dataset is included for reproducibility. Check the dataset's original Kaggle licence/terms before redistributing it publicly.
