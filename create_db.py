import pandas as pd
import sqlite3

# Function to create table and insert data for each sheet
def create_table_and_insert_data(conn, xls_file, year):
    # Read Excel data and iterate over each sheet
    xls = pd.ExcelFile(xls_file)
    for sheet_name in xls.sheet_names:
        # Read data from the current sheet
        df = pd.read_excel(xls, sheet_name, skiprows=2)
        
        # Filter out rows where 'S_No' column contains 'total'
        df = df[~df.iloc[:, 0].astype(str).str.lower().str.contains('total')]
        
        # Remove leading and trailing spaces from column names
        df.columns = df.columns.str.strip()

        # Drop duplicate columns, if any
        df = df.loc[:, ~df.columns.duplicated()]

        # Get column names from the DataFrame
        columns = df.columns.tolist()

        # Create a placeholder for column names and types
        column_definitions = ','.join([f'"{col}" TEXT' for col in columns])

        # Create a table in the database for the current sheet
        table_name = f'{sheet_name}_{year}'.replace(' ', '_')  # Add year to table name
        cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})')

        # Insert data into the table
        df.to_sql(table_name, conn, if_exists='replace', index=False)

# Define SQLite database file
db_file = 'Placement_training.db'

# Establish connection to SQLite database
conn = sqlite3.connect(db_file)
cur = conn.cursor()

# Process each Excel file for respective years
for year, xls_file in zip([2022, 2023], ['2022 Batch -placement Tracker  -Till Date.xlsx', '2023 Batch -placement Tracker  -Till Date.xlsx']): #Add your own data in xlsx format
    create_table_and_insert_data(conn, xls_file, year)
cur.execute('ALTER TABLE BE_2022 RENAME COLUMN "Elogible criteria" TO "Eligible Criteria";')
cur.execute('ALTER TABLE BE_2023 RENAME COLUMN "Elogible criteria" TO "Eligible Criteria";')
cur.execute('ALTER TABLE MBA_2022 RENAME COLUMN "Elogible criteria" TO "Eligible Criteria";')
cur.execute('ALTER TABLE MBA_2023 RENAME COLUMN "Elogible criteria" TO "Eligible Criteria";')

# Commit changes and close connection
conn.commit()
conn.close()

print(f"Database '{db_file}' created successfully.")


