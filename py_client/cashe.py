import time
import functools

def timed_cache(timeout):
    def decorator(func):
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args):
            if args in cache:
                result, timestamp = cache[args]
                # Cache qachon eskirganligini tekshirish
                if time.time() - timestamp < timeout:
                    print("Returning cached result")
                    return result

            # Natija yangidan hisoblanadi va cachega qo'shiladi
            result = func(*args)
            cache[args] = (result, time.time())
            return result

        return wrapper
    return decorator

@timed_cache(4)  # 5 daqiqa = 300 soniya
def expensive_computation(x):
    print(f"Computing {x}...")
    return x * x

# Funksiyani birinchi marta chaqiramiz, natija cachelanadi
print(expensive_computation(10))  # Output: "Computing 10..." va 100

# 5 daqiqa ichida ikkinchi marta chaqirilsa, cachedan natija olinadi
print(expensive_computation(10))  # Output: "Returning cached result" va 100

# 5 daqiqadan keyin chaqirilsa, natija yangidan hisoblanadi
time.sleep(6)  # 301 soniya kutamiz, bu cachening eskirishini ta'minlaydi
print(expensive_computation(10))  # Output: "Computing 10..." va 100


@timed_cache(timeout=4)  # 5 daqiqa = 3
def product_fn(numbers):
    return [i * 2 for i in numbers]

numbers = [1, 2, 3, 4, 5]
