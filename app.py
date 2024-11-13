import streamlit as st
import pandas as pd
import gspread
from serpapi import GoogleSearch
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
from os import getenv
from groq import Groq
MAX_LIMIT = 5
load_dotenv()

# Function to read the dataset
def read_dataset(file_path):
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format")

# Function to perform Google search
def google_search(query):
    params = {
        "engine": "google",
        "q": f"{query}",
        "api_key": getenv("SERP_API_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    # st.write(results["organic_results"])
    return results["organic_results"]

# Function to parse results using Groq
def parse_results(results, query):
    client = Groq()
    prompt = f"Extract relevant information for '{query}' from the following results:\n{results}"
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    st.write(completion.choices[0].message.content or "")
    return completion.choices[0].message.content or ""
    # for chunk in completion:
        # st.write(chunk.choices[0].delta.content or "", end="")

# Function to authenticate Google Sheets
def authenticate_google_sheets(credentials_json):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
    client = gspread.authorize(creds)
    return client

# Function to read data from Google Sheets
def read_google_sheet(client, sheet_name):
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# Streamlit app
st.title('AI Web Search Dashboard')
st.header('Upload CSV or Connect to Google Sheets')

# File uploader for CSV
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Google Sheets authentication
credentials_json = st.file_uploader("Upload Google Sheets API credentials JSON", type="json")
sheet_name = st.text_input("Enter Google Sheet name")

data = None

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.subheader('Uploaded CSV Data Preview')
    st.dataframe(data)
elif credentials_json is not None and sheet_name:
    client = authenticate_google_sheets(credentials_json)
    data = read_google_sheet(client, sheet_name)
    st.subheader('Google Sheets Data Preview')
    st.dataframe(data)

if data is not None:
    column = st.selectbox("Select the column for the query", data.columns)

prompt_input = st.text_input("Enter your custom prompt (use {entity} as a placeholder)")
st.write("Example: 'Find the latest news about {entity}'")

if data is not None and column and prompt_input:
    results = []
    for entity in range(min(len(data[column]), MAX_LIMIT)):
        search_query = f'{prompt_input} for {data[column][entity]}'#.replace(f"{entity}", data[column][entity])
        search_results = google_search(search_query)
        parsed_result = parse_results(search_results, search_query)
        results.append({'entity': data[column][entity], 'result': parsed_result})

    output_df = pd.DataFrame(results)
    st.subheader('Extracted Information')
    st.dataframe(output_df)
    
    output_file = 'output.csv'
    output_df.to_csv(output_file, index=False)
    # st.download_button(label="Download Results", data=output_file, file_name='output.csv', mime='text/csv')

