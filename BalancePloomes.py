from facebook_business.exceptions import FacebookRequestError
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
import requests
import Metaploo #Where is defined your private keys


content_saldos = ""

saldos_pipeId = ID #your pipeId in the Ploomes CRM
saldos_stageId = ID #your stageid in the Ploomes CRM


def newCards(card_title, PipeId, amount):

    url = "https://api2.ploomes.com/Deals"

    user_key = Metaploo.user_key


    headers = {

        'User-Key': user_key,
        'Content-Type': 'application/json'
    }


    data = {

        "Amount": f"{amount}", #VALOR A SER ATUALIZADO
        "Title"  : f"{card_title}", #TÍTULO DO CARD.
        "OwnerId": ID, #RESPONSÁVEL PELO CARD
        "PipelineId" : ID, #ID FUNIL SALDOS
        "StageId" : ID #ID ESTÁGIO 

    }


    response = requests.post(url, headers=headers, json=data)


    if response.status_code == 201:
        print("Requisição POST bem-sucedida")
        print("Resposta da API:", response.json())
    else:
        print("Erro na requisição POST")
        print("Código de status:", response.status_code)
        print("Resposta da API:", response.text)




def get_data():
    
    global content_saldos, saldos_pipeId

    app_id = Metaploo.app_id
    app_secret = Metaploo.app_secret
    access_token = Metaploo.access_token

    # Initialize the FacebookAdsApi with your access token
    FacebookAdsApi.init(app_id, app_secret, access_token)

    params = {

           "fields" : "balance, spend_cap, amount_spent",
           "access_token" : f"{access_token}"
        
        }






    # Make a request to get all ad accounts
    try:
        user = User(fbid='me')
        my_ad_accounts = user.get_ad_accounts(fields=['id', 'name'])

        for account in my_ad_accounts:
            url = f"https://graph.facebook.com/v3.2/{account['id']}"
            response = requests.get(url, params=params)

            if response.status_code == 200:

                data = response.json()
                account_name = account['name']
                print(f"Nome da conta: {account['name']}")
                

                saldo = float(data.get('balance', '0'))
                valor_gasto = float(data.get('amount_spent', '0'))
                spend_cap = float(data.get('spend_cap', '0'))

                if spend_cap == 0:

                    saldo_final = (saldo/100)
                    saldo_final = -saldo_final if saldo_final < 0 else saldo_final
                    print(f"{account_name} Saldo restante: R${saldo_final}\n")
                    content_saldos += f"{account_name} Saldo Restante: R${saldo_final}\n"
                    newCards(account_name, saldos_pipeId, saldo_final)



                else:
                    saldo_final = (valor_gasto - spend_cap)/100
                    saldo_final = -saldo_final if saldo_final < 0 else saldo_final
                    print(f"{account_name} Saldo restante: R${saldo_final}\n")
                    content_saldos += f"{account_name} Saldo Restante: R${saldo_final}\n"
                    newCards(account_name, saldos_pipeId, saldo_final)




       



    except FacebookRequestError as e:
        print(f"An error occurred: {e}")






get_data()
