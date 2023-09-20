from facebook_business.exceptions import FacebookRequestError
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.exceptions import FacebookRequestError
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.user import User
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.adsinsights import AdsInsights
import gspread
import random


def get_data():

    global cell
    access_token = <PRIVATE_LONG_TERM_TOKEN>
    app_id = <APP_ID>
    app_secret = <PRIVATE_APP_SECRET>

# Initialize the FacebookAdsApi with your access token


    date_preset = {

        'yesterday', 'last_7d','last_30d', 'last_month', 'this_month'
    }

    FacebookAdsApi.init(app_id, app_secret, access_token)

    for date in date_preset:
        cell += 1

        params = {
        'date_preset': date,
        'fields': ['spend', 'clicks', 'impressions', 'actions']

        }
        if date == 'last_7d':
            worksheet.update_cell(cell, ac_date_col, "02. Última semana")
        if date == 'last_30d':
            worksheet.update_cell(cell, ac_date_col, "03. Últimos 30 dias")
        if date == 'yesterday':
            worksheet.update_cell(cell, ac_date_col, "01. Ontem")
        if date == 'this_month':
            worksheet.update_cell(cell, ac_date_col, "05. Esse mês")
        if date == "last_month":
            worksheet.update_cell(cell, ac_date_col, " 04. Mês passado")


# Make a request to get all ad accounts
        try:
            user = User(fbid='me')
            my_ad_accounts = user.get_ad_accounts(fields=['id', 'name', 'conversion_values', 'website_purchase_roas'])


            for account in my_ad_accounts:
                account_id = account['id']
                ad_account_name = account.get('name', 'No name')

                if ad_account_name == "{YOUR AD_ACCOUNT}":    
                    print(ad_account_name)

                    insights = AdAccount(account_id).get_insights(params=params)
                    for insight in insights:
                        spend_value = float(insight.get('spend', '0')) #VALOR INVESTIDO
                        worksheet.update_cell(cell, ac_spend_col, spend_value)

                        clicks = int(insight.get('clicks', '0')) # CLIQUES REALIZADOS
                        print(f"INVESTED VALUE: {spend_value}")
                        print(f"CLICKS: {clicks}")
                

                        actions = insight.get('actions', [])
                   
                        for action in actions:
                            action_type = action.get('action_type', '')
                            value = int(action.get('value', 0))

                    #ESTABELECENDO CONDICIONAIS DE RESULTADOS
                            if action_type == 'onsite_conversion.messaging_conversation_started_7d': #MENSAGENS INICIADAS

                                messages = value
                                if messages > 0:
                                    cpl = spend_value / messages
                                    worksheet.update_cell(cell, ac_messages_col, messages) #UPDATE MENSAGENS INICIADAS 


                            if action_type == 'onsite_conversion.lead_grouped': #CADASTROS REALIZADOS

                                register = value
                                if register > 0:
                                    cpr = spend_value / register
                                    print(f"CADASTROS REALIZADOS: {register}")
                                    print(f"CUSTO POR CADASTRO: {cpr}")

                                    worksheet.update_cell(cell, ac_registers_col, register) #UPDATE CADASTROS REALIZADOS 
            

        except FacebookRequestError as e:
            print(f"An error occurred: {e}")

#GOOGLE SHEETS CONFIGURATION

KEY_VALUE = <PRIVATE_KEY> 
DICT = {}
gc = gspread.service_account(filename='key.json')
sh = gc.open_by_key(KEY_VALUE)
worksheet = sh.worksheet('YourWorksheetName')
wss = sh.worksheets()

ac_name_col = 1
ac_spend_col = 2
ac_messages_col = 3
ac_cost_per_messages_col = 4
ac_registers_col = 5
ac_cost_per_register_col = 6
ac_earning_col = 7
ac_date_col = 8
ac_roas_col = 9
ac_goal_col = 10
ac_sales_col = 11
ac_leads_col = 12
ac_oportunitties_col = 13
ac_ticket_col = 14
ac_cost_per_sales_col = 15



cell = 1 












get_data()
