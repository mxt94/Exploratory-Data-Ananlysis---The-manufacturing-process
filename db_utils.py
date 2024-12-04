import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned data
df = pd.read_csv('failure_data_cleaned.csv')

# Ensure that 'Machine failure' is properly set as 1 for failure, 0 for no failure
df['Machine failure'] = df['Machine failure'].apply(lambda x: 1 if x == 'Failure' else 0)

# Define the categories for analysis
torque_thresholds = [0, 50, 150]  # Example thresholds for Torque
temperature_thresholds = [270, 320]  # Example thresholds for Temperature
rpm_thresholds = [1000, 3000]  # Example thresholds for Rotational Speed

def categorize_column(column, thresholds):
    """Categorize machine settings into 'Low', 'Medium', 'High' based on thresholds."""
    categories = []
    for value in column:
        if value < thresholds[0]:
            categories.append('Low')
        elif value < thresholds[1]:
            categories.append('Medium')
        else:
            categories.append('High')
    return categories

# Apply categorization to each setting
df['Torque Category'] = categorize_column(df['Torque [Nm]'], torque_thresholds)
df['Temperature Category'] = categorize_column(df['Air temperature [K]'], temperature_thresholds)
df['RPM Category'] = categorize_column(df['Rotational speed [rpm]'], rpm_thresholds)

# Group by categories and count failures
failure_by_torque = df.groupby('Torque Category')['Machine failure'].value_counts(normalize=True).unstack(fill_value=0)
failure_by_temperature = df.groupby('Temperature Category')['Machine failure'].value_counts(normalize=True).unstack(fill_value=0)
failure_by_rpm = df.groupby('RPM Category')['Machine failure'].value_counts(normalize=True).unstack(fill_value=0)

# Debugging: Print out the failure by categories dataframes to inspect structure
print("Failure by Torque Category:\n", failure_by_torque)
print("Failure by Temperature Category:\n", failure_by_temperature)
print("Failure by RPM Category:\n", failure_by_rpm)

# Check the column names and make sure the '1' column exists
print("Failure by Torque Columns:", failure_by_torque.columns)
print("Failure by Temperature Columns:", failure_by_temperature.columns)
print("Failure by RPM Columns:", failure_by_rpm.columns)

# Plotting the failure by category
# Plot Failure by Torque Category
plt.figure(figsize=(10, 6))
sns.barplot(x=failure_by_torque.index, y=failure_by_torque.iloc[:, 0], palette='Blues')  # Use .iloc[:, 0] for failure rate (the first column)
plt.title("Failure Percentage by Torque Category")
plt.xlabel("Torque Category")
plt.ylabel("Failure Percentage")
plt.show()

# Plot Failure by Temperature Category
plt.figure(figsize=(10, 6))
sns.barplot(x=failure_by_temperature.index, y=failure_by_temperature.iloc[:, 0], palette='Blues')
plt.title("Failure Percentage by Temperature Category")
plt.xlabel("Temperature Category")
plt.ylabel("Failure Percentage")
plt.show()

# Plot Failure by RPM Category
plt.figure(figsize=(10, 6))
sns.barplot(x=failure_by_rpm.index, y=failure_by_rpm.iloc[:, 0], palette='Blues')
plt.title("Failure Percentage by RPM Category")
plt.xlabel("RPM Category")
plt.ylabel("Failure Percentage")
plt.show()

# Recommendations based on the analysis
def print_recommendations():
    print("\n--- Recommendations Based on Failure Analysis ---\n")
    
    # Check if the 'High' torque category exists before trying to access it
    if 'High' in failure_by_torque.index and failure_by_torque.loc['High', 0] > 0.05:
        print("1. High torque settings have a higher failure rate. Consider limiting the torque to the 'Medium' category to reduce failures.")
    else:
        print("1. Torque seems to have a minimal impact on failure. Continue using the current range, but monitor closely for further analysis.")
    
    # Check if the 'High' temperature category exists before trying to access it
    if 'High' in failure_by_temperature.index and failure_by_temperature.loc['High', 0] > 0.05:
        print("2. High process temperature is associated with a higher failure rate. It's advisable to operate the machine within the 'Medium' temperature range to minimize risk.")
    else:
        print("2. Temperature seems to have a minimal impact on failure. Consider operating within the high-temperature range if needed, but with caution.")

    # Check if the 'High' RPM category exists before trying to access it
    if 'High' in failure_by_rpm.index and failure_by_rpm.loc['High', 0] > 0.05:
        print("3. High RPM has a higher failure rate. You may want to reduce the RPM to 'Medium' or 'Low' categories to decrease failure risk.")
    else:
        print("3. RPM does not seem to be a significant risk factor. High RPM can continue being used but monitor closely.")
        
    print("\n--- General Recommendations ---")
    print("1. Implement real-time monitoring of machine parameters (Torque, Temperature, RPM) to detect and mitigate failure risks.")
    print("2. Consider setting automated limits for torque, temperature, and RPM to ensure they stay within safe operational thresholds.")
    print("3. Conduct periodic maintenance checks to ensure machines are operating at optimal settings and reduce the risk of failure.")
    print("4. Use predictive maintenance models to forecast failure risks based on historical operational data.")

# Print the recommendations based on the failure analysis
print_recommendations()




















