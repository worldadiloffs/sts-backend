import threading

def my_function():
    print("Bu xabar 5 soniyadan keyin chiqadi!")

# 5 soniyadan keyin funksiyani ishga tushirish uchun Timer yaratish
timer = threading.Timer(5.0, my_function)

# Timer'ni boshlash
timer.start()

print("Bu xabar darhol chiqadi!")