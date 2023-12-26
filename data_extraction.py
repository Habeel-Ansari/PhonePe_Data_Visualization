# data extraction.py

# Import Libraries
import json
import os
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, types
from credentials import DB_USER, DB_PASSWORD

def process_agg_transaction_data(path):
    extracted_data = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if os.path.isdir(state_path):
            for year in os.listdir(state_path):
                year_path = os.path.join(state_path, year)
                if os.path.isdir(year_path):
                    for quarter_file in os.listdir(year_path):
                        quarter_path = os.path.join(year_path, quarter_file)
                        if quarter_file.endswith('.json'):
                            quarter = int(quarter_file.split('.')[0])
                            with open(quarter_path, 'r') as json_file:
                                data = json.load(json_file)
                                for transaction in data['data']['transactionData']:
                                    transaction_type = transaction['name']
                                    for instrument in transaction['paymentInstruments']:
                                        if instrument['type'] == 'TOTAL':
                                            count = instrument['count']
                                            amount = instrument['amount']
                                            extracted_data.append({
                                                'State': state,
                                                'Year': int(year),
                                                'Quarter': quarter,
                                                'TransactionType': transaction_type,
                                                'TransactionCount': count,
                                                'TransactionAmount': amount
                                            })
    return extracted_data


path_to_transaction_json = 'pulse/data/aggregated/transaction/country/india/state'

extracted_data = process_agg_transaction_data(path_to_transaction_json)

df_agg_transaction = pd.DataFrame(extracted_data)

csv_filename = "aggregated_transaction_data.csv"
df_agg_transaction.to_csv(csv_filename, index = False)

def process_agg_user_data(path):
    extracted_data = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if os.path.isdir(state_path):
            for year in os.listdir(state_path):
                year_path = os.path.join(state_path, year)
                if os.path.isdir(year_path):
                    for quarter_file in os.listdir(year_path):
                        quarter_path = os.path.join(year_path, quarter_file)
                        if quarter_file.endswith('.json'):
                            try:
                                with open(quarter_path, 'r') as json_file:
                                    data = json.load(json_file)
                                    quarter = int(quarter_file.split('.')[0])

                                    # Check if 'usersByDevice' is present and not None
                                    if data.get('data', {}).get('usersByDevice') is not None:
                                        for user in data['data']['usersByDevice']:
                                            brand = user['brand']
                                            count = user['count']
                                            percentage = user['percentage']
                                            extracted_data.append({
                                                'State': state,
                                                'Year': int(year),
                                                'Quarter': quarter,
                                                'Brand': brand,
                                                'UserCount': count,
                                                'Percentage': percentage
                                            })
                                    #else:
                                        # Skip the file if 'usersByDevice' is None or not present
                                        #print(f"Skipping file as 'usersByDevice' is None or not present: {quarter_path}")
                            except Exception as e:
                                print(f"Error processing file {quarter_path}: {e}")
    return extracted_data


path_to_user_json = 'pulse/data/aggregated/user/country/india/state'

# Process the user data
extracted_user_data = process_agg_user_data(path_to_user_json)

# Convert to DataFrame
df_agg_user = pd.DataFrame(extracted_user_data)
# Save as CSV
csv_filename_users = 'aggregated_user_data.csv'
df_agg_user.to_csv(csv_filename_users, index=False)

def process_map_transaction_data(path):
    extracted_data = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if os.path.isdir(state_path):
            for year in os.listdir(state_path):
                year_path = os.path.join(state_path, year)
                if os.path.isdir(year_path):
                    for quarter_file in os.listdir(year_path):
                        quarter_path = os.path.join(year_path, quarter_file)
                        if quarter_file.endswith('.json'):
                            with open(quarter_path, 'r') as json_file:
                                data = json.load(json_file)
                                quarter = int(quarter_file.split('.')[0])
                                for district_data in data['data']['hoverDataList']:
                                    district = district_data['name']
                                    for metric in district_data['metric']:
                                        if metric['type'] == 'TOTAL':
                                            count = metric['count']
                                            amount = metric['amount']
                                            extracted_data.append({
                                                'State': state,
                                                'Year': int(year),
                                                'Quarter': quarter,
                                                'District': district,
                                                'TransactionCount': count,
                                                'TransactionAmount': amount
                                            })
    return extracted_data


path_to_map_transaction_json = 'pulse/data/map/transaction/hover/country/india/state'

# Process the map transaction data
extracted_map_transaction_data = process_map_transaction_data(path_to_map_transaction_json)

# Convert to DataFrame
df_map_transactions = pd.DataFrame(extracted_map_transaction_data)

csv_filename_map_transactions = 'map_transaction_data.csv'
df_map_transactions.to_csv(csv_filename_map_transactions, index=False)

def process_map_user_data(path):
    extracted_data = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if os.path.isdir(state_path):
            for year in os.listdir(state_path):
                year_path = os.path.join(state_path, year)
                if os.path.isdir(year_path):
                    for quarter_file in os.listdir(year_path):
                        quarter_path = os.path.join(year_path, quarter_file)
                        if quarter_file.endswith('.json'):
                            try:
                                with open(quarter_path, 'r') as json_file:
                                    data = json.load(json_file)
                                    quarter = int(quarter_file.split('.')[0])

                                    # Check if the expected data is present
                                    if data and 'data' in data and 'hoverDataList' in data['data']:
                                        for item in data['data']['hoverDataList']:
                                            district_name = item['name']
                                            # Assuming metrics contains registered users info
                                            for metric in item['metric']:
                                                if metric['type'] == 'TOTAL':  # Or any other type you're interested in
                                                    registered_users = metric['count']  # Assuming count represents registered users
                                                    extracted_data.append({
                                                        'State': state,
                                                        'Year': int(year),
                                                        'Quarter': quarter,
                                                        'District': district_name,
                                                        'RegisteredUsers': registered_users
                                                    })
                                    else:
                                        print(f"'hoverDataList' not found in file: {quarter_path}")
                            except Exception as e:
                                print(f"Error processing file {quarter_path}: {e}")
    return extracted_data


path_to_map_user_json = 'pulse/data/map/transaction/hover/country/india/state'

# Process the map user data
extracted_map_user_data = process_map_user_data(path_to_map_user_json)

# Convert to DataFrame
df_map_user = pd.DataFrame(extracted_map_user_data)

csv_filename_map_user = 'map_user_data.csv'
df_map_user.to_csv(csv_filename_map_user, index=False)

def process_top_transaction_data(path):
    extracted_data = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if os.path.isdir(state_path):
            for year in os.listdir(state_path):
                year_path = os.path.join(state_path, year)
                if os.path.isdir(year_path):
                    for quarter_file in os.listdir(year_path):
                        quarter_path = os.path.join(year_path, quarter_file)
                        if quarter_file.endswith('.json'):
                            with open(quarter_path, 'r') as json_file:
                                data = json.load(json_file)
                                quarter = int(quarter_file.split('.')[0])
                                # Processing top transaction data
                                for entry in data['data']['pincodes']:
                                    district = entry['entityName']
                                    count = entry['metric']['count']
                                    amount = entry['metric']['amount']
                                    extracted_data.append({
                                        'State': state,
                                        'Year': int(year),
                                        'Quarter': quarter,
                                        'District': district,
                                        'TransactionCount': count,
                                        'TransactionAmount': amount
                                    })
    return extracted_data


path_to_top_transaction_json = 'pulse/data/top/transaction/country/india/state'

# Process the map user data
extracted_top_transaction_data = process_top_transaction_data(path_to_top_transaction_json)

# Convert to DataFrame
df_top_transaction = pd.DataFrame(extracted_top_transaction_data)

csv_filename_top_transaction = 'top_transaction_data.csv'
df_top_transaction.to_csv(csv_filename_top_transaction, index=False)

def process_top_user_data(path):
    extracted_data = []
    for state in os.listdir(path):
        state_path = os.path.join(path, state)
        if os.path.isdir(state_path):
            for year in os.listdir(state_path):
                year_path = os.path.join(state_path, year)
                if os.path.isdir(year_path):
                    for quarter_file in os.listdir(year_path):
                        quarter_path = os.path.join(year_path, quarter_file)
                        if quarter_file.endswith('.json'):
                            with open(quarter_path, 'r') as json_file:
                                data = json.load(json_file)
                                quarter = int(quarter_file.split('.')[0])
                                # Processing top user data
                                for entry in data['data']['pincodes']:
                                    district = entry['name']
                                    registered_users = entry['registeredUsers']
                                    extracted_data.append({
                                        'State': state,
                                        'Year': int(year),
                                        'Quarter': quarter,
                                        'District': district,
                                        'RegisteredUsers': registered_users
                                    })
    return extracted_data


path_to_top_user_json = 'pulse/data/top/user/country/india/state'

# Process the map user data
extracted_top_user_data = process_top_user_data(path_to_top_user_json)

# Convert to DataFrame
df_top_user = pd.DataFrame(extracted_top_user_data)

csv_filename_top_user = 'top_user_data.csv'
df_top_user.to_csv(csv_filename_top_user, index=False)


db_config = {
    'host': 'localhost',
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': 'phonepe_data'
}

# # Establishing a connection to MySQL
connection = mysql.connector.connect(**db_config)
# cursor = connection.cursor()

# # Create a table in MySQL
# create_table_query = '''
# CREATE TABLE IF NOT EXISTS AggregatedTransactions (
#     State VARCHAR(255),
#     Year INT,
#     Quarter INT,
#     TransactionType VARCHAR(255),
#     TransactionCount BIGINT,
#     TransactionAmount FLOAT
# );
# '''
# cursor.execute(create_table_query)
#
# # Load data from CSV to DataFrame
# df = pd.read_csv('aggregated_transaction_data.csv')
#
# # Insert data into the table
# for _, row in df.iterrows():
#     insert_query = "INSERT INTO AggregatedTransactions (State, Year, Quarter, TransactionType, TransactionCount, TransactionAmount) VALUES (%s, %s, %s, %s, %s, %s)"
#     cursor.execute(insert_query, tuple(row))
#
# # Commit changes and close the connection
# connection.commit()
# cursor.close()
# connection.close()

def insert_dataframe_to_sql(df, table_name, connection_details, replace_table=False):
    try:
        # Create an SQLAlchemy engine
        engine = create_engine(f"mysql+mysqlconnector://{connection_details['user']}:{connection_details['password']}@{connection_details['host']}/{connection_details['database']}")

        # Define a mapping from Pandas dtype to SQL dtype
        dtype_mapping = {
            'object': types.VARCHAR(255),
            'int64': types.BIGINT,
            'float64': types.FLOAT,
            'datetime64[ns]': types.DateTime,
            # Add other dtype mappings as needed
        }
        # Map the DataFrame dtypes using the mapping
        sql_dtypes = {col: dtype_mapping[str(df[col].dtype)] for col in df.columns if str(df[col].dtype) in dtype_mapping}

        # Replace or append to the table as specified
        if_exists_action = 'replace' if replace_table else 'append'

        # Use to_sql to insert the data
        df.to_sql(name=table_name, con=engine, if_exists=if_exists_action, index=False, dtype=sql_dtypes)

    except Exception as e:
        print(f"An error occurred while inserting into {table_name}: {e}")
    finally:
        # Close the SQLAlchemy engine
        engine.dispose()


# Insert CSV into sql using insert_dataframe_to_sql function
insert_dataframe_to_sql(df_agg_transaction, 'aggregated_transaction', db_config, replace_table=True)
insert_dataframe_to_sql(df_agg_user, 'aggregated_user', db_config, replace_table=True)
insert_dataframe_to_sql(df_map_transactions, 'map_transactions', db_config, replace_table=True)
insert_dataframe_to_sql(df_map_user, 'map_users', db_config, replace_table=True)
insert_dataframe_to_sql(df_top_transaction, 'top_transactions', db_config, replace_table=True)
insert_dataframe_to_sql(df_top_user, 'top_users', db_config, replace_table=True)