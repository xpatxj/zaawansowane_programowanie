class Library:
    def __init__(self, city, street, zip_code, open_hours : str, phone):
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.open_hours = open_hours
        self.phone = phone

    def __str__(self):
        opis = """
        Biblioteka:
        - city - miasto, w którym znajduje się biblioteka
        - street - ulica, na której znajduje się biblioteka
        - zip_code - kod pocztowy, w którym znajduje się biblioteka
        - open_hours - godziny otwarcia biblioteki, string
        - phone - numer telefonu biblioteki
        """
        return opis

class Employee:
    def __init__(self, first_name, last_name, hire_date, birth_date, city, street, zip_code, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date
        self.birth_date = birth_date
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.phone = phone

    def __str__(self):
        opis = """
        Pracownik:
        - first_name - pierwsze imię pracownika
        - last_name - nazwisko pracownika
        - hire_date - data zatrudnienia pracownika
        - birth_date - data urodzenia pracownika
        - city - miasto, w którym mieszka pracownik
        - street - ulica, na której mieszka pracownik
        - zip_code - kod pocztowy, w którym mieszka pracownik
        - phone - numer telefonu pracownika
        """
        return opis


class Book:
    def __init__(self, library, publication_date, author_name, author_surname, number_of_pages):
        self.library = library
        self.publication_date = publication_date
        self.author_name = author_name
        self.author_surname = author_surname
        self.number_of_pages = number_of_pages

    def __str__(self):
        opis = """
        Książka:
        - library - biblioteka, w której znajduje się książka
        - publication_date - data publikacji książki
        - author_name - imię autora książki
        - author_surname - nazwisko autora książki
        - number_of_pages - liczba stron książki
        """
        return opis

class Order:
    def __init__(self, employee, student, books, order_date):
        self.employee = employee
        self.student = student
        self.books = books
        self.order_date = order_date

    def __str__(self):
        opis = f"""
        Zamówienie: 
        - employee - pole pracownika : {self.employee.first_name}
        - student - pole studenta : {self.student.name}
        - books - lista obiektów Book:
            - library - pole obiektu Library
            - publication_date - pole obiektu Book
            - author_name - pole obiektu Book
            - author_surname - pole obiektu Book
            - number_of_pages - pole obiektu Book 
            {self.books}
        - order_date - data zamowienia : {self.order_date}
        """
        return opis

class Student:
    def __init__(self, name, marks):
        self.name = name
        self.marks = marks

    def __str__(self):
        return f"{self.name} {self.marks}"

    def is_passed(self):
        oceny = []
        for x in self.marks:
            oceny.append(int(x))
        srednia = sum(oceny) / len(oceny)
        if srednia>50:
            return True
        else:
            return False

library1 = Library("Warszawa", "ul. Kwiatowa 10", "00-001", "9:00-17:00", "123456789")
library2 = Library("Kraków", "ul. Różana 5", "30-002", "10:00-18:00", "987654321")
book1 = Book(library1, "2020-01-01", "Jan", "Kowalski", 300)
book2 = Book(library2, "2019-05-15", "Anna", "Nowak", 250)
book3 = Book(library1, "2021-09-10", "Piotr", "Wiśniewski", 400)
book4 = Book(library2, "2018-12-20", "Katarzyna", "Lewandowska", 150)
book5 = Book(library1, "2022-03-05", "Michał", "Zieliński", 350)
employee1 = Employee("Jan", "Kowalski", "2020-01-01", "1990-05-15", "Warszawa", "ul. Kwiatowa 10", "00-001", "123456789")
employee2 = Employee("Anna", "Nowak", "2019-05-15", "1985-10-20", "Kraków", "ul. Różana 5", "30-002", "987654321")
employee3 = Employee("Piotr", "Wiśniewski", "2021-09-10", "1995-03-25", "Warszawa", "ul. Kwiatowa 10", "00-001", "123456789")
student1 = Student("Jan", [60, 70, 80])
student2 = Student("Anna", [40, 50, 60])
student3 = Student("Piotr", [90, 85, 95])
order1 = Order(employee1, student1, [book1, book2], "2023-01-01")
order2 = Order(employee2, student2, [book3, book4], "2023-02-15")
order3 = Order(employee3, student3, [book5], "2023-03-10")

print(order1, order2)
