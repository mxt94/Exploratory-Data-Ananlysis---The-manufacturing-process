import yaml
import pandas as pd 
from sqlalchemy import create_engine

class RDSDatabaseConnector:
    def __init__(self, credentials):
        """Initialize the database connector with the provided credentials."""
        self.host = credentials['RDS_HOST']
        self.database = credentials['RDS_DATABASE']
        self.user = credentials['RDS_USER']
        self.password = credentials['RDS_PASSWORD']
        self.port = credentials['RDS_PORT']
        self.engine = None
    
    def initialize_engine(self):
        """Initialize a SQLAlchemy engine using the provided credentials."""
        connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine = create_engine(connection_string)
        print("SQLAlchemy engine initialized.")
    
    def extract_data(self, table_name):
        """Extract data from the specified table and return it as a Pandas DataFrame."""
        if self.engine is None:
            raise Exception("Database engine is not initialized.")
        
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql(query, self.engine)
        return df

def load_credentials(filepath='credentials.yaml'):
    """Load database credentials from a YAML file and return as a dictionary."""
    with open(filepath, 'r') as file:
        credentials = yaml.safe_load(file)
    print(f"Loaded credentials: {credentials}")  # Debugging line
    return credentials

def save_to_csv(df, filename):
    """Save the DataFrame to a CSV file."""
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}.")

def load_data_from_csv(filename):
    """Load data from a CSV file into a Pandas DataFrame."""
    df = pd.read_csv(filename)
    
    # Print the shape of the DataFrame
    print(f"Data shape: {df.shape}")
    
    # Print a sample of the data
    print("Sample data:")
    print(df.head())
    
    return df
if __name__ == "__main__":
    try:
        credentials = load_credentials()
        
        db_connector = RDSDatabaseConnector(credentials)
        db_connector.initialize_engine()
        
        failure_data_df = db_connector.extract_data('failure_data')
        
        save_to_csv(failure_data_df, 'failure_data.csv')
        
        # Load the data from CSV and print the details
        loaded_data = load_data_from_csv('failure_data.csv')
        
    except Exception as e:
        print(f"An error occurred: {e}")





















