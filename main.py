from dataclasses import dataclass
from datetime import datetime

# what is @dataclass?The `@dataclass` decorator in Python is used to automatically generate special methods for classes, such as `__init__`, `__repr__`, `__eq__`, 
# and others, based on the class attributes..
# It simplifies the creation of classes that are primarily used to store data by reducing boilerplate code.

@dataclass
class Task:
    title: str
    done: bool = False
    created_at: datetime = datetime.now()

    def summary(self) -> str:
        status = "done" if self.done else "pending"
        return f"{self.title} ({status})"


def main() -> None:
    tasks = [
        Task("Learn Python"),
        Task("Build a project", done=True),
        Task("Set up dev environment", done=True),
    ]
    for t in tasks:
        print(t.summary())


if __name__ == "__main__":
    main()