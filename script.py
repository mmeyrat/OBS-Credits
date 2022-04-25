import requests
from config import *

streamer_id = "433976821"

header = {"Client-ID": client_id, "Authorization": f"Bearer {auth_token}"}
response = requests.get(f"https://api.twitch.tv/helix/users/follows?to_id={streamer_id}", headers = header)
data = response.json()

for r in data["data"]:
    print(r["from_name"])
