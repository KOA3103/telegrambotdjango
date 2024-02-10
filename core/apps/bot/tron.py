import requests


def get_hash_detail_information(hash, api_key):
    base_url = "https://apilist.tronscan.org/api"
    endpoint = f"/transaction-info?"
    params = {
        "hash": hash,  # Your transaction hash here.
        "api_key": api_key,  # Include your Tronscan API key here
    }
    try:
        response = requests.get(base_url + endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to fetch Data. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as err:
        print("Error:", err)
        return None
