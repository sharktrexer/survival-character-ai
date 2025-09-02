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
# cur path
CUR_PATH = os.path.dirname(os.path.realpath(__file__))

def fetch_sheet_data(sheet_range:str):
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
        .get(spreadsheetId=SPREADSHEET_ID, range=sheet_range)
        .execute()
    )
    values = result.get("values", [])

    if not values:
      print("No data found.")
      return

    return values

  except HttpError as err:
    print(err)

def create_csv_from_sheet(path:str, sheet_range:str):
  data = fetch_sheet_data(sheet_range)
  
  print("\n SHEET DATA FETCHED SUCCESSFULLY \n")
  
  path = os.path.join(CUR_PATH, path)
  
  with open(path, 'w', newline='') as csvf:
    writer = csv.writer(csvf)
    writer.writerows(data)
    
  print("\n CSV UPDATED SUCCESSFULLY \n")
    
def main():
  # Obtain character stat data
  char_stats_path = 'char_data.csv'
  char_stats_range = "data!A1:AC"
  create_csv_from_sheet(char_stats_path, char_stats_range)
  
  # Obtain character title & descs
  char_desc_path = 'char_desc.csv'
  char_desc_range = "desc!A1:C"
  create_csv_from_sheet(char_desc_path, char_desc_range)
  
  # Obtain character's magic types
  char_magic_path = 'char_magic.csv'
  char_magic_range = "magics!A1:D"
  create_csv_from_sheet(char_magic_path, char_magic_range)

if __name__ == "__main__":
  main()