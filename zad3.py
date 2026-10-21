def func3(x: float) -> bool:
    return x % 2 == 0

wynik = func3(4.0)
if wynik == True:
    print("Liczba jest parzysta.")  
else:
    print("Liczba jest nieparzysta.")
