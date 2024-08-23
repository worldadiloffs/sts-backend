import threading

def print_message(message, count):
    for _ in range(count):
        print(message)

# Funksiyani 5 soniyadan keyin argumentlar bilan chaqiramiz
timer = threading.Timer(5.0, print_message, args=("Hello, World!", 3))

# Timer'ni boshlash
timer.start()

print("Timer ishga tushdi.")



# Output:
