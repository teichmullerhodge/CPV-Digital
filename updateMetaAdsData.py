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
import time
import gspread


def get_data():

    global cell_pos, gspread_quota_limit
    access_token = <PRIVATE_LONG_TERM_TOKEN>
    app_id = <APP_ID>
    app_secret = <PRIVATE_APP_SECRET>

# Initialize the FacebookAdsApi with your access token


    date_preset = {

        'yesterday', 'last_7d','last_30d', 'last_month', 'this_month'
    }

    FacebookAdsApi.init(app_id, app_secret, access_token)

    for date in date_preset:
        cell_pos += 4 #Skip four lines for new accounts, adjust it at your need.

        params = {

        'date_preset': date,
        'fields': ['spend', 'clicks', 'impressions', 'actions']

        }
        if date == 'last_7d':
            worksheet.update_cell(cell_pos, ac_date_col, "Última semana")
            gspread_quota_limit += 1
        if date == 'last_30d':
            worksheet.update_cell(cell_pos, ac_date_col, "Últimos 30 dias")
            gspread_quota_limit += 1
        if date == 'yesterday':
            worksheet.update_cell(cell_pos, ac_date_col, "Ontem")
            gspread_quota_limit += 1
        if date == 'this_month':
            worksheet.update_cell(cell_pos, ac_date_col, "Esse mês")
            gspread_quota_limit += 1

        if date == "last_month":
            worksheet.update_cell(cell_pos, ac_date_col, " Mês passado")
            gspread_quota_limit += 1



# Make a request to get all ad accounts
# gspread_quota_limit is used since there's a QUOTA API LIMIT
        try:
            user = User(fbid='me')
            my_ad_accounts = user.get_ad_accounts(fields=['id', 'name'])


            for account in my_ad_accounts:
                cell_pos += 1
                if gspread_quota_limit > 45:
                    print("sleeping...")
                    time.sleep(60)
                    gspread_quota_limit = 0

                account_id = account['id']
                ad_account_name = account.get('name', 'No name')

                worksheet.update_cell(cell_pos, ac_name_col, ad_account_name)
                gspread_quota_limit += 1

                insights = AdAccount(account_id).get_insights(params=params)
                for insight in insights:
                        if gspread_quota_limit > 45:
                            
                            print("sleeping...")
                            time.sleep(60)
                            gspread_quota_limit = 0

                        spend_value = float(insight.get('spend', '0')) #VALOR INVESTIDO
                        worksheet.update_cell(cell_pos, ac_spend_col, spend_value)
                        gspread_quota_limit += 1

                        clicks = int(insight.get('clicks', '0')) # CLIQUES REALIZADOS
                        worksheet.update_cell(cell_pos, ac_clicks_col, clicks)
                        print(f"INVESTED VALUE: {spend_value}")
                        print(f"CLICKS: {clicks}")
                

                        actions = insight.get('actions', [])
                   
                        for action in actions:

                            if gspread_quota_limit > 45:
                                print("sleeping...")
                                time.sleep(60)
                                gspread_quota_limit = 0

                            action_type = action.get('action_type', '')
                            value = int(action.get('value', 0))

                    #ESTABELECENDO CONDICIONAIS DE RESULTADOS
                            if action_type == 'onsite_conversion.messaging_conversation_started_7d': #MENSAGENS INICIADAS

                                messages = value
                                if messages > 0:
                                    cpl = spend_value / messages
                                    worksheet.update_cell(cell_pos, ac_messages_col, messages) #UPDATE MENSAGENS INICIADAS
                                    gspread_quota_limit += 1

                            if action_type == 'onsite_conversion.lead_grouped': #CADASTROS REALIZADOS

                                register = value
                                if register > 0:
                                    cpr = spend_value / register
                                    print(f"CADASTROS REALIZADOS: {register}")
                                    print(f"CUSTO POR CADASTRO: {cpr}")

                                    worksheet.update_cell(cell_pos, ac_registers_col, register) #UPDATE CADASTROS REALIZADOS 
                                    gspread_quota_limit += 1

                            if action_type == 'omni_purchase': #VENDAS REALIZADAS

                                sales = value
                                if sales > 0:
                                    cost_per_sales = spend_value / sales
                                    worksheet.update_cell(cell_pos, ac_sales_col, sales) #UPDATE VENDAS REALIZADAS
                                    gspread_quota_limit += 1

                            if action_type == 'add_to_cart':
                                
                                add_to_cart = value
                                if add_to_cart > 0:
                                    cost_per_add_to_cart = spend_value / add_to_cart
                                    worksheet.update_cell(cell_pos, ac_add_to_cart_col, add_to_cart)
                                    gspread_quota_limit += 1

        except FacebookRequestError as e:
            print(f"An error occurred: {e}")

#GOOGLE SHEETS CONFIGURATION

KEY_VALUE = <PRIVATE KEY> 
DICT = {}
gc = gspread.service_account(filename='key.json')
sh = gc.open_by_key(KEY_VALUE)
worksheet = sh.worksheet('YourWorksheetPageName')
wss = sh.worksheets()

ac_name_col = 1
ac_spend_col = 2
ac_clicks_col = 3
ac_cost_per_clicks_col = 4
ac_messages_col = 5
ac_cost_per_messages_col = 6
ac_registers_col = 7
ac_cost_per_register_col = 8
ac_add_to_cart_col = 9
ac_cost_per_add_to_cart_col = 10
ac_sales_col = 11
ac_cost_per_sales_col = 12
ac_date_col = 13
ac_status_col = 14



cell_pos = 1 
gspread_quota_limit = 0

get_data()
