# people = [
#     {"name":"alice","age":22},
#     {"name":"bob","age":16},
#     {"name":"carol","age":30}
# ]


# for person in people:
#     if person["age"] >= 18:
#         print(f"{person['name'].upper()} is an adult.")

# adult_names = [person["name"].upper() for person in people if person["age"] >= 18]
# print(adult_names)
# # Output: ['ALICE', 'CAROL']

# def count_up(n):
#     for i in range(n):
#         yield i

# for x in count_up(3):
#     print(x)
# # 0
# # 1
# # 2


def first_n_squares(n):
    for i in range(n):
        yield i ** 2


a=first_n_squares(5)

print(a)