# Exploratory-Data-Ananlysis---The-manufacturing-process

## Table of contents
 - Description
 - Installation Instructions
 - Usage Instructions
 - File Structure
 - License 

## Descripton
Within this projct I will showcase mt extracting and anaylsis skills I have learnt thus far. This project aims to perform exploratory data analysis (EDA) and failure analysis on a manufacturing process dataset. The goal is to identify patterns or risk factors that could contribute to machine failures, such as torque, temperature, and RPM. Based on these insights, recommendations are provided to optimize the machine setup and reduce failure rates.

### Key Tasks:
- Perform exploratory data analysis on machine failure data.
- Categorize key machine settings (torque, temperature, and RPM).
- Analyze failure rates by these categories.
- Generate recommendations based on the failure analysis to optimize machine settings and reduce failures.

### Requirements:
- Python 3.1 or higher
- Pandas, Seaborn, Matplotlib libraries
- Jupyter Notebook (optional for running the project interactively)

### Lessons Learned:
- Data preprocessing and cleaning techniques were critical to handle missing values, categorize data, and ensure meaningful analysis.
- Statistical and visualization techniques were used to uncover trends and patterns in machine failure data.
- The importance of dynamically handling edge cases, such as missing or limited categories in the data, was highlighted.

## Installation Instructions
1) Ensure that you have python installed on your machine, which you can dowload on the official python website

2) Clone the repository:
   - Open your terminal
   - navigate to the directory where you want to clone the project
   - run the following command to clone the repository:
   git clone https://github.com/mxt94/Exploratory-Data-Ananlysis---The-manufacturing-process.git

3) Navigate to the project directory
    - you can do so using the following command:
      cd Exploratory-Data-Ananlysis---The-manufacturing-process

4) Install required packages:
   - pandas:
   - seaborn: 
   - matplotlib

     you can install these packages using the pip command within the terminal using the following command:
     pip install pandas seaborn matplotlib

5) Run the script by exceuting the following command in your terminal:
   python db_utils.py

   This will perform the analysis

## Usage Instructions

1) After setting up the project as described in the installation instructions, you can run the script (db_utils.py) that analyzes machine failure data.

2) The script will generate plots showing the failure rates by torque, temperature, and RPM categories, and it will provide recommendations for reducing machine failures.

3) Modify the thresholds in the code to experiment with different categories for torque, temperature, and RPM.
   
## File Structure

Here is what the file strcture should look like:

/Exploratory-Data-Ananlysis--- The-manufacturing-process/
│
├── db_utils.py              # Main analysis script
├── failure_data_cleaned.csv  # Processed and cleaned dataset
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation


## License 

This prohected is licensed under the MIT License. See the License file for details.

   
