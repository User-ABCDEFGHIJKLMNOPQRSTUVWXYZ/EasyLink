import requests
import base64
import os
from datetime import datetime

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

TRACKS = {
    "Blinding Lights": "0VjIjW4GlUZAMYd2vXMi3b",
    "Levitating": "463CkQjx2Zk1yXoBuierM9",
    "Stay": "5HCyWlXZPP0y6Gqq8TgA20"
}

def get_access_token():
    auth = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_b64 = base64.b64encode(auth.encode()).decode()

    res = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={"grant_type": "client_credentials"}
    )
    return res.json()["access_token"]

def get_track_data(token, track_id):
    res = requests.get(
        f"https://api.spotify.com/v1/tracks/{track_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    return res.json()

def main():
    token = get_access_token()
    rows = []

    for name, track_id in TRACKS.items():
        data = get_track_data(token, track_id)
        plays = f"{data['popularity']}% popularity"
        artist = data["artists"][0]["name"]

        rows.append(f"| — | {name} | {artist} | auto | {plays} | [Spotify](https://open.spotify.com/track/{track_id}) |")

    with open("Spotify-Music.md", "w") as f:
        f.write(f"""# 🎧 Spotify Music Hub

_Last updated: {datetime.utcnow().strftime('%Y-%m-%d')}_

## 🔥 Top Tracks

| Rank | Track | Artist | Weeks on Chart | Total Plays | Listen |
|------|-------|--------|----------------|-------------|--------|
{chr(10).join(rows)}

---
_This file is automatically updated using GitHub Actions and the Spotify API._
""")

if __name__ == "__main__":
    main()
