# Loan Data Exploration Project

## Overview
This project aims to perform exploratory data analysis (EDA) on a loan portfolio dataset. The dataset contains information about loan payments stored in an AWS RDS database. The goal is to gain insights into the loan portfolio, uncover patterns, relationships, and anomalies in the data, and make informed decisions about loan approvals, pricing, and risk management.

## Project Structure
- **db_utils.py**: Python script containing the RDSDatabaseConnector class, which handles database connections and data extraction from the RDS database.
- **credentials.yaml**: YAML file containing database credentials. This file is ignored in version control for security reasons.
- **load_data.py**: Python script containing a utility function to load data from a local CSV file into a Pandas DataFrame.
- **loan_payments.csv**: CSV file containing the loan payments data extracted from the RDS database.

## Usage
1. Ensure Python and necessary packages (e.g., psycopg2, pandas, sqlalchemy) are installed.
2. Run `pip install -r requirements.txt` to install required packages.
3. Update the `credentials.yaml` file with your RDS database credentials.
4. Run `python db_utils.py` to connect to the RDS database, extract data, and save it to a CSV file.
5. Run `python load_data.py` to load the data from the CSV file into a Pandas DataFrame and perform initial data exploration.

## Data Dictionary
A detailed description of the columns in the loan_payments dataset can be found below:
- [Insert data dictionary here]

## Future Work
- Implement more advanced data analysis techniques.
- Visualize key insights and findings.
- Develop predictive models for loan approval and risk assessment.
