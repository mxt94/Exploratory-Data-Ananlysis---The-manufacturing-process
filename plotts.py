import yaml
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


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