# 🧾 Transaction Categorisation Project

This project takes a CSV of financial transactions, categorises them based on business rules, and outputs a monthly report. It uses Python 3.11+, is fully testable via `unittest`, and includes a reproducible data pipeline managed by [DVC](https://dvc.org/).

## 📁 Project Structure

```
.
├── data/                       # Input & output files (DVC-tracked)
│   ├── transactions.csv        # Input file (DVC remote)
    ├── transactions.csv.dvc    # Input file (DVC tracking file)
│   └── report.csv              # Output file (DVC stage output)
├── src/
│   └── main.py                 # Transaction categorisation script
├── tests/
│   └── test_*.py               # Unit tests for the categorisation logic
├── dvc.yaml                    # DVC pipeline definition
├── dvc.lock                    # DVC pipeline lock file
├── requirements.txt            # Python dependencies
├── .github/workflows/          # GitHub Actions CI workflow
└── README.md                   # You're here!
```

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/MickaelLopes/transaction_categorisation.git
```

### 2. Set up your Python environment

Make sure you're using Python 3.11+.

```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Pull data with DVC

```bash
dvc pull
```

This will download `data/transactions.csv` and (if available) `data/report.csv` from the S3 DVC remote.

## 🚀 Run the Script

To run the categorisation manually:

```bash
python src/main.py
```

This will generate `data/report.csv`.

## 🔁 Reproduce the Pipeline

```bash
dvc repro
```

This will re-run the categorisation stage defined in `dvc.yaml`.

## 🧪 Run Unit Tests

```bash
python -m unittest discover -s tests -v
```

Unit tests are automatically run in GitHub Actions when you:
- Create or update a pull request into `main`

## 📦 DVC Remote Storage

- Input and output data files are managed with [DVC](https://dvc.org/)
- Remote storage: Public S3 bucket
- You do **not** need credentials to run `dvc pull`

## ✅ GitHub Actions

CI/CD is set up via GitHub Actions:
- Tests run on each pull request to `main`
- Uses Python 3.11 and a Windows runner (for compatibility with `pywin32`)

## 🧹 Cleanup Note

This project uses public S3 storage temporarily for exercise purposes. The bucket will be locked or removed after project review.

## 📌 Author

Mickael Lopes – [@MickaelLopes](https://github.com/MickaelLopes/)
