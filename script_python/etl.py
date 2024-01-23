import os
import sqlite3

import pandas as pd
import typer

DB_PATH = os.getenv("DB_PATH")
EMPLOYEES_FILE_PATH = os.getenv("EMPLOYEES_FILE_PATH")
TIMESHEETS_FILE_PATH = os.getenv("TIMESHEETS_FILE_PATH")

# Assuming that employees work 5 days a week, 8 hours per day.
# This is used for filling null values instead of using averages for a more consistent result.
DEFAULT_DAILY_MANHOUR = 8


def extract(employees_path: str = EMPLOYEES_FILE_PATH, timesheets_path: str = TIMESHEETS_FILE_PATH):
    """
    Extract data from CSV files.

    :param employees_path: Path to the employees CSV file.
    :param timesheets_path: Path to the timesheets CSV file.
    :return: Tuple of DataFrames (employees, timesheets).
    """
    employees_df = pd.read_csv(employees_path, parse_dates=["join_date", "resign_date"])
    employees_df = employees_df.rename(columns={"employe_id": "employee_id"})

    timesheets_df = pd.read_csv(timesheets_path, parse_dates=["date"])
    timesheets_df["checkin"] = pd.to_datetime(timesheets_df["checkin"], format="%H:%M:%S")
    timesheets_df["checkout"] = pd.to_datetime(timesheets_df["checkout"], format="%H:%M:%S")

    return employees_df, timesheets_df


def transform(employees_df, timesheets_df):
    """
    Transform the data.

    :param employees_df: DataFrame containing employee data.
    :param timesheets_df: DataFrame containing timesheets data.
    :return: Transformed DataFrame.
    """
    merged_df = timesheets_df.merge(employees_df, how="left", on="employee_id")

    # Removed data without a date.
    merged_df = merged_df.dropna(subset=["date"])

    merged_df["year"] = merged_df["date"].dt.year
    merged_df["month"] = merged_df["date"].dt.month

    # Get daily working hours
    merged_df["working_hours"] = (merged_df["checkout"] - merged_df["checkin"]).apply(
        lambda x: x.seconds // 3600
    )
    # Fill null working hours with default daily manhour
    merged_df["working_hours"] = merged_df["working_hours"].fillna(DEFAULT_DAILY_MANHOUR)

    result = (
        merged_df.groupby(["year", "month", "branch_id"])
        .agg({"salary": "sum", "working_hours": "sum"})
        .reset_index()
    )
    result["salary_per_hour"] = round(result["salary"] / result["working_hours"], 2)

    return result


def load(result, db_path: str = DB_PATH):
    """
    Load the data into a SQLite database.

    :param result: DataFrame with transformed data.
    :param db_path: Path to the SQLite database file.
    """
    conn = sqlite3.connect(db_path)
    result[["year", "month", "branch_id", "salary_per_hour"]].to_sql(
        name="salary_per_hour", con=conn, if_exists="append", index=False
    )
    conn.commit()
    conn.close()

def main(
    employees_path: str = typer.Argument(EMPLOYEES_FILE_PATH, help="Path to the employees CSV file."),
    timesheets_path: str = typer.Argument(TIMESHEETS_FILE_PATH, help="Path to the timesheets CSV file."),
    db_path: str = typer.Argument(DB_PATH, help="Path to the SQLite database file."),
):
    """
    CLI program for extracting, transforming, and loading data.

    :param employees_path: Path to the employees CSV file.
    :param timesheets_path: Path to the timesheets CSV file.
    :param db_path: Path to the SQLite database file.
    """
    typer.echo("Extracting data...")
    employees_df, timesheets_df = extract(employees_path, timesheets_path)

    typer.echo("Transforming data...")
    transformed_result = transform(employees_df, timesheets_df)

    typer.echo("Loading data into the database...")
    load(transformed_result, db_path)

    typer.echo("Process completed successfully.")


if __name__ == "__main__":
    typer.run(main)
