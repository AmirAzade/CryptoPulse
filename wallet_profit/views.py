from django.shortcuts import render
import requests

static_token = ""

url = 'https://api.nobitex.ir/users/wallets/balance'
headers = {
    "Authorization": "Token yourTOKENhereHEX0000000000"
}
data = {
    "currency": "btc"
}

all_coins = ['BTC', 'ETH', 'LTC', 'XRP', 'BCH', 'BNB', 'EOS', 'XLM', 'ETC', 'TRX', 'DOGE', 'UNI', 'DAI', 'LINK', 'DOT', 'AAVE', 'ADA', 'SHIB', 'FTM', 'MATIC', 'AXS', 'MANA', 'SAND', 'AVAX', 'MKR', 'GMT', 'USDC', 'BTC', 'ETH', 'LTC', 'XRP', 'BCH', 'BNB', 'EOS', 'XLM', 'ETC', 'TRX', 'PMN', 'DOGE', 'UNI', 'DAI', 'LINK', 'DOT', 'AAVE', 'ADA', 'SHIB', 'FTM', 'MATIC', 'AXS', 'MANA', 'SAND', 'AVAX', 'MKR', 'GMT', 'USDC']
coins = ['BTC', 'ETH', 'LTC', 'XRP', 'BNB', 'ETC', 'TRX', 'DOGE', 'DAI', 'ADA', 'SHIB', 'AXS', 'MANA', 'SAND', 'AVAX', 'USDC']

def display_number(request):
    if request.method == 'POST':
        token = request.POST.get('token', 0)
        headers['Authorization'] = f"Token {token}"
        static_token = token


        available_coins = []

        id_tracker = 0
        for c in coins:
            data['currency'] = c.lower()
            response = requests.post(url, headers=headers, json=data)
            if float(response.json()['balance']) != 0: last_price = requests.get(f'https://api.nobitex.ir/v2/orderbook/{c.upper()}USDT')

            if response.status_code == 200 and (last_price.status_code == 200 or float(response.json()['balance'])) != 0:
                available_coins.append({'id' : id_tracker, 'coin' : c.upper(), 'asset' : float(response.json()['balance']), 'image' : f'{c.lower()}.svg', 'priceusdt' : float(last_price.json()['lastTradePrice'])})
                id_tracker += 1
            

        print(available_coins)
        available_coins = sorted(available_coins, key=lambda d: d['asset'], reverse=True)
        return render(request, 'wallet.html', {'tr_data': available_coins, 'static_token' : static_token})
        

        
    else:
        return render(request, 'wallet.html', {'number': 0})
