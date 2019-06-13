users = ("John", "Artur", "Kate")


def hello_user(name):
    print(f"Hello, {name}!")


def hello_all(user_list):
    for user in user_list:
        hello_user(user)


hello_all(users)


def string_multiple(value, count):
    return value * count


temp_string = string_multiple("Text0", 3)
print(temp_string)
