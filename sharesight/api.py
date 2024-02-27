import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

def get_token(client_id, client_secret):
    token_url = "https://api.sharesight.com/oauth2/token"
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret)
    return token

def send_custom_price(access_token, investment_id, last_traded_price, last_traded_on):
    url = f"https://api.sharesight.com/api/v3/custom_investment/{investment_id}/prices.json"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"last_traded_price": last_traded_price, "last_traded_on": last_traded_on}
    response = requests.post(url, headers=headers, json=data)
    return response