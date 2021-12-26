from fyers_api import fyersModel
from fyers_api import accessToken

client_id = "8LODKCYPOR-100"  # "XA02959"
secret_key = "2U6TZMM40W"
redirect_uri = "http://127.0.0.1:5000/login"

session = accessToken.SessionModel(client_id=client_id,
                                   secret_key=secret_key, redirect_uri=redirect_uri,
                                   response_type="code", grant_type="authorization_code")
# res = session.generate_authcode()
#
# print(res)


auth_code = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2NDA0MTExOTQsImV4cCI6MTY0MDQ0MTE5NCwibmJmIjoxNjQwNDEwNTk0LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImF1dGhfY29kZSIsImRpc3BsYXlfbmFtZSI6IlhBMDI5NTkiLCJub25jZSI6IiIsImFwcF9pZCI6IjhMT0RLQ1lQT1IiLCJ1dWlkIjoiZGFlNGU3NjZmZjJkNGJiMzgwMzhmMGQ0MDVkZDhkZjYiLCJpcEFkZHIiOiIxMDYuMjEyLjEyNi4xNDciLCJzY29wZSI6IiJ9.QZuNpO9TZiMgL_WR_MwW7fqhNVRG-I66opnSIZ5TxyA"
session.set_token(auth_code)
response = session.generate_token()

# access_token = response["access_token"]
print(response)
