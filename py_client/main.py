import os 
def main():
    def ffdf():
        os.system("python manage.py makemigrations")
        os.system("python manage.py migrate")
        os.system("python manage.py collectstatic --noinput")
    return ffdf()



if __name__ == "__main__":
    print(main())