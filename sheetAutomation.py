import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Ersetze durch deinen Service Account Key Pfad
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class GoogleSheetAutomation:
    def __init__(self):
        creds = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        self.service = build('sheets', 'v4', credentials=creds)

    def check_and_delete_rows(self, spreadsheet_id, sheet_name='Sheet1', range_='A1:A'):
        """
        Überprüft die erste Spalte einer Google Sheet und löscht Zeilen,
        bei denen die Uhrzeit in der ersten Zelle veraltet ist.
        Gibt die letzte Uhrzeit zurück, die nicht gelöscht wurde.
    
        Args:
            spreadsheet_id (str): Die ID der Google Sheet.
            sheet_name (str, optional): Der Name des Sheets (z.B. 'Sheet1'). Defaults to 'Sheet1'.
            range_ (str, optional): Der Bereich, der überprüft werden soll. Defaults to 'A1:A'.
    
        Returns:
            str: Die letzte verbleibende Uhrzeit, die nicht gelöscht wurde, oder None, wenn keine gültigen Einträge verbleiben.
        """
        try:
            # 1. Get the sheet ID (integer) from the sheet name:
            sheet_metadata = self.service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
            sheets = sheet_metadata.get('sheets', '')
            sheet_id = None
            for sheet in sheets:
                title = sheet.get("properties", {}).get("title", "")
                if title == sheet_name:
                    sheet_id = sheet.get("properties", {}).get("sheetId", 0)
                    break
    
            if sheet_id is None:
                raise ValueError(f"Sheet with name '{sheet_name}' not found!")
    
            # 2. Get the data from the sheet:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_
            ).execute()
            values = result.get('values', [])
    
            if not values:
                print(f"Keine Daten in der angegebenen Spalte gefunden: {range_}")
                return None
    
            rows_to_delete = []
    
            for row, row_values in enumerate(values, start=1):
                if row_values and len(row_values) > 0:
                    timestamp_str = row_values[0]
                    try:
                        timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')
                        if timestamp < datetime.datetime.now():
                            rows_to_delete.append(row)
                    except ValueError:
                        print(f"Ungültiges Datumsformat in Zeile {row}: {timestamp_str}")
    
            if rows_to_delete:
                requests = []
                for row in rows_to_delete:  # Reihenfolge beibehalten!
                    requests.append({
                        'deleteDimension': {
                            'range': {
                                'sheetId': sheet_id,
                                'dimension': 'ROWS',
                                'startIndex': row - 1,
                                'endIndex': row
                            }
                        }
                    })
    
                body = {'requests': requests}
                self.service.spreadsheets().batchUpdate(
                    spreadsheetId=spreadsheet_id, body=body
                ).execute()
                print(f"Folgende Zeilen wurden gelöscht: {rows_to_delete}")
            else:
                print("Keine veralteten Einträge zum Löschen gefunden.")
    
            # 3. Abrufen der verbleibenden Daten, um die letzte gültige Uhrzeit zu finden
            result_after_delete = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_
            ).execute()
            remaining_values = result_after_delete.get('values', [])
    
            if remaining_values:
                # Die erste verbleibende Uhrzeit zurückgeben
                return remaining_values[0][0]
            else:
                print("Keine verbleibenden Einträge nach dem Löschen.")
                return None
    
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return None


if __name__ == "__main__":
    sheet_automation = GoogleSheetAutomation()
    spreadsheet_id = '1xFt4y2wLT8P19oEdFuDHrKtUpwWLLBYXcIXNvgpBq3k'  # Ersetze durch deine Sheet-ID
    last_valid_time = sheet_automation.check_and_delete_rows(spreadsheet_id, sheet_name='rain_schedule')
    print(f"Letzte gültige Uhrzeit: {last_valid_time}")