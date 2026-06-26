import sqlite3
import pandas as pd

# Create/connect to database
connect = sqlite3.connect("hospital.db")

# Read CSV files
patients = pd.read_csv("patients.csv")
doctors = pd.read_csv("doctors_schedule.csv")

# Create tables
patients.to_sql(
    "patients",
    connect,
    if_exists="replace",
    index=False
)

doctors.to_sql(
    "doctor_schedule",
    connect,
    if_exists="replace",
    index=False
)

connect.commit()
connect.close()

print("hospital.db created successfully!")