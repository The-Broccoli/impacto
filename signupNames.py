import requests
import json


class SignupNames():

    def get_signup_names(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                names = []
                for signup in data.get('signUps', []):
                    names.append(signup.get('name'))
                # Namen alphabetisch sortieren (case-insensitive)
                names.sort(key=str.lower)
                return names
                
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Abrufen der Daten: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"Fehler beim Verarbeiten der JSON-Daten: {e}")
            return []
            
    def get_signup_data(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                users = {}
                for signup in data.get('signUps', []):
                    user_id = signup.get('userId')
                    if user_id:
                        users[user_id] = {
                            "name": signup.get('name'),
                            "className": signup.get('className')
                        }
                title = data.get('title', [])
                return users, title
            
        except requests.exceptions.RequestException as e:
            print(f"Fehler beim Abrufen der Daten: {e}")
            return {}, {}
        except json.JSONDecodeError as e:
            print(f"Fehler beim Verarbeiten der JSON-Daten: {e}")
            return {}, {}
            
            
# test1, test2 = SignupNames().get_signup_data('https://raid-helper.dev/api/v2/events/1312455017525022801')
# print(test2)