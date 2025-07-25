'''
Uses google sheet API to extract character data

This is intended only for updating the char_data.csv file

Thus the imports are not necessary for running the rest of the program for the end-user
'''

import csv
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID and range of the char data spreadsheet.
SPREADSHEET_ID = "1N3TNTE4pn3dSxt0b4XWMjVVjcfISM1pYjj03lZVBBss"
RANGE_NAME = "data!A1:AC"

# Credentials path
PATH = os.getcwd() + "\\sheet_credentials.json"
# Token path
TOKEN_PATH = os.getcwd() + "\\token.json"
# csv path
CSV_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                        'char_data.csv')


def fetch_sheet_data():
  """Basic usage of the Sheets API.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(TOKEN_PATH):
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      try:
        creds.refresh(Request())
      except:
        os.remove(TOKEN_PATH)
        print("\nCredentials failed to refresh. token.json deleted. Please run again.")
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          PATH, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(TOKEN_PATH, "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    return values

  except HttpError as err:
    print(err)

def create_csv_from_sheet():
  data = fetch_sheet_data()
  
  print("\n SHEET DATA FETCHED SUCCESSFULLY \n")
  
  with open(CSV_PATH, 'w', newline='') as csvf:
    writer = csv.writer(csvf)
    writer.writerows(data)
    
  print("\n CSV UPDATED SUCCESSFULLY \n")
    
def main():
  create_csv_from_sheet()

if __name__ == "__main__":
  main()