import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List

# Helper function to calculate failure rates
def calculate_failure_rate(df: pd.DataFrame, category_column: str, failure_column: str) -> pd.Series:
    """
    Calculate the failure rate for each category.
    
    Args:
        df (pd.DataFrame): The dataset to analyze.
        category_column (str): The column containing the categories (e.g., 'Torque', 'Temperature').
        failure_column (str): The column indicating whether the machine failed (0 or 1).
    
    Returns:
        pd.Series: A Series with the failure rate for each category.
    """
    failure_by_category = df.groupby(category_column)[failure_column].mean()
    return failure_by_category

# Function to plot failure by categories
def plot_failure_by_category(failure_data: pd.Series, category_name: str):
    """
    Plot a barplot of failure rates by category.
    
    Args:
        failure_data (pd.Series): A Series containing failure rates by category.
        category_name (str): The name of the category being analyzed (e.g., 'Torque').
    """
    sns.barplot(x=failure_data.index, y=failure_data.values, palette='Blues')
    plt.title(f"Failure by {category_name} Category")
    plt.xlabel(f"{category_name} Category")
    plt.ylabel("Failure Rate")
    plt.show()

# Function to generate recommendations based on failure rates
def generate_recommendations(failure_by_torque: pd.Series, failure_by_temperature: pd.Series, failure_by_rpm: pd.Series):
    """
    Generate recommendations based on the failure rates for different categories.
    
    Args:
        failure_by_torque (pd.Series): The failure rate by torque category.
        failure_by_temperature (pd.Series): The failure rate by temperature category.
        failure_by_rpm (pd.Series): The failure rate by RPM category.
    
    Returns:
        List[str]: A list of recommendations based on the failure rates.
    """
    recommendations = []

    if failure_by_torque.get('High', 0) > 0.05:
        recommendations.append("High torque settings have a higher failure rate. Consider limiting the torque to the 'Medium' category.")
    
    if failure_by_temperature.get('High', 0) > 0.05:
        recommendations.append("High temperature settings have a higher failure rate. Try reducing the temperature to the 'Medium' category.")
    
    if failure_by_rpm.get('High', 0) > 0.05:
        recommendations.append("High RPM settings have a higher failure rate. Consider reducing the RPM to a safer range.")
    
    return recommendations

# Function to print recommendations
def print_recommendations(failure_by_torque: pd.Series, failure_by_temperature: pd.Series, failure_by_rpm: pd.Series):
    """
    Print out the recommendations based on the failure analysis.
    
    Args:
        failure_by_torque (pd.Series): The failure rate by torque category.
        failure_by_temperature (pd.Series): The failure rate by temperature category.
        failure_by_rpm (pd.Series): The failure rate by RPM category.
    """
    print("--- Recommendations Based on Failure Analysis ---\n")
    recommendations = generate_recommendations(failure_by_torque, failure_by_temperature, failure_by_rpm)
    
    if not recommendations:
        print("No significant failure rates detected. The system is functioning well.")
    else:
        for rec in recommendations:
            print(f" - {rec}")

# Main execution block
if __name__ == "__main__":
    # Example data (replace this with actual data reading logic)
    data = {
        'Torque': ['High', 'Medium', 'High', 'Medium', 'High'],
        'Temperature': ['High', 'Medium', 'Medium', 'High', 'Medium'],
        'RPM': ['High', 'Medium', 'Medium', 'Medium', 'High'],
        'Machine failure': [1, 0, 1, 0, 1]
    }
    
    df = pd.DataFrame(data)

    # Calculate failure rates by categories
    failure_by_torque = calculate_failure_rate(df, 'Torque', 'Machine failure')
    failure_by_temperature = calculate_failure_rate(df, 'Temperature', 'Machine failure')
    failure_by_rpm = calculate_failure_rate(df, 'RPM', 'Machine failure')

    # Plot failure rates
    plot_failure_by_category(failure_by_torque, 'Torque')
    plot_failure_by_category(failure_by_temperature, 'Temperature')
    plot_failure_by_category(failure_by_rpm, 'RPM')

    # Print out recommendations based on failure analysis
    print_recommendations(failure_by_torque, failure_by_temperature, failure_by_rpm)





















