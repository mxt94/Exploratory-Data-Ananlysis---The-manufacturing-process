import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

class RDSDatabaseConnector:
    def __init__(self, credentials: dict):
        self._host = credentials['RDS_HOST']
        self._database = credentials['RDS_DATABASE']
        self._user = credentials['RDS_USER']
        self._password = credentials['RDS_PASSWORD']
        self._port = credentials['RDS_PORT']
        self._engine: Engine = None

    def initialize_engine(self) -> None:
        connection_string = f"postgresql://{self._user}:{self._password}@{self._host}:{self._port}/{self._database}"
        self._engine = create_engine(connection_string)
        print("SQLAlchemy engine initialized.")

    def extract_data(self, table_name: str) -> pd.DataFrame:
        if self._engine is None:
            raise RuntimeError("Database engine is not initialized.")
        
        query = f"SELECT * FROM {table_name};"
        return pd.read_sql(query, self._engine)

class DataFrameTransform:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe

    def check_missing_values(self) -> pd.DataFrame:
        null_counts = self.dataframe.isnull().sum()
        null_percentage = (null_counts / len(self.dataframe)) * 100
        return pd.DataFrame({'Count': null_counts, 'Percentage': null_percentage})

    def drop_columns_with_missing_values(self, threshold: float = 50.0) -> None:
        missing_info = self.check_missing_values()
        columns_to_drop = missing_info[missing_info['Percentage'] > threshold].index
        self.dataframe.drop(columns=columns_to_drop, inplace=True)
        print(f"Dropped columns: {list(columns_to_drop)}")

    def clean_column(self, column: str) -> None:
        """Cleans a column by converting values to numeric, handling non-numeric values."""
        print(f"Cleaning column: '{column}'")
        # Check if column is numeric
        if self.dataframe[column].dtype != 'object':  # Only clean numeric columns
            # Convert to numeric, coercing errors to NaN (i.e., invalid entries like 'L50595')
            self.dataframe[column] = pd.to_numeric(self.dataframe[column], errors='coerce')

            # Check for problematic rows after coercion
            problematic_rows = self.dataframe[column].isnull()
            if problematic_rows.any():
                print(f"Found problematic rows in '{column}' (non-numeric values turned into NaN):")
                print(self.dataframe[problematic_rows][column])

    def impute_missing_values(self) -> None:
        """Impute missing values for each column, cleaning as necessary."""
        for column in self.dataframe.columns:
            if column == 'product ID':  # Skip 'product ID' column for numerical operations
                continue

            if self.dataframe[column].isnull().any():
                print(f"\nProcessing column: '{column}'")

                # Clean the column to remove or coerce non-numeric values
                self.clean_column(column)

                # Impute missing values
                if self.dataframe[column].dtype in [np.float64, np.int64]:
                    # If it's numeric, impute missing values with the median
                    median_value = self.dataframe[column].median()
                    self.dataframe[column] = self.dataframe[column].fillna(median_value)
                    print(f"Imputed missing values in '{column}' with median: {median_value}")
                else:
                    # If it's still not numeric (after coercion), impute with mode (most frequent value)
                    mode_value = self.dataframe[column].mode()[0]
                    self.dataframe[column] = self.dataframe[column].fillna(mode_value)
                    print(f"Imputed missing values in '{column}' with mode: {mode_value}")

    def identify_outliers(self, column: str, method: str = 'IQR') -> list:
        """Identify outliers using the IQR method."""
        if self.dataframe[column].dtype in [np.float64, np.int64]:  # Only detect outliers on numeric columns
            if method == 'IQR':
                Q1 = self.dataframe[column].quantile(0.25)
                Q3 = self.dataframe[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = self.dataframe[(self.dataframe[column] < lower_bound) | (self.dataframe[column] > upper_bound)]
                print(f"Identified outliers in '{column}':")
                print(outliers)
                return outliers.index.tolist()
            else:
                raise ValueError("Method not supported. Please use 'IQR'.")
        else:
            return []

    def remove_outliers(self, column: str, outliers_indices: list) -> None:
        """Remove outliers by dropping rows with outlier values."""
        if len(outliers_indices) > 0:
            self.dataframe.drop(index=outliers_indices, inplace=True)
            print(f"Removed {len(outliers_indices)} outlier rows from '{column}'.")

    def transform_skewed_columns(self, skewed_columns: list) -> None:
        """Apply transformation (log transformation) to reduce skewness."""
        for column in skewed_columns:
            if self.dataframe[column].dtype in [np.float64, np.int64]:
                original_skew = self.dataframe[column].skew()
                # Apply log transformation to reduce skewness
                self.dataframe[column] = np.log1p(self.dataframe[column])
                new_skew = self.dataframe[column].skew()
                print(f"Transformed '{column}' from skewness {original_skew:.2f} to {new_skew:.2f}")

    def remove_highly_correlated_columns(self, threshold: float = 0.9) -> None:
        """Remove columns that are highly correlated (above the threshold)."""
        corr_matrix = self.dataframe.corr()
        print("\nCorrelation Matrix:\n", corr_matrix)

        # Find highly correlated columns
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
        to_drop = [column for column in upper.columns if any(upper[column] > threshold)]
        self.dataframe.drop(columns=to_drop, inplace=True)
        print(f"\nDropped highly correlated columns: {to_drop}")

class Plotter:
    @staticmethod
    def plot_missing_values(missing_data: pd.DataFrame) -> None:
        plt.figure(figsize=(10, 6))
        missing_data['Percentage'].plot(kind='bar', color='skyblue')
        plt.title('Percentage of Missing Values in Each Column')
        plt.xlabel('Columns')
        plt.ylabel('Percentage of Missing Values')
        plt.axhline(y=0, color='gray', linewidth=0.8)
        plt.xticks(rotation=45)
        plt.show()

    @staticmethod
    def plot_skewness(dataframe: pd.DataFrame) -> None:
        skewness = dataframe.skew()
        plt.figure(figsize=(10, 6))
        skewness.plot(kind='bar', color='orange')
        plt.title('Skewness of Each Column')
        plt.axhline(0, color='gray', linewidth=0.8)
        plt.ylabel('Skewness')
        plt.xticks(rotation=45)
        plt.show()

    @staticmethod
    def plot_outliers(dataframe: pd.DataFrame, column: str) -> None:
        """Plot boxplot for detecting outliers."""
        plt.figure(figsize=(10, 6))
        dataframe.boxplot(column=column)
        plt.title(f'Boxplot for {column}')
        plt.show()

def load_credentials(filepath: str = 'credentials.yaml') -> dict:
    with open(filepath, 'r') as file:
        credentials = yaml.safe_load(file)
    return credentials

def save_to_csv(dataframe: pd.DataFrame, filename: str) -> None:
    dataframe.to_csv(filename, index=False)
    print(f"Data saved to {filename}.")

def load_data_from_csv(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename)
    print(f"Data shape: {df.shape}")
    return df

if __name__ == "__main__":
    try:
        # Load credentials and initialize the database connector
        credentials = load_credentials()
        db_connector = RDSDatabaseConnector(credentials)
        db_connector.initialize_engine()
        
        # Extract the data
        failure_data_df = db_connector.extract_data('failure_data')

        # Initialize the DataFrameTransform class
        transformer = DataFrameTransform(failure_data_df)

        # Check and visualize missing values before handling
        missing_info_before = transformer.check_missing_values()
        print("Missing values before handling:")
        print(missing_info_before)
        Plotter.plot_missing_values(missing_info_before)

        # Drop columns with excessive missing values
        transformer.drop_columns_with_missing_values(threshold=50.0)

        # Impute missing values
        transformer.impute_missing_values()

        # Visualize outliers before removing
        columns_to_check_for_outliers = transformer.dataframe.select_dtypes(include=[np.float64, np.int64]).columns
        for column in columns_to_check_for_outliers:
            Plotter.plot_outliers(transformer.dataframe, column)

        # Identify and remove outliers
        for column in columns_to_check_for_outliers:
            outliers = transformer.identify_outliers(column)
            transformer.remove_outliers(column, outliers)

        # Visualize outliers after removal
        for column in columns_to_check_for_outliers:
            Plotter.plot_outliers(transformer.dataframe, column)

        # Remove highly correlated columns
        transformer.remove_highly_correlated_columns(threshold=0.9)

        # Identify and visualize skewed columns
        skewed_columns = transformer.dataframe.skew()[transformer.dataframe.skew().abs() > 1].index.tolist()
        Plotter.plot_skewness(failure_data_df)

        # Transform skewed columns
        transformer.transform_skewed_columns(skewed_columns)

        # Visualize skewness after transformation
        Plotter.plot_skewness(transformer.dataframe)

        # Save a copy of the transformed DataFrame for comparison
        save_to_csv(transformer.dataframe, 'transformed_failure_data.csv')

    except Exception as e:
        print(f"An error occurred: {e}")








