#!/usr/bin/env python3
import requests
import os
import sys

# Provide the webhook URL that Discord generated
discord_webhook_url = os.getenv('DISCORD_SECRET')

if (discord_webhook_url is None) or (discord_webhook_url == ""):
    print("DISCORD_SECRET is empty")
    sys.exit(1)

api_key = os.getenv('COIN_SECRET')

if (api_key is None) or (api_key == ""):
    print("COIN_SECRET is empty!")
    sys.exit(1)


# Get the ETH price 
eth_price_url = 'https://www.worldcoinindex.com/apiservice/ticker?key=' + api_key + '&label=ethbtc&fiat=usd'  

data = requests.get(eth_price_url).json()
print(str(data))
price_in_usd = data['Markets'][0]['Price']

# Post the message to the Discord webhook
data = {
    "content": "ETH price is $" + str(price_in_usd) + " USD!"  
}

price_in_usd = str(price_in_usd).replace(',','')

if os.path.isfile('ath.eth') == False:
    f = open("ath.eth", "a")
    f.write("0")
    f.close()

f = open("ath.eth", "r+")

ath = f.read()

if ath == "":
    ath = "0"

if float(price_in_usd) > float(ath):
        print("ATH!!!")
        requests.post(discord_webhook_url, data=data)
        f.seek(0)
        f.write(price_in_usd)
else:
        print("Not an all time high")
        print("ATH recorded at " + str(ath))

f.close()
