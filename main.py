from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Birthday(Field): 
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if value:
            try:
                datetime.strptime(value, "%Y.%m.%d")
            except ValueError as e:
                raise ValueError("Incorrect date format. Please use YYYY.MM.DD") from e
        self.__value = value 


class Name(Field):
    pass

class Phone(Field):
    def validate(self, value):
        if len(value) == 10 and value.isdigit():
            self.value = value
        else:
            raise ValueError("Phone number should be a string of 10 digits")

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"

    def add_phone(self, phone_number: str):
        try:
            phone = Phone(phone_number)
            if phone not in self.phones:
                self.phones.append(phone)
        except ValueError as e:
            raise ValueError("Phone number should be a string of 10 digits") from e

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if phone:
            phone.value = new_phone
        else:
            raise ValueError("Phone number does not exist")

    def remove_phone(self, phone_number):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError("Phone number does not exist")

    def days_to_birthday(self):
        if self.value:
            today = datetime.now().date()
            next_birthday = datetime.strptime(f"{today.year}.{self.value.month}.{self.value.day}", "%Y.%m.%d").date()
            if next_birthday < today:
                next_birthday = datetime.strptime(f"{today.year + 1}.{self.value.month}.{self.value.day}", "%Y.%m.%d").date()
            return (next_birthday - today).days
        return


class AddressBook(UserDict):
    def __init__(self, file):
        super().__init__()
        self.file = file

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def find(self, name):
        return self.data.get(name)

    def __str__(self):
        pass

    def add(self):
        pass

    def iterator(self, item_number):
        counter = 0
        result = ""
        for item,  record in self.data.items():
            result += f"{item}: {record}"
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0 
                result = ""

    def dump(self):
        with open(self.file, "wb") as f:
            pickle.dump(self.data, f)

    def load(self):
        try:
            with open(self.data, "rb") as f:
                self.data = pickle.load(f)
        except FileNotFoundError:
            self.data = {}

    def search_name_and_phone(self):
        query = input("Enter name or phone number to search: ")
        results = []

        for record in self.data.values():   # Search by phone number
            if query.isdigit():
                for phone in record.phones:
                    if query in phone.value:
                        results.append(record)
                        break
            else:   # Search by name
                if query.lower() in record.name.value.lower():
                    results.append(record)

        if results:
            print("Matching contacts found:")
            for idx, record in enumerate(results, start=1):
                print(f"{idx}. {record}")
        else:
            print("No matching contacts found.")