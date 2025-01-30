import yaml
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

class DataTransform:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def convert_to_numeric(self, column_name: str):
        """
        Converts a column to numeric if possible, forcing errors to NaN.
        
        :param column_name: Name of the column to convert
        :return: None (modifies the DataFrame in place)
        """
        self.df[column_name] = pd.to_numeric(self.df[column_name], errors='coerce')
        
    def convert_to_datetime(self, column_name: str):
        """
        Converts a column to datetime format.
        
        :param column_name: Name of the column to convert
        :return: None (modifies the DataFrame in place)
        """
        self.df[column_name] = pd.to_datetime(self.df[column_name], errors='coerce')

    def convert_to_categorical(self, column_name: str):
        """
        Converts a column to categorical type.
        
        :param column_name: Name of the column to convert
        :return: None (modifies the DataFrame in place)
        """
        self.df[column_name] = self.df[column_name].astype('category')

    def clean_column(self, column_name: str, symbol: str):
        """
        Cleans a column by removing unwanted symbols.
        
        :param column_name: Name of the column to clean
        :param symbol: Symbol to remove from the column
        :return: None (modifies the DataFrame in place)
        """
        self.df[column_name] = self.df[column_name].str.replace(symbol, '', regex=True)

class DataFrameInfo:
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def describe_columns(self):
        return self.df.describe(include='all').transpose()

    def extract_statistical_values(self):
        """
        Extract mean, median, and standard deviation for all columns.
        
        :return: Dictionary with statistical values
        """
        stats = {}
        stats['mean'] = self.df.mean()
        stats['median'] = self.df.median()
        stats['std'] = self.df.std()
        return stats

    def count_distinct_values(self):
        """
        Count distinct values in each categorical column.
        
        :return: Dictionary with distinct counts for categorical columns
        """
        distinct_values = {}
        for column in self.df.select_dtypes(include='category').columns:
            distinct_values[column] = self.df[column].nunique()
        return distinct_values

    def null_values_info(self):
        """
        Count NULL values in each column and return as a DataFrame.
        
        :return: DataFrame with count and percentage of NULLs in each column
        """
        null_count = self.df.isnull().sum()
        null_percentage = (null_count / len(self.df)) * 100
        return pd.DataFrame({
            'null_count': null_count,
            'null_percentage': null_percentage
        })
    
    def print_shape(self):
        """
        Prints the shape (rows, columns) of the DataFrame.
        
        :return: None
        """
        print(f"Shape of the DataFrame: {self.df.shape}")

class DataFrameTransform:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def remove_missing_values(self, threshold: float = 0.2):
        """
        Remove columns that have more than a certain percentage of missing values.
        
        :param threshold: Percentage threshold above which columns are dropped
        :return: DataFrame with missing values removed
        """
        missing_percentage = self.df.isnull().mean() * 100
        cols_to_drop = missing_percentage[missing_percentage > threshold].index
        self.df.drop(cols_to_drop, axis=1, inplace=True)
        print(f"Removed columns: {cols_to_drop}")
    
    def impute_missing_values(self, strategy: str = 'mean'):
        """
        Impute missing values using mean or median.
        
        :param strategy: 'mean' or 'median' strategy for imputation
        :return: None (modifies the DataFrame in place)
        """
        if strategy == 'mean':
            self.df.fillna(self.df.mean(), inplace=True)
        elif strategy == 'median':
            self.df.fillna(self.df.median(), inplace=True)
        print(f"Missing values imputed using {strategy}.")