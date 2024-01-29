# ---------------------------------------------------TypedDict----------------------------------------------------------
from typing import TypedDict


class AppInfo(TypedDict, total=False):
    title: str
    description: str
    version: int


def getinfo() -> AppInfo:
    return AppInfo(title='Telegram', description='app', version=1)


a: AppInfo = getinfo()
print(a['title'])
print(a['description'])  # In the key field it gives me some hints using which, it's clear if the dict does have them


class MediaRating(TypedDict,
                  total=False):  # if total is true, so the object requires to name all it's variables on call
    title: str
    stars: int
    app: AppInfo


c = MediaRating(
    title="random",
    stars=5,
    app=AppInfo(title="Telegram",
                description="App",
                version=1)
)
b = MediaRating(title='Vanya')
print(c)

# --------------------------------------------------NewType-------------------------------------------------------------
from typing import NewType

Versioa = NewType('Version', float)
ut = Versioa(1.2)
print(ut, '-', type(ut))
upgrade: float = 1.0
print(ut + upgrade)

# WARNING  WARNING  WARNING  WARNING  WARNING  WARNING   WARNING  WARNING   WARNING  WARNING  WARNING  WARNING WARNING
# Python 3.12 supports NewType from the box using type command

type x = tuple[float, float]
type y = list[list[str | float]]

am: y = [[1.1, 2]]
print(type(am[0][0]))
ma: x = (1.2, 1.2)

# 1.2.3
class Version:
    def __init__(self, major: int = 0, minor: int = 0, patch: int = 0) -> None:
        self.major = major
        self.minor = minor
        self.patch = patch

    def major_update(self, upval: int = 1) -> None:
        self.major += upval

    def minor_update(self, upval: int = 1) -> None:
        self.minor += upval

    def patch_update(self, upval: int = 1) -> None:
        self.patch += upval

    def __add__(self, other):
        return Version(self.major + other.major, self.minor + other.minor, self.patch + other.patch)

    def __sub__(self, other):
        return Version(self.major - other.major, self.minor - other.minor, self.patch - other.patch)

    def __repr__(self) -> str:
        return f'Version({self.major!r}.{self.minor!r}.{self.patch!r})'


Vc = Version()
Vc.major_update()
Vc.minor_update(4)
Vc.patch_update(6)

anVc = Version(major=3)

print(Vc + anVc)
print(Vc - anVc)


from typing import Type
type a = list[str]

print(type(a))
