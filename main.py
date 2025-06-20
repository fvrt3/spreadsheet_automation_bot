# main.py
import pandas as pd
import os
import glob
from utils import detect_columns, clean_data, email_output, log_summary

# Create an output and summary folder if none is found
os.makedirs("output", exist_ok=True) 
os.makedirs("summary", exist_ok=True)

# Flag to toggle attachment of logs (set to False to email only the spreadsheets)
INCLUDE_LOGS = True

# Define supported data types
data_types = ["input/*.csv", "input/*.xlsx", "input/*.tsv"]

# Get files for supported data files
data_files = []
for type in data_types:
    data_files.extend(glob.glob(type))

if not data_files:
    raise FileNotFoundError("No supported files were found in ..input/")

# Clean and email
output_files = []
log_files = []
for file in data_files:
    print(f"\nProcessing file: {file}")
    ext = os.path.splitext(file)[1].lower()

    # Load based on data file extension
    if ext == ".csv":
        df = pd.read_csv(file)
    elif ext == ".xlsx":
        df = pd.read_excel(file)
    elif ext == ".tsv":
        df = pd.read_csv(file, sep="\t")
    else:
        print(f"Skipping unsupported file: {file}")
        continue

    # Detect key columns (e.g. Date, Name, Amount, etc.)
    column_map = detect_columns(df.columns.tolist())
    print("Detected columns:", column_map)

    # Data cleaning
    df_clean = clean_data(df, column_map)

    # Save output
    filename = os.path.splitext(os.path.basename(file))[0]
    output_path = f"output/cleaned_{filename}.csv"
    df_clean.to_csv(output_path, index=False)
    print(f"Saved cleaned file: {filename}")
    output_files.append(output_path)

    # Save summary log
    if INCLUDE_LOGS:
        log_path = f"summary/log_{filename}.txt"
        log_summary(
            log_path = log_path,
            file_name=filename,
            column_map=column_map,
            original_rows=len(df),
            cleaned_rows=len(df_clean)
        )
        log_files.append(log_path)

# Email the output
email_output(
    to_email="hurriedturtle83@gmail.com",
    subject=f"Automated Report",
    body="Hello,\n\nPlease find the cleaned data files attached.\n\nRegards,\nAutomation Bot",
    attachment_paths = output_files + log_files if INCLUDE_LOGS else output_files
)