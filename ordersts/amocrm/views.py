# from amocrm_api import AmoLegacyClient # for login password auth
from amocrm_api import AmoOAuthClient # for oauth
import  datetime

class AmocrmManager:
    def __init__(self):
        self.accsecc_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjNkNTczOTY3ZTk0NjE0YzEyNzljNTBjZmQ4ZTY5YTA0YTZmZjU0NDZmMjdjOTZjZGQ5ZTIwMTU5YTAxZmViNzIxMTgyZTMwYWM3ZTUyYzlkIn0.eyJhdWQiOiJkNGRhNzdhZC1hZThmLTQ4YzMtYTBiOS04ZWJhYjlmNjk1MGIiLCJqdGkiOiIzZDU3Mzk2N2U5NDYxNGMxMjc5YzUwY2ZkOGU2OWEwNGE2ZmY1NDQ2ZjI3Yzk2Y2RkOWUyMDE1OWEwMWZlYjcyMTE4MmUzMGFjN2U1MmM5ZCIsImlhdCI6MTczMTQ5MDkxOCwibmJmIjoxNzMxNDkwOTE4LCJleHAiOjE3MzgzNjgwMDAsInN1YiI6IjExNDE1NDE4IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxOTA1OTQyLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJjcm0iLCJmaWxlcyIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiLCJwdXNoX25vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiMzRlNjg4ZDAtZWQwMi00MTVlLWE1YzYtY2U4NTY0MDgxNGQ1IiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.PdNKc1eQnF6jGOLYsg9uXF5rWYqzm32251B698DukpDE9HTbAC7M17epkAerhRAB22rbemAsti9jBj_gaAwz6zt9t9RlJF3kncMTQY8nBCGMvH0z7curLTo3kKCSqW6M9QFA1Xc-M08E64XpNgIDgJh9XOxFQdhFAPGaDemEMQl9egv9o81b6k9DTGF-EivWNx9ygcGs6_d7FgrOcJbJ0CgQPOt_b6PwZwotr2n52Wm1D6HdC7xdHmbUOwQGkSJUT8glKO1fqcPfMeZxz285V7gMwgXrQcmpkm0_7Nih3-0XOpQUDhLwPFWKQPonQ3vN0t5oEaU9pwVVunJaoUJorQ'
        # self.accsecc_token=  'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjljOTFhM2UxYzQ2NzQ2NTQ5NWRjMGU0MTRlMTBiMjY3MDkzNWJjZTI4NWM0MWIyY2M4Yjc2ZmE4YzUwYWNmM2Q4NDlmZGNjMTJkNTQxMTBmIn0.eyJhdWQiOiJkNGRhNzdhZC1hZThmLTQ4YzMtYTBiOS04ZWJhYjlmNjk1MGIiLCJqdGkiOiI5YzkxYTNlMWM0Njc0NjU0OTVkYzBlNDE0ZTEwYjI2NzA5MzViY2UyODVjNDFiMmNjOGI3NmZhOGM1MGFjZjNkODQ5ZmRjYzEyZDU0MTEwZiIsImlhdCI6MTcyOTU5NTcyNywibmJmIjoxNzI5NTk1NzI3LCJleHAiOjE3Mjk2ODIxMjcsInN1YiI6IjExNDE1NDE4IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMxOTA1OTQyLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiMWM0YzJiODgtMGEzNy00NTgwLThhOTEtOGVhMjA2MzdhYjE1IiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.EtVu8Ht-F94AMU7gYuGRFccx_2Wus-fsdkTL52q0I62Ur-7a4PTOxU2OPhTjf7sjZuDuHOBaS6fgvKps1PXQA8enXLwwB2rrXTPuDgzJPeQFw2SHVYwyZ1Q8uXHkgtCJdn1b4wMaIWwGKaPTll_tYR2-5chSyAFC5q7CC-0lFxn0ObgFcneT2kBc0pvSQlX6zZHyZBPQF5DslvpTcJNiS8oAeG0aXQAWMxv58FSge_zwfY1VqAolt5KQBlwyollub69QX7bNcWOHVcZD9ig87dO5SpAwJYaNlKEdf0mjWB8uizOw_UpGfl3NkKBi56POsyELr9D6HbiyG7nxinwdBA'
        self.refresh_token = 'def502009a7bdf1740b334939a781ca4138997cc9d7efd5579e26c9ba6f328540dabe76fa82091825860d5da752014a56663be692df4c7abdc1e272c299aa698bafd17bca01a2a7c37e84bef0ecc6113b65de7b5192f2b880b90d9a3fb49654670cd5827b41bc749d0673d83831821175af9bf149146448711d7606ca5a2853c1d1e4eef08829b959758da3e2ed29c6fd13e35731d664ecfd6eb09773cb419b959c19c1d1ce0226cffe424bb075a0bbb7bb08a87bbcc0cfefb774fabd978d4888c8f34eeda97b77d3b1f8b60e672ee1c023ef8e72302bdaf27625cd18b02f0ff746bc74bbe003b5ff7336249a908c491c06511cad36eaa17e49a09f780e7fa2029e13aaf19abc4e946656273b778a6835a84b5131ab6c02039b86312d297a3584f730c8e10264ce6effdaef4f6feea52983ec8fcaedaf32e77658f9fe30068feca9fc32b06f52f6b779c574c66367b50d64e915dccb4450471676242b213291f48fd2d307abf79bf5ed804f570a4eefeae927a5b72e63b3ed4ccbf006097fc3e7fcc26fbc3fea6e228db83813c9ce6fee19270ed786c267edf9d33b0fcafe180249771e7e2f7a59b282076162f5707b488877a2dfb912424e3f05a651a581ee6c7830184be97793700fb604c07462bfa0776380b80818f62d234eb1f51551b4774526183870a4051040a142a10e2'
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
            redirect_uri=self.redirect_uri,)
        
    @property
    def self_seccess_login(self):
        dt = datetime.datetime.today().strftime("%a, %d %b %Y %H-%m-%d")
        date_time = f"{dt} UTC"
        headers = {
            "IF-MODIFIED-SINCE": f"{date_time}",
            "Content-Type": "application/json",
        }

        self.client.update_session_params(headers)
    
    def create_lead(self, name,  contant_id, product_name):
        objects = [
                    {
                    "name": name,   
                                # "created_by": 0,
                                # "price": 20000,
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
        conctacts = [
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
        result = self.client.create_contacts(conctacts)

        return  result["_embedded"]['contacts'][0]['id']
    

    def create_request_amocrm(self, phone, name, product_name):
        self.self_seccess_login
        id = self.create_contact(name=name, phone=phone)
        self.create_lead(name=name,  contant_id=id, product_name=product_name)






# lead = AmocrmManager().create_request_amocrm('+998991234567', 'Azamat')

def request_to_amocrm(phone, name, product_name=None):
    return AmocrmManager().create_request_amocrm(phone=phone, name=name, product_name=product_name)
            