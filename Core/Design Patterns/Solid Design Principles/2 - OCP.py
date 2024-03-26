"""
2 - Open-Closed Principle
    open for extension, closed for modification
"""

from enum import Enum, auto


class Color(Enum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()


class Size(Enum):
    SMALL = auto()
    MEDIUM = auto()
    LARGE = auto()


class Product:
    def __init__(self, name, color, size):
        self.name = name
        self.color = color
        self.size = size


class ProductFilter:
    def filter_by_color(self, products, color):
        for p in products:
            if p.color == color: yield p

    # After the class was written, it cannot be modified, only extended:
    def filter_by_size(self, products, size):
        for p in products:
            if p.size == size: yield p

    def filter_by_color_and_size(self, products, size, color):
        for p in products:
            if p.color == color and p.size == size: yield p

    # But what if we need more filters? In this example the maximum value of filter's permutations is 3 (c, s, cs)
    # But if we had 3 different filters, this number would increase up to 7 (c, s, w, cs, cw, sw, csw)


# So let's use the specification pattern:

class Specification:
    def is_satisfied(self, product):
        pass


class Filter:
    def filter(self, items, spec):
        pass


class ColorSpecification(Specification):
    def __init__(self, color):
        self.color = color

    def is_satisfied(self, product):
        return product.color == self.color


class SizeSpecification(Specification):
    def __init__(self, size):
        self.size = size

    def is_satisfied(self, product):
        return product.size == self.size


class AndSpecification(Specification):
    def __init__(self, *args):
        self.args = args

    def is_satisfied(self, product):
        return all(map(
            lambda spec: spec.is_satisfied(product), self.args
        ))


class BetterFilter(Filter):
    def filter(self, items, spec):
        for item in items:
            if spec.is_satisfied(item):
                yield item


if __name__ == '__main__':
    apple = Product('Apple', Color.GREEN, Size.SMALL)
    tree = Product('Tree', Color.GREEN, Size.LARGE)
    house = Product('House', Color.BLUE, Size.LARGE)

    products = [apple, tree, house]

    pf = ProductFilter()
    print('Green products (old): ')
    for p in pf.filter_by_color(products, Color.GREEN):
        print(f' - {p.name} is Green')

    bf = BetterFilter()
    print('Green products (new):')
    for p in bf.filter(products, ColorSpecification(Color.GREEN)):
        print(f' - {p.name} is Green')

    print('Large Blue items: ')
    large_blue = AndSpecification(SizeSpecification(Size.LARGE), ColorSpecification(Color.BLUE))
    for p in bf.filter(products, large_blue):
        print(f' - {p.name} is Blue and Large')

    