"""
Cullen Baker
October 27th, 2023
for Decryption Capital

Run the code here:
https://colab.research.google.com/drive/1PExlT0WPvO5WjUZGdTLay1Z92GDONE7s?usp=sharing

Get top 30 coin market cap list from coinmarketcap.com
Check if each coin is tradable on Coinbase, Kraken, and Gemini

Email Cullen Baker at cullen77401@gmail.com any questions/issues/troubleshooting
Feel free to make any changes as Zhe sees fit, just make sure to version up and comment what you changed

This code probably works better if you run it on your machine. 
If you know how, copy the code and run the python file on your computer.

Upgrades that would be cool to have:
- Compare new csv to an old csv and highlight any changes
- Run and automatically email Zhe the csv file + highlights
"""

import requests
import csv

# API key for coinmarketcap.com
# This is a free API key that any intern can generate
# If this key does not work, generate a new one at https://coinmarketcap.com/api/documentation/v1/
API_KEY = "aa51b619-ee59-4bad-8386-51c6190cd550"


def coinbase_tradable(coin_symbol):
    base_url = "https://api.pro.coinbase.com"
    endpoint = "/products"

    # Make a GET request to the products endpoint to get the list of available trading pairs
    response = requests.get(f"{base_url}{endpoint}")
    products = response.json()

    # Check if the given coin symbol is in the list of tradable products
    for product in products:
        if product["id"] == f"{coin_symbol}-USD":
            return "Yes"  # Coin is tradable against USD on Coinbase Pro

    return "No"  # Coin is not tradable on Coinbase Pro


def kraken_tradable(coin_symbol):
    base_url = "https://api.kraken.com/0/public/AssetPairs"

    # Make a GET request to the AssetPairs endpoint to get the list of available trading pairs
    response = requests.get(base_url)
    data = response.json()

    # Check if the given coin symbol is in the list of tradable pairs
    for pair_name, pair_info in data["result"].items():
        if "USD" in pair_name and f"{coin_symbol}" in pair_name: 
            return "Yes"

    return "No"  # Coin is not tradable on Kraken


def gemini_tradable(coin_symbol):
    base_url = "https://api.gemini.com/v1/symbols"

    # Make a GET request to the symbols endpoint to get the list of available trading pairs
    response = requests.get(base_url)
    data = response.json()

    for symbol in data:
        if symbol == f"{coin_symbol.lower()}usd":
            return "Yes"

    return "No"  # Coin is not tradable on Gemini


def get_top_30():
    """
    Get top 30 coin market cap list from coinmarketcap.com
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    parameters = {
        'start':'1',
        'limit':'30',           # change this if you want more/less than 30 coins
        'convert':'USD'
        }
    
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
        }

    response = requests.get(url, params=parameters, headers=headers)
    content = response.json()
    data = content['data']
    for coin in data:
        print(coin['name'], "\nPrice:", round(coin['quote']['USD']['price'],2), "Market Cap", round(coin['quote']['USD']['market_cap']/1000000000,2), "1m % chng:", round(coin['quote']['USD']['percent_change_30d'],2), "\n")

    return data


def main():
    # Get the top 30 coins from coinmarketcap.com
    data = get_top_30()

    with open('top30.csv', 'w', newline='') as csvfile:
        # Create the headers for the csv file
        fieldnames = ['Name', 'Symbol', 'Market Cap ($B)', 'Price ($)', '1 Month Percent Change', "On Coinbase:", "On Kraken:", "On Gemini:"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # This writes all the data into the csv file
        for coin in data:
            # Try's in case there is an error with the exchange APIs
            try:
                cbt = coinbase_tradable(coin['symbol'])
            except Exception as e:
                cbt = "No"
                print(e)
            try:
                kt = kraken_tradable(coin['symbol'])
            except Exception as e:
                kt = "No"
                print(e)
            try:
                gt = gemini_tradable(coin['symbol'])
            except Exception as e:
                gt = "No"
                print(e)

            writer.writerow({'Name': coin['name'], 'Symbol': coin['symbol'], 'Market Cap ($B)': round(coin['quote']['USD']['market_cap']/1000000000,2), 
                             'Price ($)': round(coin['quote']['USD']['price'],2), '1 Month Percent Change': round(coin['quote']['USD']['percent_change_30d'],2),
                             'On Coinbase:': cbt, 'On Kraken:': kt, 'On Gemini:': gt})


if __name__ == "__main__":
    main()

