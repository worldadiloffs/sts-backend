# from amocrm_api import AmoOAuthClient # for oauth
# import datetime
# import os

# class AmocrmManager:
#     def __init__(self):
#         self.accsecc_token = os.environ['AMOCRM_ACCESS_TOKEN']
#         self.refresh_token = os.environ['AMOCRM_REFRESH_TOKEN']
#         self.client_id = 'adff957c-f828-4d10-8008-21f3e8781733'
#         self.client_secret = 'er3tJARihFWuZMF8bneTqm6OF4jcOrYYwbsMMy6slYt4cWQbbk1H3T5L3jOCTvEM'
#         self.redirect_uri = "https://api.sts-shop.uz",
#         self.crm_url = 'https://anvarjonsts.amocrm.ru/'
#         self.client = AmoOAuthClient(
#             access_token=self.accsecc_token,
#             refresh_token=self.refresh_token,
#             crm_url=self.crm_url,
#             client_id=self.client_id,
#             client_secret=self.client_secret,
#             redirect_uri=self.redirect_uri,
#         )
        
#     @property
#     def self_seccess_login(self):
#         dt = datetime.datetime.today().strftime("%a, %d %b %Y %H-%m-%d")
#         date_time = f"{dt} UTC"
#         headers = {
#             "IF-MODIFIED-SINCE": f"{date_time}",
#             "Content-Type": "application/json",
#         }

#         self.client.update_session_params(headers)
    
#     def refresh_access_token(self):
#         tokens = self.client.refresh_tokens()
#         self.accsecc_token = tokens['access_token']
#         self.refresh_token = tokens['refresh_token']
#         # Optionally, update the environment variables or a secure storage with the new tokens
#         os.environ['AMOCRM_ACCESS_TOKEN'] = self.accsecc_token
#         os.environ['AMOCRM_REFRESH_TOKEN'] = self.refresh_token

#     def create_lead(self, name, contant_id, product_name):
#         objects = [
#             {
#                 "name": name,
#                 "_embedded": {
#                     "contacts": [
#                         {
#                             "id": contant_id
#                         }
#                     ]
#                 },
#                 "custom_fields_values": [
#                     {
#                         "field_id": 1058921,
#                         "values": [
#                             {
#                                 "value": f"{product_name}",
#                             }
#                         ]
#                     }
#                 ]
#             },
#         ]
#         return self.client.create_leads(objects)

#     def create_contact(self, name, phone):
#         contacts = [
#             {
#                 "name": name,
#                 "custom_fields_values": [
#                     {
#                         "field_id": 1051791,
#                         "field_name": "Телефон",
#                         "field_code": "PHONE",
#                         "field_type": "multitext",
#                         "values": [
#                             {
#                                 "value": phone,
#                                 "enum_id": 1232765,
#                                 "enum_code": "MOB"
#                             }
#                         ]
#                     }
#                 ]
#             },
#         ]
#         result = self.client.create_contacts(contacts)
#         return result["_embedded"]['contacts'][0]['id']
    
#     def create_request_amocrm(self, phone, name, product_name):
#         self.self_seccess_login
#         try:
#             id = self.create_contact(name=name, phone=phone)
#             self.create_lead(name=name, contant_id=id, product_name=product_name)
#         except Exception as e:
#             if 'token expired' in str(e).lower():
#                 self.refresh_access_token()
#                 id = self.create_contact(name=name, phone=phone)
#                 self.create_lead(name=name, contant_id=id, product_name=product_name)
#             else:
#                 raise e

# def request_to_amocrm(phone, name, product_name=None):
#     return AmocrmManager().create_request_amocrm(phone=phone, name=name, product_name=product_name)


from amocrm.v2 import tokens, Contact, Lead, custom_field
from amocrm.v2.tokens import default_token_manager, FileTokensStorage


class AmocrmManager:
    def __init__(self):
        default_token_manager(
            client_id="adff957c-f828-4d10-8008-21f3e8781733",
            client_secret="er3tJARihFWuZMF8bneTqm6OF4jcOrYYwbsMMy6slYt4cWQbbk1H3T5L3jOCTvEM",
            subdomain="anvarjonsts",
            redirect_url="https://api.sts-shop.uz",
            storage=FileTokensStorage(), 
        )

    def create_contact(self, name, phone):
        contact = Contact(name=name)
        contact.custom_fields_values = [
            {
                "field_code": "PHONE",
                "values": [{"value": phone, "enum_code": "MOB"}]
            }
        ]
        contact.save()
        print(" Contact created:", contact.id, contact.name, contact.custom_fields_values)
        return contact.id
    

    def create_lead(self, name, contact_id, product_name):
        lead = Lead(name=name)
        lead.custom_fields_values = [
            {
                "field_id": 1058921,
                "values": [{"value": product_name}]
            }
        ]
        lead._embedded = {"contacts": [{"id": contact_id}]}
        lead.save()
        print("Lead created:", lead.id, lead.name, lead.custom_fields_values)
        return lead.id

    def create_request_amocrm(self, phone, name, product_name):
        try:
            contact_id = self.create_contact(name=name, phone=phone)
            lead_id = self.create_lead(name=name, contact_id=contact_id, product_name=product_name)
            return {
                "success": True,
                "contact_id": contact_id,
                "lead_id": lead_id
            }
        except Exception as e:
            print("Error while creating in amoCRM:", e)
            return {
                "success": False,
                "error": str(e)
            }


def request_to_amocrm(phone, name, product_name=None):
    crm = AmocrmManager()
    return crm.create_request_amocrm(phone=phone, name=name+phone, product_name=product_name or "Без названия")

