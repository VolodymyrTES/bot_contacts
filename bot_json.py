from collections import UserDict
import click
from datetime import datetime
import os
import json

json_name = "myadressbook.json"
json_birthday = "birthdays.json"

if not os.path.isfile(json_name) and not os.path.isfile(json_birthday): #створили файл json в якому будемо зберігати дані(імена, номери)
    json_file = open(json_name, 'w')
    dic = {'Name': 'Phone number'}
    json.dump(dic,json_file)
    json_file.close()

dic_birthday = {'Name': datetime(year=1991, month=8, day=23)}

def datetime_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def save_address_book(address_book, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(address_book, json_file, default=datetime_serializer)

save_address_book(dic_birthday, json_birthday) 
    
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "Invalid input. Please try again."
    return wrapper

class Field:
    
    def __init__(self, value):
        self._value = value
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value 

class Name(Field):
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        if not isinstance(new_value, str):
            raise ValueError("Value must be a string.")
        self._value = new_value

class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        if not isinstance(new_value, str):
            raise ValueError("Value must be a string.")
        if not new_value.isdigit() or len(new_value) != 10:
            raise ValueError("Invalid phone number format. Please use a 10-digit number.")
        self._value = new_value

class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, new_value):
        if not isinstance(new_value, str):
            raise ValueError("Value must be a string.")
        try:
            datetime.strptime(new_value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format. Please use the format: YYYY-MM-DD.")
        self._value = new_value
    
class AddressBook(UserDict):

    with open(json_name, 'r') as file:
        contacts = json.load(file)
    
    def load_address_book(file_path):
        try:
            with open(file_path, 'r') as json_file:
                loaded_address_book = json.load(json_file)
                # Deserialize datetime objects from ISO format
                for name, date_str in loaded_address_book.items():
                    loaded_address_book[name] = datetime.fromisoformat(date_str)
            return loaded_address_book
        except FileNotFoundError:
            return {}

    # підгружае файл з json файлу
    birthday = load_address_book(json_birthday)

    n = 0
    def __next__(self):   
        self.n +=1      
        if self.n == 2:
            raise StopIteration
        text = []
        for name_key, phone_value in self.contacts.items():
            text.append(f"{name_key.title()}'s phone number: {phone_value}")      
        return text
                                   
    def __iter__(self):
        return self
    
    def add_record(self, record):
        self.data[record.name.value] = record
        
    @input_error 
    def all(self, part):
        list = []
        for key, value in self.contacts.items():
            if part.lower() in key.lower() or part.lower() in value.lower():
                list.append(f'{key}:{value}')
        if list == []:
            print("Nothing's found")
        else:
            for i in list: print(i)

    @input_error 
    def add_birthday(self, name, birthday): # додає день народження контакта
        if len(birthday) != 10:
            raise ValueError("Data must be next format: 2012-12-06.")
        data = birthday.split('-')
        self.birthday[name] = datetime(year=int(data[0]), month=int(data[1]), day=int(data[2]))
        save_address_book(self.birthday, json_birthday)
        print(f"{name}'s birthday: {self.birthday[name].year}-{self.birthday[name].month}-{self.birthday[name].day}")
        
    @input_error
    def show_all_contacts(self): #показуе всі контакти
        if 'Name' in self.contacts:
            self.contacts.pop('Name')
            with open(json_name,  'w') as file:
                json.dump(self.contacts, file)
        for name, phone in self.contacts.items():
            print(f"{name} - {phone}")

    @input_error
    def days_to_birthday(self, name): # повертає кількість днів до наступного дня народження.
        if name not in self.birthday:
            print("the contact doesn't exist")
        else:
            current_date = datetime.now() #сьогоднішня дата
            contact_birthday = self.birthday.get(name)
            day_1 = datetime(year=current_date.year, month=contact_birthday.month, day=contact_birthday.day)
            if current_date.month <= (day_1.month): 
                delta = day_1 - current_date # визначення дельти(різниця між поточною датою і датою дня народження контакту)
                print(f"{name}'s birthday is in {delta.days} days.")
            else: # Якщо день народження контакту вже в наступному році 
                day_1 = datetime(year=current_date.year+1, month=contact_birthday.month, day=contact_birthday.day)
                delta = day_1 - current_date 
                print(f"{name}'s birthday is in {delta.days} days.")

    @input_error #показуе введений контакт
    def show_phone(self, name):
        for key, value in self.contacts.items():
            if name.lower() == key.lower():
                print(f"{name.title()}'s phone number: {value}")
                break
            else:
                print(f"There is no {name} in contacts.")
                break
                

class Record(AddressBook):
    def __init__(self, name=None, birthday = None): #додаємо поле birthday у випадку якщо користувач додае дату народження нового контакту у вигляді "2000-01-15"
        self.name = name
        self.phones = []
        self.birthday = birthday
    

    def add_phone(self, phone):
        self.phones.append(phone)
        with open(json_name,  'w') as file:
                json.dump(self.contacts, file)

    @input_error #додає контакт
    def add_contact(self, name, phone):
        name_new = Name(name)
        self.contacts[name_new.value] = phone
        with open(json_name,  'w') as file:
            json.dump(self.contacts, file)
        print(f"Added contact: {name_new.value} - {phone}")
          
    @input_error #змінює контакт
    def change_contact(self, contact_info):
        name, phone = contact_info.split()
        if name in self.contacts:
            self.contacts[name] = phone
            with open(json_name,  'w') as file:
                json.dump(self.contacts, file)
            print(f"Changed phone for contact {name}")
        else:
            print(f"There is no {name} in contacts.")

    @input_error
    def delete_phone(self, phone):
        key = ''
        for name, value in self.contacts.items():
            if value == phone:
                key += name
        self.contacts.pop(key)
        with open(json_name,  'w') as file:
                json.dump(self.contacts, file)
        print('Contact was deleted')

                    
@click.command()
def main():
    list = AddressBook()
    
    while True:
        command = input("Enter a command: ")
        if command.lower() == "hello":
            print("How can I help you?\nMy commands:\n\tadd... - saves the new contact in memory;\n\tfind... - look for all contacts by name and phone number;\n\tchange... - saves the new phone number of the existing contact;\n\tdelete... - delete the contact by phone number;\n\tphone... - displays the phone number for the specified contact;\n\tshow all - shows all saved contacts with phone numbers;\n\tbirthday... - shows days left till contact's birthday;\n\tnew birthday... - adds the day of birth ex.(new birthday Vova 1991-02-18);\n\tshow page...- shows a page of contacts ex.(show page 2);\n\tgood bye - close the program.")

        elif command.lower().startswith("add "):
            name, phone = command[4:].split()
            name_field = Name(name)
            phone_field = Phone(phone)
            record = Record(name_field)
            record.add_phone(phone_field)
            list.add_record(record)
            Record(name).add_contact(name, phone)

        elif command.lower() == "show all":
            AddressBook().show_all_contacts()
        
        elif command.lower().startswith("find "):
            AddressBook().all(command[5:])

        elif command.lower().startswith("change "): 
            Record().change_contact(command[7:])

        elif command.lower().startswith('delete '):
            Record().delete_phone(command[7:])

        elif command.lower().startswith("phone "):
            list.show_phone(command[6:])

        elif command.lower().startswith("birthday "):
            AddressBook().days_to_birthday(command[9:])

        elif command.lower().startswith("new birthday "):
            try:
                name, data = command[13:].split(' ')
                AddressBook().add_birthday(name, data)
            except ValueError:
                print("Wrong format! it's supposed to be: new birthday Volodymyr 1991-18-02.")

        elif command.lower().startswith('show page '): #Додамо пагінацію (посторінковий висновок) для AddressBook для ситуацій, коли книга дуже велика і треба показати вміст частинами, а не все одразу. Реалізуємо це через створення ітератора за записами.
            page_contacts = AddressBook()
            page = int(command[10:]) # 1page = 2 contact
            end = (page*10) +1
            text = []
            list_contact = ""
            for i in page_contacts:
                text = i
            for i in text[(end)-11:(end-1)]:
                list_contact += i+"\n"
            print(f'Page {page}:\n{list_contact}')
            
        elif command.lower() in ("good bye", "close", "exit"):
            print("Good bye! Have a nice day!")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()

