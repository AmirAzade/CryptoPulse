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

coins = ['btc', 'trx', 'ltc']

def display_number(request):
    if request.method == 'POST':
        token = request.POST.get('token', 0)
        headers['Authorization'] = f"Token {token}"
        static_token = token


        available_coins = []

        id_tracker = 0
        for c in coins:
            response = requests.post(url, headers=headers, json=data)

            if(response.status_code == 200):
                available_coins.append({'id' : id_tracker, 'coin' : c, 'asset' : response.json()['balance']})
                id_tracker += 1
            


        return render(request, 'wallet.html', {'tr': available_coins, 'static_token' : static_token})
        

        
    else:
        return render(request, 'wallet.html', {'number': 0})
