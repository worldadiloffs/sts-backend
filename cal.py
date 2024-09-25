summa = 62900
oy = 12
oylik = 7338



# oylik = ((summa *(30.42)*foiz))/(365*100) +   (summa/oy)

foiz = (oylik  - summa/oy) * 365 / (summa *(30.42))
print(foiz)

