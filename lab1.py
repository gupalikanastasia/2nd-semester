class Human:
    def __init__(self, name, age):
        self.name = name
        self.__age = age

    def get_age(self):
        return self.__age

    def introduce(self):
        print(f"Привіт! Я {self.name}, мені {self.__age} років.")


class Student(Human):
    def __init__(self, name, age, university):
        super().__init__(name, age)
        self.university = university

    def introduce(self):
        print(f"Привіт! Я {self.name}, я навчаюсь у {self.university}.")

if __name__ == "__main__":
    person = Human("Олег", 40)
    person.introduce()

    student = Student("Анастасія", 19, "ТФК ЛНТУ")
    student.introduce()

    print(f"Вік студента з бази даних:"
          f" {student.get_age()}")