# Prototype

# A partially or fully initialized object that you can copy(clone) and make use of

"""
"Specify the kinds of objects to create using a prototypical instance, and
create new objects by copying this prototype"
                                                @GoF
"""

import copy


class Address:
    def __init__(self, street_address, city, country):
        self.country = country
        self.city = city
        self.street_address = street_address

    def __str__(self):
        return f'{self.street_address}, {self.city}, {self.country}'


class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __str__(self):
        return f'{self.name} lives at {self.address}'


john = Person("John", Address("123 London Road", "London", "UK"))
print(john)
# jane = john
jane = copy.deepcopy(john)
jane.name = "Jane"
jane.address.street_address = "124 London Road"
print(john, jane)

# Summary
'''
- To implement a prototype, partially construct an object and store it somewhere
- Deep copy the prototype
- Customize the resulting instance
- A factory provides a convenient API for using prototypes
'''


