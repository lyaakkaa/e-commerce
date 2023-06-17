import requests


class HereService:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_coordinates(self, address) -> dict:
        url = f"https://geocode.search.hereapi.com/v1/geocode?q={address}&apikey=5QPrf-H2MNdWD-9df7pfd6ZNL13tKDj8cChJItf9EDE"
        response = requests.get(url)
        json = response.json()

        return {
            "location": {
                "latitude": json["items"][0]["position"]["lat"] if len(json["items"]) != 0 else 0.0,
                "longitude": json["items"][0]["position"]["lng"] if len(json["items"]) != 0 else 0.0,
            }
        }