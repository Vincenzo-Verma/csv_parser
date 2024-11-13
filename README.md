# CSV PARSER

## Project Description
The CSV PARSER is a Streamlit application that allows users to upload a CSV file or connect to a Google Sheet, perform web searches for each entity in a selected column, and extract relevant information using Groq's LLM. The results are displayed in a user-friendly table format and can be downloaded as a CSV file.

---

## Features
- Upload CSV files or connect to Google Sheets for data input.
- Perform web searches using SerpAPI.
- Extract relevant information using Groq's LLM.
- Display extracted information in a table format.
- Download the results as a CSV file.

---

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- Streamlit
- Pandas
- Gspread
- OAuth2Client
- SerpAPI
- Groq API Client
- Google API Client
- Dotenv

---

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/web-parser.git
   cd csv-parser
   ```
2. Install required libraries:
   ```
   pip install -r requirements.txt
   ```
3. Setup Environment Variables:
   - Move/Rename the `.env_example` file to `.env` and put the respected API keys.
   ```
   mv .env_example .env
   ```
---

### Code Executionn
 - Run the streamlit file
   ```
   streamlit run app.py
   ```
