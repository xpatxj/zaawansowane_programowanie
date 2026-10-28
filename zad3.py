class Property:
    def __init__(self, area, rooms, price, address):
        self.area = area
        self.rooms = rooms
        self.price = price
        self.address = address

    def __str__(self):
        opis = f"""
        Nieruchomość:
        - area - powierzchnia nieruchomości : {self.area}
        - rooms - liczba pokoi : {self.rooms}
        - price - cena nieruchomości : {self.price}
        - address - adres nieruchomości : {self.address}
        """
        return opis


class House(Property):
    def __init__(self, area, rooms, price, address, plot):
        super().__init__(area, rooms, price, address)
        self.plot = plot

    def __str__(self):
        opis = f"""
        Dom:
        - area - powierzchnia domu : {self.area}
        - rooms - liczba pokoi : {self.rooms}
        - price - cena domu : {self.price}
        - address - adres domu : {self.address}
        - plot - powierzchnia działki : {self.plot}
        """
        return opis


class Flat(Property):
    def __init__(self, area, rooms, price, address, floor):
        super().__init__(area, rooms, price, address)
        self.floor = floor

    def __str__(self):
        opis = f"""
        Mieszkanie:
        - area - powierzchnia mieszkania : {self.area}
        - rooms - liczba pokoi : {self.rooms}
        - price - cena mieszkania : {self.price}
        - address - adres mieszkania : {self.address}
        - floor - piętro mieszkania : {self.floor}
        """
        return opis


Property = Property(100, 3, 500000, "ul. Kwiatowa 10, Warszawa")
House = House(100, 3, 500000, "ul. Kwiatowa 10, Warszawa", 200)
Flat = Flat(100, 3, 500000, "ul. Kwiatowa 10, Warszawa", 5)
print(Property)
print(House)
print(Flat)
