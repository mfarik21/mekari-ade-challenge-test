# Salary Perhour Challenge Test


## Overview

This are ETL solution to produce 

## Folder Structure

- **data:**
  - **employees.csv:** Contains data about employees.
  - **timesheet.csv:** Stores information related to employee timesheets.
- **database:** Used SQLite for a hassle-free setup, and separated it for Python and SQL solutions.
- **notebook:**
  - **python_solution.ipynb:** Jupyter notebook with step-by-step Python solutions.
  - **sql_solution.ipynb:** Jupyter notebook with step-by-step SQL solutions.
- **python_sql:** Source code files and scripts for the Python solution.
- **script_sql:** Source code files and scripts for the SQL solution.

## ETL Scripts

### 1. SQL

**DB Setup**
sqlite3 installation (on Ubuntu):

```bash
sudo apt-get update
sudo apt-get install sqlite3
```

Create Employees, Timesheet and Salary perhour:

```bash
#!/bin/bash

DB_PATH="database/sql_solution.db"
SETUP_FILE="script_sql/setup.sql"

# Run the SQL file with sqlite3
sqlite3 "$DB_PATH" < "$SETUP_FILE"

```

**Load CSV data to tables**

Load Employee CSV file:

```bash
#!/bin/bash

CSV_FILE="data/employees.csv"
TABLE_NAME="employees"

# Skip the first line in the CSV file and save the rest to a temporary file
tail -n +2 "$CSV_FILE" > "$CSV_FILE.tmp"

# Run the SQLite command to import the modified CSV file
sqlite3 "$DB_PATH" <<EOF
.mode csv
.import "$CSV_FILE.tmp" "$TABLE_NAME"
EOF

# Remove the temporary file
rm "$CSV_FILE.tmp"
```

Load Timesheet CSV file:

```bash
#!/bin/bash

CSV_FILE="data/timesheets.csv"
TABLE_NAME="timesheets"

tail -n +2 "$CSV_FILE" > "$CSV_FILE.tmp"

sqlite3 "$DB_PATH" <<EOF
.mode csv
.import "$CSV_FILE.tmp" "$TABLE_NAME"
EOF

rm "$CSV_FILE.tmp"
```

**Runing the Script**

```bash
#!/bin/bash

ETL_FILE="script_sql/etl.sql"

sqlite3 "$DB_PATH" < "$ETL_FILE"

```

**Running a Query**
```bash
#!/bin/bash

sqlite3 "$DB_PATH" "SELECT * FROM salary_per_hour;"
```

### 2. Python


**Installation**

Make sure you have Python installed, and then install the required dependencies:

```bash
pip install -r requirements.txt
```

**Running the CLI Program**

```bash
python etl_script.py [OPTIONS] EMPLOYEES_PATH TIMESHEETS_PATH DATABASE_PATH
```

- EMPLOYEES_PATH: Path to the employees CSV file.
- TIMESHEETS_PATH: Path to the timesheets CSV file.
- DATABASE_PATH: Path to the SQLite database file.

This will extract data from employees.csv and timesheets.csv, transform the data, and load it into the SQLite database mydatabase.db.

**Example**

```bash
python script_python/etl.py data/employees.csv data/timesheets.csv database/python_solution.db
```


## Notebooks

For experimental purposes, the project includes step-by-step and interactive solutions for both Python and SQL approaches in Jupyter notebooks. To run them, you need to install Jupyter Notebook and the following libraries in the Conda shell (for Linux): `ipython-sql` and `sqlite3`.

