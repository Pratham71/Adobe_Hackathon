import requests


def api_request(link):
    response = requests.get(link)

    if response.status_code == 200:
        data = response.json()
        return((data["results"][0]["geometry"]['lat'],
                data["results"][0]["geometry"]['lng']))
    else:
        print("Error:", response.status_code)


def lat_long_convert(transactions):
    # Make a GET request to the API
    for i in transactions:
        PLACE = i[3]
        OPENCAGEDATA_KEY = "7c9e9348137d423180ab7c3b2db55f4e"
        link = f"https://api.opencagedata.com/geocode/v1/json?q={PLACE}&key={OPENCAGEDATA_KEY}"
        i[3] = api_request(link)
    return transactions
