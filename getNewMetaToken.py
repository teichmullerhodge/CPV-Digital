import requests

# Replace these placeholders with your actual values
graph_api_version = "v18.0" 
app_id = <APP_ID>
app_secret = <APP_SECRET_KEY>
your_access_token = <GRAPH_API_TOKEN>

url = f"https://graph.facebook.com/{graph_api_version}/oauth/access_token"

params = {
    "grant_type": "fb_exchange_token",
    "client_id": app_id,
    "client_secret": app_secret,
    "fb_exchange_token": your_access_token
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    access_token = data.get("access_token")
    print(f"Access Token: {access_token}")
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
