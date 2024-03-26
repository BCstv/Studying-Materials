"""
S - Single Responsibility Principle (Separation of Concerns)
    If you have a class, that class should have its primary responsibility, whatever it's meant to be doing, and it
    should not take on other responsibilities
"""

class Journal:
    def __init__(self):
        self.entries = []
        self.count = 0

    def add_entry(self, text):
        self.entries.append(f"{self.count}: {text}")
        self.count += 1

    def remove_entry(self, pos):
        del self.entries[pos]

    def __str__(self):
        return "\n".join(self.entries)

    # break SRP, because save, load, and load_from_web are not class' responsibilities
    def save(self, filename):
        file = open(filename, "w")
        file.write(str(self))
        file.close()

    def load(self, filename):
        pass

    def load_from_web(self, uri):
        pass


class PersistenceManager:
    @staticmethod
    def save(journal, filename):
        file = open(filename, "w")
        file.write(str(journal))
        file.close()

    @staticmethod
    def load(journal, filename):
        pass

    @staticmethod
    def load_from_web(uri):
        pass


j = Journal()
j.add_entry("I cried today.")
j.add_entry("I ate a bug.")
print(f"Journal entries:\n{j}\n")

p = PersistenceManager()
file = r'c:\temp\journal.txt'
p.save(j, file)

# verify!
with open(file) as fh:
    print(fh.read())


















