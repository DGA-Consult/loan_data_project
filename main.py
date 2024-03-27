import yaml
from db_utils import RDSDatabaseConnector

# Load database credentials from the YAML file
credentials_file = 'credentials.yaml'

# Load the credentials
with open(credentials_file, 'r') as file:
    credentials = yaml.safe_load(file)

# Create an instance of RDSDatabaseConnector
rds_connector = RDSDatabaseConnector(credentials)

# Connect to the database
rds_connector.connect()

# Extract data from the RDS database
table_name = 'loan_payments'
df = rds_connector.extract_data(table_name)

# Save the extracted data to a CSV file
if df is not None:
    file_path = 'loan_payments.csv'
    rds_connector.save_to_csv(df, file_path)

# Disconnect from the database
rds_connector.disconnect()
