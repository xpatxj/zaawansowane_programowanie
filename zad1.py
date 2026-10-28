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
        if srednia > 50:
            return True
        else:
            return False


student1 = Student("Jan", [60, 70, 80])
print(student1.is_passed())

student2 = Student("Anna", [40, 50, 60])
print(student2.is_passed())
