 Stock Data Pipeline 📈❄️

A Python-based **end-to-end data pipeline** that extracts real-time stock ticker information from the [Polygon.io API](https://polygon.io/), automates ingestion with a scheduler, and loads structured data into **Snowflake** for analytics.

Built as part of **Zach Wilson's Data Engineering Beginner Bootcamp**.

---

## 🚀 Features

* **Real-time Data Extraction**: Fetches stock ticker data from Polygon.io API
* **Pagination Handling**: Automatically traverses large datasets using `next_url`
* **Rate Limit Management**: Intelligent retry logic with strategic delays to avoid HTTP 429 errors
* **CSV Export**: Option to save tickers locally in `tickers.csv`
* **Snowflake Integration**: Inserts ticker data into `STOCK_TICKERS';
* **Automation**: `scheduler.py` ensures the pipeline runs continuously and keeps Snowflake data fresh
* **Error Resilience**: Robust error handling for API, JSON, and database operations

---

## 📊 Results

* **Successful Extraction**: 11,730+ stock tickers retrieved
* **Pages Processed**: 12 API pages handled seamlessly
* **Snowflake Loading**: Data written into a cloud data warehouse for analysis
* **Continuous Updates**: Scheduler ensures fresh data without manual intervention

---

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/stock-data-pipeline.git
   cd stock-data-pipeline
   ```

2. **Create virtual environment**

   ```bash
   python -m venv pythonenv
   pythonenv\Scripts\activate   # Windows (cmd)
   source pythonenv/bin/activate  # Mac/Linux
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:

   ```ini
 SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "PRIYAM1991")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "polygon@12345")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "GHSXTHO-HLC50951")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "SNOWFLAKE_LEARNING_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "LEOPRIYAM")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")

SNOWFLAKE_TABLE = "STOCK_TICKERS"
   ```

---

## 📋 Requirements

`requirements.txt`:

```
requests>=2.28.0
python-dotenv>=0.19.0
snowflake-connector-python>=3.0.0
schedule>=1.2.0
```

---

## 🚦 Usage

### Extract to CSV

```bash
python script.py
```

### Load into Snowflake

```bash
python script_snowflake.py
```

### Run with Scheduler (automated pipeline)

```bash
python scheduler.py
```

---

## 📁 Output

* **CSV Mode** → `tickers.csv` with 11,730+ rows
* **Snowflake Mode** → Data loaded into:

  ```
  ATIQUE.PUBLIC.STOCK_TICKERS
  ```
* **Scheduler Mode** → Automates pipeline, inserting fresh data every interval

---

## 🏗️ Architecture

```
Polygon.io API → Pagination & Rate Limit Handling → 
  ├── CSV Export (script.py)  
  ├── Snowflake Load (script_snowflake.py)  
  └── Scheduler Automation (scheduler.py)
```

---

## 📈 Challenges Overcome

* **API Rate Limits** → Solved with retries + strategic delays
* **Large Dataset Pagination** → Extracted 11,000+ records over 12 pages
* **Data Loading** → Mapped API fields into Snowflake table dynamically
* **Automation** → Used Python scheduler to keep pipeline running 24/7

---

## 🎯 Learning Outcomes

* Building **real-world ETL/ELT pipelines**
* Managing **API pagination and throttling**
* Automating ingestion with **Python scheduler**
* Cloud data loading into **Snowflake**
* Following **environment variable security best practices**

---

## 🙏 Acknowledgments

Part of **Zach Wilson’s Free Data Engineering Beginner Bootcamp**.
🔗 Learn more: [learn.dataexpert.io](https://learn.dataexpert.io)
