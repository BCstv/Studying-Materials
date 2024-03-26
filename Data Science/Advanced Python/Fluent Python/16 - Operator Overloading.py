class Number:
    def __init__(self, val: int):
        self.val = val

    def __add__(self, other: 'Number') -> 'Number':
        if isinstance(other, Number):
            return Number(self.val + other.val)
        return NotImplemented

    def __iadd__(self, other: 'Number') -> 'Number':
        if isinstance(other, Number):
            self.val += other.val * 3
            return self
        return NotImplemented

    def __repr__(self) -> str:
        return f'{self.val!r}'

a = Number(12)
b = Number(5)

b += a
print(b)

class Vector:
    def __init__(self, val: list[int]):
        self.vectors = val

    def __matmul__(self, other: 'Vector') -> list:
        if isinstance(other, Vector):
            return list(a * b for a, b in zip(self.vectors, other.vectors))
        return NotImplemented

a = Vector([1, 2, 3])
b = Vector([2, 4, 6])

print(a @ b)
