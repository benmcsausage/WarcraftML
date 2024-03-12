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
    
def store_token(response):
    try:
        with open(".credentials.json", mode= "w", encoding= "utf-8") as f:
            json.dump(response.json(), f)
    except OSError as e:
        print(e)
        return None

def read_token():
    try:
        with open(".credentials.json", mode= "r+", encoding = "utf-8") as f:
            access_token= json.load(f)
        return access_token.get("access_token")
    except OSError as e:
        print(e)
        return None

def retrieve_headers() -> dict[str,str]: 
    return {"Authorization": f"Bearer{read_token()}"}

query = """query($code:String){
            reportData{
                report(code:$code){
                fights(difficulty:3){
                    id
                    name
                    startTime
                    endTime
                    }}}}"""
def get_data(query: str, **kwargs):
    """Fetches data from wclogs public API. Please provide a query and the parameters."""
    data = {"query": query, "variables":kwargs}
    with requests.Session() as session:
        session.headers = retrieve_headers()
        response = session.get(publicURL,json = data)
        return response.json()

def main():
    #response = get_token()
    #print(response.json())
    #token = read_token()
    #print(token)
    response = get_data(query, code ="LPmp4tAvZc78kyw6")
    print(response)
if __name__ == "__main__": main()