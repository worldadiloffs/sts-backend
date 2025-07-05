from amocrm_manager import request_to_amocrm

if __name__ == "__main__":
    result = request_to_amocrm("+998901234567", "Test User", "Test Product")
    print(result)