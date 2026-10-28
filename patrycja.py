# zadanie a
# def funkcja(imie1, imie2, imie3, imie4, imie5):
#     print("Imiona:", imie1, imie2, imie3, imie4, imie5)
#
#
# imie1 = input("Podaj pierwsze imię: ")
# imie2 = input("Podaj drugie imię: ")
# imie3 = input("Podaj trzecie imię: ")
# imie4 = input("Podaj czwarte imię: ")
# imie5 = input("Podaj piąte imię: ")
#
# funkcja(imie1, imie2, imie3, imie4, imie5)

# zadanie b
# def funkcja2(lista_liczb):
#     if len(lista_liczb) > 6:
#         print("Podano za dużo liczb. Podaj co najwyżej 5 liczb.")
#         return
#     lista_liczb3 = []
#     for liczba in lista_liczb:
#         liczba = liczba*2
#
#         lista_liczb3.append(liczba)
#
#     return lista_liczb3
#     # print("Liczby:", ", ".join(lista_liczb3))
#
# lista_liczb2 = input("Podaj liczby oddzielone przecinkami: ")
# lista_liczb4 = funkcja2([int(x) for x in lista_liczb2.split(",")])
# print(lista_liczb4)

# zadanie c
# def funkcja3(lista_liczb):
#     for liczba in lista_liczb:
#         if liczba % 2 == 0:
#             print(liczba)
#
# funkcja3(range(1, 11))

# zadanie d
# def funkcja4(lista_liczb):
#     for liczba in lista_liczb:
#         if lista_liczb.index(liczba) % 2 == 0:
#             print(liczba)
#
# funkcja4(range(1, 11))
