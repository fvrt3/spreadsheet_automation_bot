# utils.py
from config import KEYWORDS
import pandas as pd
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load .env file for email credentials
load_dotenv()

# Auto-detect important featuers (can be customized by KEYWORDS in config.py and DISPATCH below)
def detect_columns(columns):
    detected = {key: None for key in KEYWORDS}

    for col in columns:
        col_lower = col.lower()
        for key, key_set in KEYWORDS.items():
            if any (k in col_lower for k in key_set) and not detected[key]:
                detected[key] = col
        
    return detected

# Clean important features
def clean_date_column(df, col):
    df[col] = pd.to_datetime(df[col], errors='coerce')

    return df

def clean_amount_column(df, col):
    df[col] = pd.to_numeric(df[col], errors='coerce')

    return df.dropna(subset=[col])

def clean_price_column(df, col):
    df[col] = pd.to_numeric(df[col], errors='coerce')

    return df.dropna(subset=[col])

def clean_name_column(df, col):
    df[col] = df[col].astype(str).str.strip().str.title()

    return df[df[col].notna() & (df[col] != '')]

# Custom cleaning logic dispatch
DISPATCH = {
    'date': clean_date_column,
    'amount': clean_amount_column,
    'price': clean_price_column,
    'name': clean_name_column,
}

# Cleaning controller
def clean_data(df, column_map):
    df = df.copy()
    for key, col in column_map.items():
        if col and col in df.columns and key in DISPATCH:
            df = DISPATCH[key](df, col)

    df = df.dropna(how='all').drop_duplicates()

    return df

# Summary logger for cleaning
def log_summary(log_path, file_name, column_map, original_rows, cleaned_rows):
    with open(log_path, "a") as log_file:
        log_file.write(f"\n--- {file_name} ---\n")
        log_file.write("Detected columns:\n")
        for key, col in column_map.items():
            log_file.write(f"   {key}: {col}\n")
        log_file.write(f"Rows before cleaning: {original_rows}\n")
        log_file.write(f"Rows after cleaning:  {cleaned_rows}\n")
        log_file.write(f"Rows removed:         {original_rows - cleaned_rows}\n")
        log_file.write(f"{'-'*40}\n")

# Automatically email the results
def email_output(
    to_email,
    subject,
    body,
    attachment_paths,
    smtp_server='smtp.gmail.com',
    smtp_port=587
):
    # Load credentials from .env
    email_user = os.getenv('EMAIL_USER')
    email_pass = os.getenv('EMAIL_PASS')

    if not email_user or not email_pass:
        raise ValueError("Email credentials not set in environment variables. \nLocally save the email credentials in a .env")
    
    # Create email
    msg = EmailMessage()
    msg['From'] = email_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body)

    # Attach file
    for path in attachment_paths:
        with open(path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(path)
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
        
    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as smtp:
        smtp.starttls()
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)

    # Confirm completion
    print(f"Successfully sent email with {len(attachment_paths)} attachments to {to_email}")