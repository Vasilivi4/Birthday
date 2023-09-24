from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def validate(self):
        pass


class Phone(Field):
    def validate(self):
        if not isinstance(self.value, str):
            raise ValueError("Phone must be a string")

        for char in self.value:
            if char not in "0123456789-":
                raise ValueError("Phone number can only contain digits and hyphens")

        if not (7 <= len(self.value) <= 15):
            raise ValueError("Phone number must be between 7 and 15 characters long")


class Birthday(Field):
    def validate(self):
        if not isinstance(self.value, datetime):
            raise ValueError("Birthday must be a datetime object")

        if self.value > datetime.now():
            raise ValueError("Birthday cannot be in the future")

        if self.value.year < 1900:
            raise ValueError("Year of birth cannot be earlier than 1900")

        try:
            self.value.replace(year=datetime.now().year)
        except ValueError:
            raise ValueError("Invalid day or month in the birthday date")


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now()
            next_birthday = self.birthday.value.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_until_birthday = (next_birthday - today).days
            return days_until_birthday
        return None


class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def iterator(self, N):
        for i in range(0, len(self.records), N):
            yield self.records[i : i + N]


record1 = Record("Num Doe", Phone("123-456-7890"), Birthday(datetime(1990, 10, 23)))
record2 = Record(
    "Shevelov Olecsander", Phone("096-840-8018"), Birthday(datetime(1988, 4, 16))
)
record3 = Record("Shyrik Nom", Phone("555-555-5555"), Birthday(datetime(1988, 2, 19)))

address_book = AddressBook()
address_book.add_record(record1)
address_book.add_record(record2)
address_book.add_record(record3)

for page in address_book.iterator(1):
    for record in page:
        print(f"Name: {record.name}")
        if record.phone:
            print(f"Phone: {record.phone}")
        days_to_birthday = record.days_to_birthday()
        if days_to_birthday is not None:
            print(f"Days to Birthday: {days_to_birthday}")
    print()
