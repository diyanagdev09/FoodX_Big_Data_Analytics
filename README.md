# FoodX — Big Data Analytics for Food Delivery

FoodX analyses food-delivery order history to understand demand patterns, restaurant performance, delivery operations, customer segments, and restaurant recommendations.

## Project components

- **PySpark + Spark SQL:** data loading, cleaning, and analytical queries.
- **Demand analysis:** hourly and day-of-week order patterns.
- **Restaurant and delivery analysis:** order volume, order value, ratings, KPT, rider wait, and distance.
- **K-Means (Spark MLlib):** customer segmentation using order frequency, spending, average order value, and discounts.
- **ALS (Spark MLlib):** collaborative-filtering restaurant recommendations.
- **Streamlit + Plotly:** standalone dashboard using exported result CSVs.

## Repository layout

```text
FoodX_Big_Data_Analytics/
├── app.py
├── requirements.txt
├── notebooks/
│   └── FoodX_Big_Data_Analytics.ipynb
└── data/
    ├── raw/
    │   └── order_history_kaggle_data.csv
    └── results/
        ├── daily_demand.csv
        ├── hourly_demand.csv
        ├── restaurant_analysis.csv
        ├── delivery_analysis.csv
        ├── customer_segments.csv
        └── recommendations.csv
```

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

The dashboard opens in your browser. It uses the CSV outputs already included in `data/results/`.

## Re-run the analytics

Open `notebooks/FoodX_Big_Data_Analytics.ipynb` in Google Colab. Upload the raw CSV when prompted and run the notebook cells in order. The notebook uses PySpark and exports the analytical result tables.

## Important notes

- The included dashboard displays the exported results; it does not retrain K-Means or ALS when the app starts.
- Run the notebook to regenerate result CSVs after changing the source data or model settings.
- The raw dataset is included for reproducibility. Check the dataset's original Kaggle licence/terms before redistributing it publicly.
- The notebook is a Colab workflow; local execution may require adapting its `google.colab` upload/download cells.
