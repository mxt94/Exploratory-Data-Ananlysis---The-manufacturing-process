# Exploratory-Data-Ananlysis---The-manufacturing-process

## Table of contents
 - Description
 - Installation Instructions
 - Usage Instructions
 - File Structure
 - License 

## Descripton
Within this projct I will showcase mt extracting and anaylsis skills I have learnt thus far. The main objective is to retrieve data for quality control analysis and identify potential machine failures. Throughout this project, I will showcase what I have learnt in various areas including database connectivity, data extraction using SQLAlchemy, and data manipulation with Pandas.

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
   - pandas: For data manipulation and analysis
   - sqlalchemy: for database connectivity
   - pyyaml: for loading YAML files
   - pyscopg2: PostgreSQL adapter for pyhton (if you're using PostgreSQL).

     you can install these packages using the pip command within the terminal using the following command:
     pip install pandas sqlalchemy pyyaml psycopg2

5) Configure database credentials:
    - create a file named credentials.yaml in the project directory
      you can do so by running the touch credentials.yaml command in the terminal within the repository
    - Add your AWS RDS database credentials in the following format:
      RDS_HOST: eda-projects.cq2e8zno855e.eu-west-1.rds.amazonaws.com
      RDS_PASSWORD: EDAprocessanalysis
      RDS_USER: manufacturinganalyst
      RDS_DATABASE: process_data
      RDS_PORT: 5432

6) Run the script by exceuting the following command in your terminal:
   python db_utils.py

   This will connect to the database, extract the data and savie it a CSV named failure_data.csv in the project directory

## Usage Instructions

After setting up the project successfully, you can use it to extratcmanufacturing data from the AWS RDS Database using the following steps:

1) Ensure credentials are Set:

  - Before running the script make sure that the credentials.yaml file in the project directory contains the correct database crdentials. The file should look like this:
      RDS_HOST: eda-projects.cq2e8zno855e.eu-west-1.rds.amazonaws.com
      RDS_PASSWORD: EDAprocessanalysis
      RDS_USER: manufacturinganalyst
      RDS_DATABASE: process_data
      RDS_PORT: 5432

2) Within the termina navigate to the project directory using:
   cd Exploratory-Data-Ananlysis---The-manufacturing-process

   - Execute the script to extract data:
     python db_utils.py

3) Data extraction:
   - The script will connect to the AWS RDS Database, exceute a query to extract data from the failure_data table, and save it as a CSV file named failure_data.csv in the project directory.
   - You will see console output indicating the progress suc as confirmation of the SQLAlchemt engine initialisation and success of data extraction

4) Inspect the CSV File:
   - After running the script you can open the failure_data.csv file using any spreadsheet software (like excel) or a text editor to inspect the extracted data.
   - The CSV file contains the following columns:
     * UID: Unique identifier for each machining session.
     * product_ID: Serial number for the specific product.
     * Type: Quality level of the product (L, M, H).
     * air temperature [K]: Average room temperature during the process (in Kelvin).
     * process temperature [K]: Temperature of the machine during production (in Kelvin).
     * Rotational speed [rpm]: Average RPM of the tool.
     * Torque [Nm]: Torque in Newton-meters.
     * Tool wear [min]: Minutes of wear on the tool.
     * machine failure: Indicates whether there was a failure.
     * TWF, HDF, PWF, OSF, RNF: Specific failure types.
 
 5) Further analysis (Optional)
     - You can use the extracted data for further analysis using python, such as:
       * Data visualisation using libraries like Matplotlib or Seaborn.
       * Statistical analysis using SciPy or smiliar packages.
       * Machine learning models to predict potentoial failes based on historical data

 6) Stopping the process:
     - if you need to stop the process before it completes you can use the Ctrl + C command in the terminal to terminate the script
   
## File Structure

Here is what the file strcture should look like:

project-directory/
│
├── db_utils.py        # Script for database operations and data extraction
├── credentials.yaml    # YAML file containing database credentials
├── failure_data.csv    # CSV file for extracted data
└── README.md           # Project documentation

## License 

This prohected is licensed under the MIT License. See the License file for details.

   
