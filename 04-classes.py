class Human:
    first_name: str
    last_name: str

    def __str__(self):
        return f"Human: {self.name} {self.last_name}"

    def __init__(self, first_name, last_name="Undefined"):
        self.name = first_name
        self.last_name = last_name


class User(Human):
    name: str
    __passport: str = "1234 123123"

    def hello(self):
        print(f"Hello, {self.name}!")


john = User("John", "Doe")

# john.hello()

artur = User("Artur")
# artur.hello()

print(john)
# hello_user(john.name)
# print(john._User__passport)
# john._passport = "123123 "
