CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER,
    branch_id INTEGER,
    salary INTEGER,
    join_date DATE,
    resign_date DATE
);

CREATE TABLE IF NOT EXISTS timesheets (
    timesheet_id INTEGER,
    employee_id INTEGER,
    date DATE,
    checkin TEXT,
    checkout TEXT
);

CREATE TABLE IF NOT EXISTS salary_per_hour (
    year INTEGER,
    month INTEGER,
    branch_id INTEGER,
    salary_per_hour INTEGER
);