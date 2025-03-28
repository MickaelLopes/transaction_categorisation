import logging 
import pandas as pd 
import pandera as pa
import sys
import argparse


# Set up logging 
logging_format = "%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO)
log = logging.getLogger(__name__)

# Set up constants
input_filepath = "data/transactions.csv"
output_filepath = "data/report.csv" 

# Set up argument parser
parser = argparse.ArgumentParser(description="Transaction Categorisation Script")
parser.add_argument("--debug", action="store_true", help="Enable debug mode")

def load_data(filename : str, rows_to_skip : int = 2) -> pd.DataFrame:
    log.info(f"Loading data from {filename}")
    try: 
        data = pd.read_csv(filename, skiprows=rows_to_skip)
        log.info(f"Data loaded successfully")
        return data
    except FileNotFoundError:
        log.error(f"File {filename} not found")
        raise FileNotFoundError

def convert_value_to_float(value:[str|int|float]) -> float:
    # Take into account the empty values
    if pd.isna(value):
        return 0.0
    
    if isinstance(value, int):
        return float(value)
    elif isinstance(value, float):
        return value
    elif isinstance(value, str):
        try : 
            return float(value.replace(",", ""))
        except ValueError as e:
            log.error(f"Value {value} is not a valid float: {e}")
            raise ValueError
    else:
        log.error(f"Value {value} is not a valid type")
        raise ValueError
    
def clean_columns(data: pd.DataFrame) -> pd.DataFrame:
    # Castint Date into datetime
    log.info("Cast 'Date' column to datetime")
    try : 
        data["Date"] = pd.to_datetime(data["Date"])
    except KeyError as e:
        log.error(f"Column 'Date' not found: {e}")
        raise
    except Exception as e:
        log.error(f"An error occurred while casting 'Date' column: {e}")
        raise
    
    # Cleaning 'Debit' and 'Credit' columns into float
    log.info("Cleaning 'Debit' and 'Credit' columns")
    try : 
        data["Debit"] = data['Debit'].apply(convert_value_to_float)
        data["Credit"] = data['Credit'].apply(convert_value_to_float)
    except KeyError as e:
        log.error(f"Column 'Debit' or 'Credit' not found: {e}")
        raise
    except Exception as e:
        log.error(f"An error occurred while casting 'Debit' or Credit columns: {e}")
        raise
    
    # Cleaning 'Account' and 'Department'. Removing leading and trailing whitespaces and capitalising first letter
    log.info("Cleaning 'Account' and 'Department' columns")
    data["Account"] = data["Account"].str.strip().str.lower().str.capitalize().fillna("")
    data["Department"] = data["Department"].str.strip().str.lower().str.capitalize().fillna("") 
    return data

def dq_data(data : pd.DataFrame) -> pd.DataFrame:
    log.info("Performing Data Quality checks")
    try : 
        data = clean_columns(data)
    except Exception as e:
        log.error(f"An error occurred while cleaning columns: {e}")
        sys.exit(1)
    # Validation checks could be redundant since we are already casting the columns
    # However, it is a good placeholder to add more complex checks in the future if necessary
    schema = pa.DataFrameSchema(
        columns = {
            "Date" : pa.Column(pa.DateTime, coerce=True, nullable=False),
            "Debit" : pa.Column(pa.Float, coerce=True, nullable=False),
            "Credit" : pa.Column(pa.Float, coerce=True, nullable=False),
            "Account" : pa.Column(pa.String, nullable=True),
            "Department" : pa.Column(pa.String, nullable=True),
        }
    )
    try: 
        schema.validate(data)
        log.info("Data quality checks passed")
        return data
    except pa.errors.SchemaError as e:
        log.error(f"Data quality checks failed: {e}")
        sys.exit(1)
    
def categorise_transaction(account: str, department: str) -> str:
    log.debug(f"Categorising transactions for account {account} and department {department}")
    if account.lower() == 'marketing' : 
        if department.lower() == 'traffic':
            log.debug(f"Transaction belongs to 'Traffic' department")
            return 'Traffic'
        else : 
            log.debug(f"Transaction belongs to 'Marketing' department")
            return 'Marketing'
    else : 
        log.debug(f"Transaction belongs to 'Other' department")
        return 'Other'

def create_report(data: pd.DataFrame) -> pd.DataFrame:
    log.info("Creating report")
    # Calculating Category for each transaction
    data["Category"] = data.apply(lambda x: categorise_transaction(x["Account"], x["Department"]), axis=1)
    # Allow to sort by 
    category_order = pd.CategoricalDtype(categories=["Traffic", "Marketing", "Other"], ordered=True)
    data["Category"] = data["Category"].astype(category_order)
    # Casting Date to period to group by month
    data['Month'] = data['Date'].dt.to_period('M')
    
    # Create report / observed variable force to show all the categories even if they are not present in the data for a given month (can be set to False to hide them)
    report = data.groupby(['Month', 'Category'], observed=False).agg({'Debit': 'sum', 'Credit': 'sum'}).reset_index()
    report['Total'] = report['Debit'] - report['Credit']
    report = report.drop(columns = ['Debit', 'Credit'])
    report = report.sort_values(by=['Month', 'Category'], ascending=[True, True]) # Sort by Month and Category
    report['Month'] = report['Month'].dt.to_timestamp().dt.month_name() # Cast Month to String

    log.info("Report created successfully")
    return report

def transactions_categorisation(data: pd.DataFrame) -> pd.DataFrame: 
    log.info("Starting Transaction Categorisation process")
    data = dq_data(data)
    data_report = create_report(data)
    log.info("Transaction categorisation process completed")
    return data_report
    
if __name__ == "__main__":
    args = parser.parse_args()
    # Set logging level based on debug argument
    if args.debug:
        log.setLevel(logging.DEBUG)
    
    # Import data     
    log.info("Import transaction data")
    df_transaction = load_data(input_filepath)
    log.info("Transaction data loaded successfully")
    
    # Create report
    df_report = transactions_categorisation(df_transaction)

    # Save report
    df_report.to_csv(output_filepath, index=False)
    log.info(f"Report saved to {output_filepath}")