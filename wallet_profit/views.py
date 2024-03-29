from django.shortcuts import render
import requests
import json

static_token = ""



all_coins = ['BTC', 'ETH', 'LTC', 'XRP', 'BCH', 'BNB', 'EOS', 'XLM', 'ETC', 'TRX', 'DOGE', 'UNI', 'DAI', 'LINK', 'DOT', 'AAVE', 'ADA', 'SHIB', 'FTM', 'MATIC', 'AXS', 'MANA', 'SAND', 'AVAX', 'MKR', 'GMT', 'USDC', 'BTC', 'ETH', 'LTC', 'XRP', 'BCH', 'BNB', 'EOS', 'XLM', 'ETC', 'TRX', 'PMN', 'DOGE', 'UNI', 'DAI', 'LINK', 'DOT', 'AAVE', 'ADA', 'SHIB', 'FTM', 'MATIC', 'AXS', 'MANA', 'SAND', 'AVAX', 'MKR', 'GMT', 'USDC']
# coins = ['BTC', 'ETH', 'LTC', 'XRP', 'BNB', 'ETC', 'TRX', 'DOGE', 'DAI', 'ADA', 'SHIB', 'AXS', 'MANA', 'SAND', 'AVAX', 'USDC']
coins = ['BTC', 'TRX', 'LTC', 'DOGE']

def format_float(number):
    # Format the number to up to 8 decimal places
    formatted_number = "{:.5f}".format(number)
    # Remove trailing zeros
    formatted_number = formatted_number.rstrip('0').rstrip('.')
    return float(formatted_number)

def display_number(request):
    if request.method == 'POST':

        token = request.POST.get('token', 0)
        

        static_token = token
        available_coins, total_asset = fill_chart2(token)

        
        return render(request, 'wallet.html', {'tr_data': available_coins, 'total_asset' : format_float(total_asset),'static_token' : static_token})
        

        
    else:
        return render(request, 'wallet.html', {'number': 0})


def fill_chart(token):
    global coins

    url = 'https://api.nobitex.ir/users/wallets/balance'
    headers = {
        "Authorization": f"Token {token}"
    }
    data = {
        "currency": "btc"
    }

    id_tracker = 0
    available_coins = []

    for c in coins:
        data['currency'] = c.lower()
        response = requests.post(url, headers=headers, json=data)
        if float(response.json()['balance']) != 0:
            last_price = requests.get(f'https://api.nobitex.ir/v2/orderbook/{c.upper()}USDT')

            if response.status_code == 200 and float(response.json()['balance']) != 0 and last_price.status_code == 200:
                available_coins.append({'id' : id_tracker, 'coin' : c.upper(), 'balance' : float(response.json()['balance']), 'priceusdt' : float(last_price.json()['lastTradePrice']), 'asset' : float(float(response.json()['balance']) * float(last_price.json()['lastTradePrice'])),'image' : f'{c.lower()}.svg'})
                id_tracker += 1
                    
    available_coins = sorted(available_coins, key=lambda d: d['balance'], reverse=True)
    return available_coins

def fill_chart2(token):
    available_coins = []
    total_asset = 0

    usdt_url = 'https://api.nobitex.ir/users/wallets/balance'
    usdt_headers = {
        'Authorization': 'Token d8f40b150de96d3557dba79481f42b9cdfdc4a1c',
    }
    usdt_data = {
        'currency': 'usdt'
    }
    usdt_response = requests.post(usdt_url, headers=usdt_headers, data=usdt_data).json()['balance']
    total_asset+= float(usdt_response)
    available_coins.append({'id' : 0, 'coin' : "USDT", 'balance' : format_float(float(usdt_response)), 'priceusdt' : 1, 'asset' : format_float(float(usdt_response)), 'image' : f'{"usdt".lower()}.svg'})



    url = 'https://api.nobitex.ir/users/wallets/list'
    headers = {
        'Authorization': f'Token {token}'
    }
    response = requests.get(url, headers=headers).json()

    id_tracker = 1

    wallet_count = int(len(response['wallets']))
    for i in range(wallet_count):

        item = response['wallets'][i]

        currency_name = str(item['currency'])
        

        if(float(item['balance']) != 0):
            if(currency_name.upper() == "RLS" or currency_name.upper() == "USDT"): continue
            last_price = requests.get(f'https://api.nobitex.ir/v2/orderbook/{currency_name.upper()}USDT').json()


            if item['currency'] == 'btc':
                url2 = 'https://api.nobitex.ir/users/wallets/transactions/list?wallet=' + str(item['id'])
                response2 = requests.get(url2, headers=headers).json()

                with open('testt.json', 'w') as outfile:
                    json.dump(response2, outfile, indent=4)

                


            available_coins.append({'id' : id_tracker, 'coin' : str(item['currency']).upper(), 'balance' : format_float(float(item['balance'])), 'priceusdt' : format_float(float(last_price['lastTradePrice'])), 'asset' : format_float(float(float(item['balance']) * float(last_price['lastTradePrice']))), 'image' : f'{currency_name.lower()}.svg'})
            total_asset+= float(float(item['balance']) * float(last_price['lastTradePrice']))
            id_tracker += 1


    
    

    return available_coins, total_asset