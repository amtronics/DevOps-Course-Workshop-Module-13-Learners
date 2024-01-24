import os
import pyodbc
import urllib.parse

valid_drivers = ['ODBC Driver 17 for SQL Server']
driver = next((driver for driver in pyodbc.drivers() if driver in valid_drivers), pyodbc.drivers()[-1])
connect_string = f"Driver={{{driver}}};Server=tcp:{os.environ.get('DB_SERVER_NAME')},1433;Database={os.environ.get('DATABASE_NAME')};Uid={os.environ.get('DATABASE_USER')};Pwd={os.environ.get('DATABASE_PASSWORD')};Encrypt=yes;TrustServerCertificate=Yes;Connection Timeout=30;"
url_encoded_connect_string = urllib.parse.quote_plus(connect_string)

class Config:
    SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc:///?odbc_connect={url_encoded_connect_string}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULED_JOB_INTERVAL_SECONDS = int(os.environ.get('SCHEDULED_JOB_INTERVAL_SECONDS'))
    FINANCE_PACKAGE_URL = os.environ.get('FINANCE_PACKAGE_URL')