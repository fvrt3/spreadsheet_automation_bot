# Spreadsheet Automation Bot

A Python-based automation tool that reads spreadsheet files, cleans and standardizes the data, and emails the cleaned reports. Built for freelancers, data analysts, and small business workflows.

## Features
- Auto-detects key fields (Date, Name, Amount, Price)
- Cleans messy data with custom logic for each field
- Supports `.csv`, `.tsv`, and `.xlsx` input formats
- Outputs standardized `.csv` files and log summaries
- Emails final reports and logs as attachments

## Technologies
- Python 3.x
- pandas
- openpyxl (for Excel support)
- python-dotenv (for secure credential handling)
- smtplib / email (for emailing reports)

## Project Structure
```
.
├── input/               # Raw spreadsheet files
├── output/              # Cleaned CSVs and log files
├── config.py            # Keyword mapping for column detection
├── utils.py             # All logic: cleaning, detection, email, logging
├── main.py              # Orchestrates the workflow
├── .env                 # Stores email credentials (not committed)
├── .gitignore           # Prevents sensitive and bulky files from being tracked
├── LICENSE              # MIT License
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/fvrt3/spreadsheet_automation_bot.git
   cd spreadsheet-automation-bot
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your Gmail credentials:
   ```env
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_app_password
   ```

> Note: You must use a Gmail App Password if 2FA is enabled.

## ⚙️ Usage
1. Place one or more `.csv`, `.tsv`, or `.xlsx` files in the `input/` folder.
2. Run the bot:
   ```bash
   python main.py
   ```
3. Cleaned files and logs will appear in `output/`.
4. An email with all attachments will be sent to the configured recipient.

## 📄 License
This project is licensed under the [MIT License](LICENSE).

## 🙌 Credits
Created by fvrt3

---

Feel free to fork, contribute, or adapt it for your own use.
