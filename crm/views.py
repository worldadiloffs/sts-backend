from config.settings import crm_token , crm_key, crm_url



class CrmAuth(object):
    def __init__(self):
        self.token = crm_token
        self.key = crm_key
        self.url = crm_url

    def get_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "X-Client-Key": self.key,
        }
    
    def get_url(self):
        return self.url
    
    def get_token(self):
        return self.token
    
    def get_key(self):
        return self.key