import requests
import os
import json
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import scrolledtext, messagebox

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
def get_report_and_display():
    # Get the raid code from the entry widget
    raid_code = raid_code_entry.get()
    
    # Retrieve the raid report data
    raid_report_response = get_raid_report(raid_code)
    
    if raid_report_response:
        # Format the raid report data
        formatted_report = format_raid_report(raid_report_response)
        
        # Clear the text area and display the formatted report
        report_text_area.delete("1.0", tk.END)
        report_text_area.insert(tk.END, formatted_report)
    else:
        # Display an error message if retrieval fails
        messagebox.showerror("Error", "Failed to retrieve raid report data.")

"""def count_wipes_per_boss(response):
    wipes_count = {}

    if "errors" in response:
        print("Error:", response["errors"])
        return wipes_count
    
    report = response["data"]["reportData"]["report"]
    
    for fight in report["fights"]:
        if fight.get("boss"):  # Check if it's a boss fight
            boss_name = fight["name"]
            if boss_name not in wipes_count:
                wipes_count[boss_name] = 0
            
            for event in fight["events"]:
                # Check for events indicating a wipe
                if event["type"] == "death" and event["sourceID"] in report["friendlies"]:
                    # If a player died, check if it's a group wipe
                    if all(death["type"] == "wipe" for death in event["additionalDeaths"]):
                        wipes_count[boss_name] += 1
                        
    return wipes_count

def plot_wipes_per_boss(wipes_count):
    bosses = list(wipes_count.keys())
    wipes = list(wipes_count.values())
    print("Bosses:", bosses)
    print("Wipes:", wipes)v
    plt.figure(figsize=(10, 6))
    plt.bar(bosses, wipes, color='skyblue')
    plt.xlabel('Boss')
    plt.ylabel('Number of Wipes')
    plt.title('Number of Wipes for Each Boss Encounter')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()"""
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
    #wipes_count_per_boss = count_wipes_per_boss(raid_report_response)
    #plot_wipes_per_boss(wipes_count_per_boss)
if __name__ == "__main__": main()
root = tk.Tk()
root.title("Warcraft Logs Raid Report Viewer")

# Create a frame to hold the entry widget and button
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Create an entry widget to input the raid code
raid_code_label = tk.Label(input_frame, text="Enter Raid Code:")
raid_code_label.grid(row=0, column=0, padx=10)

raid_code_entry = tk.Entry(input_frame, width=20)
raid_code_entry.grid(row=0, column=1, padx=10)

# Create a button to fetch and display the raid report
fetch_button = tk.Button(input_frame, text="Fetch Report", command=get_report_and_display)
fetch_button.grid(row=0, column=2, padx=10)

# Create a scrolled text widget to display the raid report
report_text_area = scrolledtext.ScrolledText(root, width=80, height=30, wrap=tk.WORD)
report_text_area.pack(padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()