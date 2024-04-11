"""When piecewise object construction is complicated, provide an API for doing it succinctly"""

# ----------------------------------------------------------------------------------------------------------------------

# Builder

"""
"Separate the construction of a complex object from its representation so
that the same construction process can create different representations."
                                    @GoF
"""

class HtmlElement:
    indent_size = 2

    def __init__(self, name='', text=''):
        self.name = name
        self.text = text
        self.elements = []

    def __str(self, indent):
        lines = []
        i = ' ' * (indent * self.indent_size)
        lines.append(f'{i}<{self.name}>')

        if self.text:
            i1 = ' ' * ((indent + 1) * self.indent_size)
            lines.append(f'{i1}{self.text}')

        for e in self.elements:
            lines.append(e.__str(indent + 1))

        lines.append(f'{i}</{self.name}>')
        return '\n'.join(lines)

    def __str__(self):
        return self.__str(0)

    @staticmethod  # It breaks the second SOLID principle, but it's fine
    def create(name):
        return HtmlBuilder(name)

class HtmlBuilder:
    def __init__(self, root_name):
        self.__root = HtmlElement(root_name)

    def add_child(self, child_name, child_text):
        self.__root.elements.append(
            HtmlElement(name=child_name, text=child_text)
        )

    def add_child_fluent(self, child_name, child_text):
        self.__root.elements.append(
            HtmlElement(name=child_name, text=child_text)
        )
        return self

    def __str__(self):
        return str(self.__root)

builder1 = HtmlElement.create('ul')  # HtmlBuilder is getting invoked right from the HtmlElement

builder1.add_child_fluent('li', 'hello').add_child('li', 'world')
# return self in add_child_fluent allows to call method few times on itself

print(builder1)
# str() is not required, because it is already called in Builder's __str__

# ----------------------------------------------------------------------------------------------------------------------

# Builder Facets

# Some objects are that complicated that you actually need more than one builder to do this
# How to make a nice database which will allow us to jump between different builders?

class Person:
    def __init__(self):
        # address
        self.street_address = None
        self.postcode = None
        self.city = None
        # employment
        self.company_name = None
        self.position = None
        self.annual_income = None

    def __str__(self):
        return f'Address: {self.street_address}, {self.postcode}, {self.city} \n' + \
               f'Employed at {self.company_name} as a {self.position}, earning {self.annual_income}'

# We want to have two separate builders. One for an address information, and another one for an employment

class PersonBuilder:  # Facade
    def __init__(self, person=None):
        if person is None:
            self.person = Person()
        else:
            self.person = person  # Creating a person in the header of initialization creates one Person object for all manipulations

    # Two jumpers to jump from one builder to another

    @property
    def works(self):
        return PersonJobBuilder(self.person)

    @property
    def lives(self):
        return PersonAddressBuilder(self.person)

    def build(self):
        return self.person

class PersonJobBuilder(PersonBuilder):

    def at(self, company_name):
        self.person.company_name = company_name
        return self  # It is called a 'fluent interface'

    def position(self, position):
        self.person.position = position
        return self

    def earning(self, annual_income):
        self.person.annual_income = annual_income
        return self

class PersonAddressBuilder(PersonBuilder):

    def at(self, street_address):
        self.person.street_address = street_address
        return self

    def with_postcode(self, postcode):
        self.person.postcode = postcode
        return self

    def in_city(self, city):
        self.person.city = city
        return self


pb = PersonBuilder()
person = pb \
        .lives \
            .at('123 road')\
            .in_city('Miami')\
            .with_postcode('65000')\
        .works\
            .at('Google')\
            .position('Team Lead')\
            .earning(210_000)\
    .build()

print(person)

# ----------------------------------------------------------------------------------------------------------------------

# Builder Inheritance

# What if you want to add additional builder which customize more and more of the object

class Person:
    def __init__(self):
        self.name = None
        self.position = None
        self.date_of_birth = None

    def __str__(self):
        return f'{self.name} - {self.date_of_birth} \n' \
            + f'Position: {self.position} \n'

    @staticmethod
    def new():
        return PersonBuilder()

class PersonBuilder:
    def __init__(self):
        self.person = Person()

    def build(self):
        return self.person

class PersonInfoBuilder(PersonBuilder):
    def called(self, name):
        self.person.name = name
        return self

class PersonJobBuilder(PersonInfoBuilder):
    def works_as_a(self, position):
        self.person.position = position
        return self

class PersonBirthDateBuilder(PersonJobBuilder):
    def born(self, date_of_birth):
        self.person.date_of_birth = date_of_birth
        return self

pb = PersonBirthDateBuilder()  # One of the main builder's children
me = pb\
        .called('Stas') \
        .born('2006') \
        .works_as_a('Software Engineer').build()
print(me)


# Every single one of those builders are satisfying for the second SOLID principle, which is the main priority

# TEST

class CodeBuilder:
    def __init__(self, root_name):
        self.root_name = root_name
        self.fields = ['  pass']

    def add_field(self, type, name):
        if len(self.fields) == 1:
            self.fields = ['  def __init__(self):']
        self.fields.append(f'    self.{type} = {name}')
        return self

    def __str__(self):
        return '\n'.join([f'class {self.root_name}:'] + self.fields)

cb = CodeBuilder('Stas')
print(cb)

# SUCCESS

# Summary
"""
- A builder is a separate component for building an object
- Can either give builder an initializer or return it via a static function 
- To make builder fluent, return self
- Different facets of an object can be built with a different builders working in tandem via a base class
"""


