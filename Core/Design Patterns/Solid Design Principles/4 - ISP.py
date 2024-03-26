"""
4 - Interface Segregation Principle
    A class should not be forced to implement methods it doesn't need
"""
from abc import abstractmethod


class Machine:
    def print(self, document):
        raise NotImplementedError

    def fax(self, document):
        raise NotImplementedError

    def scan(self, document):
        raise NotImplementedError

class MultifunctionPrinter(Machine):
    def print(self, document):
        pass

    def fax(self, document):
        pass

    def scan(self, document):
        pass

class OldFashionPrinter(Machine):
    """It cannot fax and scan"""
    def print(self, document):
        pass  # OK

    def fax(self, document):
        pass  # No operation((

    def scan(self, document):
        """Not supported"""
        raise NotImplementedError('This printer cannot scan!')

    # So the problem is that, while somebody will use our OldFashionedPrinter, he will still see those methods.

class Printer:
    @abstractmethod
    def print(self, document): pass


class Scanner:
    @abstractmethod
    def scan(self, document): pass


# same for Fax, etc.

class MyPrinter(Printer):
    def print(self, document):
        print(document)


class Photocopier(Printer, Scanner):
    def print(self, document):
        print(document)

    def scan(self, document):
        pass  # something meaningful


class MultiFunctionDevice(Printer, Scanner):  # Fax, etc
    @abstractmethod
    def print(self, document):
        pass

    @abstractmethod
    def scan(self, document):
        pass
