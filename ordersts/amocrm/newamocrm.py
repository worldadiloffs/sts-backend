from amocrm_api import AmoOAuthClient # for oauth
import datetime
import os

class AmocrmManager:
    def __init__(self):
        self.accsecc_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImNkY2MzZGRjMGNkYjJjNTgzYzhkOGYyNGUzZWUwZDJkYzA0OTI4NzEwMjRjZDQ5NTcwMzA1NDZkYjg4NjhhNDRkMTMzOTg5MTkwOGM4YzMwIn0.eyJhdWQiOiJkNGRhNzdhZC1hZThmLTQ4YzMtYTBiOS04ZWJhYjlmNjk1MGIiLCJqdGkiOiJjZGNjM2RkYzBjZGIyYzU4M2M4ZDhmMjRlM2VlMGQyZGMwNDkyODcxMDI0Y2Q0OTU3MDMwNTQ2ZGI4ODY4YTQ0ZDEzMzk4OTE5MDhjOGMzMCIsImlhdCI6MTczMjE2ODk4MSwibmJmIjoxNzMyMTY4OTgxLCJleHAiOjE3MzIyNTUzODEsInN1YiI6IjExNDE1NDE4IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxOTA1OTQyLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiOTU0MmM4NzAtZGY5Mi00YjE3LWFmNDYtMThlOGI3ZmJjMzk5IiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.bHsolMMVIMrLQg70hcaqsiY7-6aNsT2hZ09AQyd_tioZ6LEUNc4hR-C_iKqBFCbYZRkAwZdkMdZWbeEvU_t8oE4gMEnrhDrZ90_0OhHdFKG0MZZH1BmnN4CANKWm2lG6Rvg3UxqA-rv3FBgqiMAqOYrIbHf0mjz1mGUU95D-cwjriijiNb7rbtiOOrrtxRWxi8K6C05DXLRY3jvfW_Fqf_OnzSSfI0cKLMbhgrCaKG6vAySUoy2PhlNg2pu5WTI59upiM8bQDHUsJ4HG2dteh8muJgt3_CaXIwsuao5Yg28gizb-VpZ1QjyALiTuLicXFgngrrVYWB-cYR0FwTXCWw"
        self.refresh_token = "def502007f26ba03f5de2fc87ba0e2416948a8a12bb6d59d6156260caa670a8d36507606c9c26f0eae1733d830578ea42c3b3527b1ed6caba466c0ecd68041969ee2d70f127e80c98e91135b54b4ffc5d3e979cfa6fdc8a88df9637bb2cc296dd84db9a33dd92bc88c0de59aef6dcd7b97f6a7471c475242ded1b6c249ecab2414fd1288b8e4eac94b2a4d60878de484339ec0405206c3a874199f947a267d2591e2875e7bc62632f06004ffa6d2ee72035c2f12b7630c1adf2601e0594c141945a9ffa9046531d3d6da7e42fb4afac42d63b51edc6f3f0efdb704f08f7617ee2e28b60a40771356a34c920b87c9a02a0c2616771c19d63c9b3e0cb0017925c7b6d389a253b0bedf3520130e4f6d1acdba3bd2c93670bad7f25129d75f29729e4dfee6dd1a7aec9eb00097db3f638b46e2648e75b60b88728440161b5c028949663bfb1b2ea75cc1d7bd651a634f17ff04ec620df5033ee17c6cd4fa2ca54ce5d0e371995a442c96acb8ac3bdd56e8450a35774c733a73d8cf488b8260fd2de174c5966b41ead9247d9799fe44fef66f7eca21f02d2be1087f7f012b5445c29c7b5538d4d2af49f37bb5b8cc32dcb249bef27b7e8224e4ca68700af4c1fbd250d76f0a62b937a56370eb9b428a417100b8c4f5a3796709abfa10a6f26b5c7bf73751e46bdd8b2c14a06557c5ade7"
        self.client_id = 'd4da77ad-ae8f-48c3-a0b9-8ebab9f6950b'
        self.client_secret = 'odTo3DRX2oMGbFPjQ5eLcIi0PZssKSNE1qHn2k5YjkHjRzIIaC14qz3sGuNy5jyx'
        self.redirect_uri = "https://api.sts-shop.uz",
        self.crm_url = 'https://anvarjonsts.amocrm.ru/'
        self.client = AmoOAuthClient(
            access_token=self.accsecc_token,
            refresh_token=self.refresh_token,
            crm_url=self.crm_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
        )
        
    @property
    def self_seccess_login(self):
        dt = datetime.datetime.today().strftime("%a, %d %b %Y %H-%m-%d")
        date_time = f"{dt} UTC"
        headers = {
            "IF-MODIFIED-SINCE": f"{date_time}",
            "Content-Type": "application/json",
        }

        self.client.update_session_params(headers)
    
    def refresh_access_token(self):
        tokens = self.client.refresh_tokens()
        self.accsecc_token = tokens['access_token']
        self.refresh_token = tokens['refresh_token']
        # Optionally, update the environment variables or a secure storage with the new tokens
        os.environ['AMOCRM_ACCESS_TOKEN'] = self.accsecc_token
        os.environ['AMOCRM_REFRESH_TOKEN'] = self.refresh_token

    def create_lead(self, name, contant_id, product_name):
        objects = [
            {
                "name": name,
                "_embedded": {
                    "contacts": [
                        {
                            "id": contant_id
                        }
                    ]
                },
                "custom_fields_values": [
                    {
                        "field_id": 1058921,
                        "values": [
                            {
                                "value": f"{product_name}",
                            }
                        ]
                    }
                ]
            },
        ]
        return self.client.create_leads(objects)

    def create_contact(self, name, phone):
        contacts = [
            {
                "name": name,
                "custom_fields_values": [
                    {
                        "field_id": 1051791,
                        "field_name": "Телефон",
                        "field_code": "PHONE",
                        "field_type": "multitext",
                        "values": [
                            {
                                "value": phone,
                                "enum_id": 1232765,
                                "enum_code": "MOB"
                            }
                        ]
                    }
                ]
            },
        ]
        result = self.client.create_contacts(contacts)
        return result["_embedded"]['contacts'][0]['id']
    
    def create_request_amocrm(self, phone, name, product_name):
        self.self_seccess_login
        try:
            id = self.create_contact(name=name, phone=phone)
            self.create_lead(name=name, contant_id=id, product_name=product_name)
        except Exception as e:
            if 'token expired' in str(e).lower():
                self.refresh_access_token()
                id = self.create_contact(name=name, phone=phone)
                self.create_lead(name=name, contant_id=id, product_name=product_name)
            else:
                raise e

def request_to_amocrm(phone, name, product_name=None):
    return AmocrmManager().create_request_amocrm(phone=phone, name=name, product_name=product_name)