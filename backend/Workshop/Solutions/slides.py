# ====================
# *ARGS / **KWARGS
# ====================

from contextlib import contextmanager
import asyncio
from functools import lru_cache, partial
from dataclasses import dataclass


def greet(*args):
    for name in args:
        print(f"Hello {name}")


greet("Buddy", "Max", "Bella")


def create_pet(**kwargs):
    print(kwargs)


create_pet(name="Buddy", age=3, animal="dog")


def flexible(required, *args, **kwargs):
    print(required)
    print(args)
    print(kwargs)


flexible("first", "extra1", "extra2", option=True, count=5)


# ====================
# LAMBDA
# ====================

def add(x, y): return x + y


print(add(2, 3))

pets = [{"name": "Buddy", "age": 3}, {"name": "Max", "age": 7}]

sorted_pets = sorted(pets, key=lambda p: p["age"])
print(sorted_pets)


# ====================
# TYPE HINTS
# ====================

def greet(name: str) -> str:
    return f"Hello {name}"


def add(a: int, b: int) -> int:
    return a + b


names: list[str] = ["Buddy", "Max"]
ages: dict[str, int] = {"Buddy": 3, "Max": 7}


# ====================
# CLASSES + __init__
# ====================

class Pet:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def speak(self) -> str:
        return f"{self.name} says hello"


buddy = Pet("Buddy", 3)
print(buddy.name)
print(buddy.speak())


# ====================
# INHERITANCE
# ====================

class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "..."


class Dog(Animal):
    def speak(self) -> str:
        return f"{self.name} says woof"


class Cat(Animal):
    def speak(self) -> str:
        return f"{self.name} says meow"


dog = Dog("Buddy")
cat = Cat("Whiskers")
print(dog.speak())
print(cat.speak())


# ====================
# @PROPERTY
# ====================

class Circle:
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:
        return self._radius

    @radius.setter
    def radius(self, value: float):
        if value < 0:
            raise ValueError("no negative radius")
        self._radius = value

    @property
    def area(self) -> float:
        return 3.14 * self._radius ** 2


c = Circle(5)
print(c.area)
c.radius = 10
print(c.area)


# ====================
# @CLASSMETHOD / @STATICMETHOD
# ====================

class Pet:
    count = 0

    def __init__(self, name: str):
        self.name = name
        Pet.count += 1

    @classmethod
    def get_count(cls) -> int:
        return cls.count

    @staticmethod
    def is_valid_name(name: str) -> bool:
        return len(name) > 0


print(Pet.is_valid_name("Buddy"))
p1 = Pet("Buddy")
p2 = Pet("Max")
print(Pet.get_count())


# ====================
# DUNDER METHODS
# ====================

class Pet:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return f"{self.name} ({self.age})"

    def __repr__(self) -> str:
        return f"Pet('{self.name}', {self.age})"

    def __eq__(self, other) -> bool:
        return self.name == other.name

    def __lt__(self, other) -> bool:
        return self.age < other.age


buddy = Pet("Buddy", 3)
print(buddy)
print(repr(buddy))


# ====================
# DATACLASSES
# ====================


@dataclass
class Pet:
    name: str
    age: int
    animal: str = "dog"


buddy = Pet("Buddy", 3)
print(buddy)
print(buddy.name)


# ====================
# DECORATORS
# ====================

def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper


@log_call
def greet(name):
    return f"Hello {name}"


print(greet("Buddy"))


# ====================
# DECORATORS WITH ARGS
# ====================

def repeat(times: int):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator


@repeat(3)
def say_hello():
    print("hello")


say_hello()


# ====================
# FUNCTOOLS
# ====================


@lru_cache(maxsize=100)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


print(fib(30))


def greet(greeting, name):
    print(f"{greeting}, {name}")


say_hello = partial(greet, "Hello")
say_hello("Buddy")


# ====================
# LIST COMPREHENSION
# ====================

nums = [1, 2, 3, 4, 5]

squares = [n * n for n in nums]
print(squares)

evens = [n for n in nums if n % 2 == 0]
print(evens)


# ====================
# DICT COMPREHENSION
# ====================

names = ["Buddy", "Max", "Bella"]

name_lengths = {name: len(name) for name in names}
print(name_lengths)


# ====================
# SET COMPREHENSION
# ====================

nums = [1, 2, 2, 3, 3, 3]

unique_squares = {n * n for n in nums}
print(unique_squares)


# ====================
# MAP / FILTER
# ====================

nums = [1, 2, 3, 4, 5]

squares = list(map(lambda x: x * x, nums))
print(squares)

evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)


# ====================
# ENUMERATE / ZIP
# ====================

names = ["Buddy", "Max", "Bella"]

for i, name in enumerate(names):
    print(i, name)


ages = [3, 7, 2]

for name, age in zip(names, ages):
    print(f"{name} is {age}")


# ====================
# UNPACKING
# ====================

a, b, c = [1, 2, 3]
print(a, b, c)

first, *rest = [1, 2, 3, 4, 5]
print(first)
print(rest)

*start, last = [1, 2, 3, 4, 5]
print(start)
print(last)

d1 = {"a": 1}
d2 = {"b": 2}
merged = {**d1, **d2}
print(merged)


# ====================
# WALRUS OPERATOR
# ====================

nums = [1, 2, 3, 4, 5]

if (n := len(nums)) > 3:
    print(f"list has {n} items")

results = [y for x in nums if (y := x * 2) > 4]
print(results)


# ====================
# MATCH / CASE
# ====================

def handle(action: str):
    match action:
        case "start":
            print("starting")
        case "stop":
            print("stopping")
        case _:
            print("unknown")


handle("start")
handle("other")


def parse(data):
    match data:
        case {"type": "pet", "name": name}:
            print(f"pet named {name}")
        case [first, *rest]:
            print(f"list starting with {first}")
        case _:
            print("no match")


parse({"type": "pet", "name": "Buddy"})
parse([1, 2, 3])


# ====================
# TRY / EXCEPT
# ====================

try:
    x = 1 / 0
except ZeroDivisionError:
    print("cant divide by zero")
finally:
    print("always runs")


try:
    x = int("not a number")
except ValueError as e:
    print(f"error: {e}")


# ====================
# RAISE EXCEPTIONS
# ====================

def set_age(age: int):
    if age < 0:
        raise ValueError("age cant be negative")
    return age


try:
    set_age(-5)
except ValueError as e:
    print(e)


# ====================
# ASYNC / AWAIT
# ====================


async def fetch_data():
    print("fetching...")
    await asyncio.sleep(1)
    print("done")
    return {"data": 123}


async def main():
    result = await fetch_data()
    print(result)


asyncio.run(main())


# ====================
# ASYNC GATHER
# ====================

async def fetch(name, delay):
    await asyncio.sleep(delay)
    return f"{name} finished"


async def main():
    results = await asyncio.gather(
        fetch("task1", 2),
        fetch("task2", 1),
        fetch("task3", 3),
    )
    print(results)


asyncio.run(main())


# ====================
# CONTEXT MANAGERS
# ====================

with open("example.txt", "w") as f:
    f.write("hello")


class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, *args):
        import time
        print(f"took {time.time() - self.start:.2f}s")


with Timer():
    for i in range(1000000):
        pass


# ====================
# CONTEXTLIB
# ====================


@contextmanager
def timer():
    import time
    start = time.time()
    yield
    print(f"took {time.time() - start:.2f}s")


with timer():
    for i in range(1000000):
        pass


# ====================
# GENERATORS
# ====================

def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1


for num in count_up(5):
    print(num)


# ====================
# GENERATOR EXPRESSIONS
# ====================

nums = [1, 2, 3, 4, 5]

squares = (n * n for n in nums)

for s in squares:
    print(s)


# ====================
# SLOTS
# ====================

class Pet:
    __slots__ = ["name", "age"]

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


buddy = Pet("Buddy", 3)
print(buddy.name)
