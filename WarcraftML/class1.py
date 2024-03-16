import requests
import os
import json

clientId = "9b8b018d-77bc-4af6-8965-cc422d67be58"
secretId= "G4VH4kaXL1UCat7mp3Uxjy26UJ76fRK5meJ7Rc46"
tokenURL = "https://www.warcraftlogs.com/oauth/token"
publicURL = "https://www.warcraftlogs.com/api/v2/client"

def get_token(store: bool = True):
    data = {"grant_type":"client_credentials"}
    auth = (clientId, secretId)
    with requests.Session() as session:
        response = session.post(tokenURL, data = data, auth = auth)
    if store and response.status_code == 200:
        store_token(response)
    return response
    

def read_token():
    try:
        with open(".credentials.json", mode= "r+", encoding = "utf-8") as f:
            access_token= json.load(f)
        return access_token.get("access_token")
    except OSError as e:
        print(e)
        return None

def store_token(response):
    try:
        with open(".credentials.json", mode="w", encoding="utf-8") as f:
            json.dump({"access_token": response.json()["access_token"]}, f)
    except OSError as e:
        print(e)
        return None

def retrieve_headers() -> dict[str,str]: 
    return {"Authorization": f"Bearer {read_token()}"}



def get_raid_report(code):
    query = """query GetRaidReport($code: String!) {
      reportData {
        report(code: $code) {
          code
          title
          owner {
            name
          }
          startTime
          endTime
          zone {
            name
          }
          fights {
            id
            name
            startTime
            endTime
            encounterID
          }
        }
      }
    }"""
    
    variables = {"code": code}
    response = get_data(query, **variables)
    return response
def format_raid_report(response):
    if "errors" in response:
        print("Error:", response["errors"])
        return
    
    report = response["data"]["reportData"]["report"]
    boss_encounters = {
    "Lord Marrowgar",
    "Lady Deathwhisper",
    "Icecrown Gunship Battle",
    "Deathbringer Saurfang",
    "Festergut",
    "Rotface",
    "Professor Putricide",
    "Blood Prince Council",
    "Blood-Queen Lana'thel",
    "Valithria Dreamwalker",
    "Sindragosa",
    "The Lich King",
    "Halion"
    }
    print("Raid Report Details:")
    print(f"Code: {report['code']}")
    print(f"Title: {report['title']}")
    print(f"Owner: {report['owner']['name']}")
    print(f"Start Time: {report['startTime']}")
    print(f"End Time: {report['endTime']}")
    print(f"Zone: {report['zone']['name']}")
    print("Fights:")
    for fight in report["fights"]:
        print(f"- Fight ID: {fight['id']}")
        print(f"  Fight Name: {fight['name']}")
        print(f"  Start Time: {fight['startTime']}")
        print(f"  End Time: {fight['endTime']}")
        encounter = fight.get("encounterID")
        if isinstance(encounter, dict) and fight["name"] in boss_encounters:
             print(f"- Boss Kill: {fight['name']} (Fight ID: {fight['id']})")
        elif fight["name"] in boss_encounters:
            print(f"- Boss Kill: {fight['name']} (Fight ID: {fight['id']})")
        else:
            print(f"- Non-Boss Fight: {fight['name']} (Fight ID: {fight['id']})")
def get_data(query: str, **kwargs):
    """Fetches data from wclogs public API. Please provide a query and the parameters."""
    data = {"query": query, "variables": kwargs}
    headers = {"Content-Type": "application/json", **retrieve_headers()}
    
    with requests.Session() as session:
        response = session.post(publicURL, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

def main():
    response = get_token()
    store_token(response)
    #print(response.json())
    token = read_token()
    #print(token)
    #response1 = get_data(query, code ="LPmp4tAvZc78kyw6")
    #print(response1)
    raid_report_response = get_raid_report("2RngATHaBQpd3Y4b")
    format_raid_report(raid_report_response)
if __name__ == "__main__": main()