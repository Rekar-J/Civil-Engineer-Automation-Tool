import pandas as pd
import os

# Initialize database if it doesn't exist
def initialize_database():
    if not os.path.exists("database.csv"):
        pd.DataFrame(columns=["Uploaded File", "Type"]).to_csv("database.csv", index=False)

# Load the database into a DataFrame
def load_database():
    initialize_database()
    return pd.read_csv("database.csv")

# Save a new record to the database
def save_to_database(file_name, file_type):
    db = load_database()
    new_entry = pd.DataFrame({"Uploaded File": [file_name], "Type": [file_type]})
    updated_db = pd.concat([db, new_entry], ignore_index=True)
    updated_db.to_csv("database.csv", index=False)

# Delete a record from the database
def delete_from_database(file_name):
    db = load_database()
    updated_db = db[db["Uploaded File"] != file_name]
    updated_db.to_csv("database.csv", index=False)
