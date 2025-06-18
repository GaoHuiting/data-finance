import pandas as pd
import re
from datetime import datetime

# Load the file
data_path = '/Users/jessicagao/Downloads/DA-test/new-finance-data.csv'

# Load the dataset
data = pd.read_csv(data_path, low_memory=False)

# Validation functions
def validate_date_format(date, format_regex):
    if pd.isnull(date) or date == '':
        return False  # Empty fields are invalid
    return bool(re.match(format_regex, str(date)))

def validate_birth_date(birth_date):
    if pd.isnull(birth_date) or birth_date == '':
        return False  # Empty fields are invalid
    try:
        # Convert birth_date to datetime object
        birth_date_obj = datetime.strptime(str(birth_date), '%Y%m%d')  # Assuming format YYYYMMDD
        return birth_date_obj < datetime.today()  # Check if birth_date is older than today
    except ValueError:
        return False 


def validate_postal_code(postal_code):
    if pd.isnull(postal_code) or postal_code == '':
        return False  
    return bool(re.match(r'^[A-Za-z]\d[A-Za-z]\d[A-Za-z]\d$', str(postal_code)))

def validate_percentage(value):
    if pd.isnull(value) or value == '':
        return False  
    try:
        value = float(value)
        return 0 <= value <= 1
    except ValueError:
        return False

def validate_binary(value):
    if pd.isnull(value) or value == '':
        return False  # Treat empty fields as invalid
    return str(value).strip() in ['0', '1'] or value in [0, 1]

# Check if the number is displayed as string
def is_number_string(value):
    
    if pd.isnull(value) or value == '':
        return False  # Treat empty fields as invalid
    return isinstance(value, (int, float)) or str(value).replace('.', '', 1).isdigit()

# if 'insurance_indicator' in data.columns:
#     invalid_records = data[~data['insurance_indicator'].apply(validate_binary)]
#     print("Invalid records for 'insurance_indicator':")
#     print(invalid_records)
#     print(f"Count of invalid records: {len(invalid_records)}")

# Define checks based on the data dictionary
checks = {
    'loan_id': lambda x: not pd.isnull(x) and x != '',  
    'filing_date': lambda x: validate_date_format(x, r'^\d{4}-\d{2}-\d{2}$'),
    'birth_date': validate_birth_date,
    'maturity_date': lambda x: validate_date_format(x, r'^\d{4}-\d{2}-\d{2}$'),
    'postal_code': validate_postal_code,
    'GDS': validate_percentage,
    'TDS': validate_percentage,
    'insurance_indicator': validate_binary,
    'origination_indicator': validate_binary,
    'renewal_indicator': validate_binary,
    'outstanding_amount': is_number_string,
    'authorized_amount': is_number_string,
    'bureau_score': is_number_string,
    'interest_rate': is_number_string,
    'income': is_number_string
}


# Data issue desription
issues = {}
issue_descriptions = {
    'filing_date': "Invalid date format (expected YYYY-MM-DD)",
    'birth_date': "Invalid birth date format (no later than today, expected YYYYMMDD)",
    'postal_code': "Invalid postal code format (expected A1A1A1)",
    'GDS': "Percentage out of range (expected 0 to 1)",
    'TDS': "Percentage out of range (expected 0 to 1)",
    'insurance_indicator': "Invalid binary value (expected 0 or 1)",
    'origination_indicator': "Invalid binary value (expected 0 or 1)",
    'renewal_indicator': "Invalid binary value (expected 0 or 1)",
    'outstanding_amount': "Mixed data types (expected number instead of strings)",
    'authorized_amount': "Mixed data types (expected number instead of strings)",
    'bureau_score': "Mixed data types (expected number instead of strings)",
    'interest_rate': "Mixed data types (expected number instead of strings)",
    'income': "Mixed data types (expected number instead of strings)"
}


# Check for loan_id unique
if 'loan_id' in data.columns:
    duplicate_loan_ids = data['loan_id'].duplicated().sum() #count
    if duplicate_loan_ids > 0:
        print(f"Data quality issue in 'loan_id': Duplicate values found. {duplicate_loan_ids} records affected.")
        issues['loan_id'] = duplicate_loan_ids
    else:
        print("No duplicates found in 'loan_id'.")

# Validate other columns
for column, check in checks.items():
    if column in data.columns:
        invalid_records = data[~data[column].apply(check)]
        issues[column] = len(invalid_records)
        if len(invalid_records) > 0:
            description = issue_descriptions.get(column, "Unknown issue")
            print(f"Data quality issue in '{column}': {description}. {len(invalid_records)} records affected.")

# Output issues
print("\nSummary of Data Quality Issues:")
for column, count in issues.items():
    description = issue_descriptions.get(column, "Unknown issue")
    print(f"{column}: {description}. {count} bad records.")
