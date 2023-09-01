from collections import UserDict
import click
from datetime import datetime
import os
import pickle
from functools import partial

pkl_name = "myadressbook.pkl"
pkl_birthday = "birthdays.pkl"

if not os.path.isfile(pkl_name) and not os.path.isfile(pkl_birthday): #створили файл json в якому будемо зберігати дані(імена, номери)
    pkl_file = open(pkl_name, 'wb')
    dic = {'Name': 'Phone number'}
    pickle.dump(dic, pkl_file)
    pkl_file.close()

dic_birthday = {'Name': datetime(year=1991, month=8, day=23)}

def save_address_book(address_book, file_path):
    with open(file_path, 'wb') as pkl_file:
        pickle.dump(address_book, pkl_file)

save_address_book(dic_birthday, pkl_birthday) 
    
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

    @Field.value.setter
    def value(self, new_value):
        if not isinstance(new_value, str):
            raise ValueError("Value must be a string.")
        if not new_value.isdigit() or len(new_value) != 10:
            raise ValueError("Invalid phone number format. Please use a 10-digit number.")
        self._value = new_value

class Birthday(Field):

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

    def open_contacts(self):
        with open(pkl_name, 'rb') as file:
            contacts = pickle.load(file)
        return contacts
    
    
    def load_address_book(self, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as pkl_file:
                loaded_address_book = pickle.load(pkl_file)
                for name, date_str in loaded_address_book.items():
                    loaded_address_book[name] = date_str
            return loaded_address_book
        else:
            return {}


    n = 0
    def __next__(self): 
        self.contacts = self.open_contacts()  
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
        self.contacts = self.open_contacts()
        contact_list = []
        for key_words, key_phones in self.contacts.items():
            if part.lower() in key_words.lower() or part.lower() in key_phones.lower():
                contact_list.append(f'{key_words}:{key_phones}')
        if contact_list == []:
            print("Nothing's found")
        else:
            for contacts in contact_list: print(contacts)

    @input_error 
    def add_birthday(self, name, birthday): # додає день народження контакта
        self.birthday = self.load_address_book(pkl_birthday)
        if len(birthday) != 10:
            raise ValueError("Data must be next format: 2012-12-06.")
        data = birthday.split('-')
        self.birthday[name] = datetime(year=int(data[0]), month=int(data[1]), day=int(data[2]))
        save_address_book(self.birthday, pkl_birthday)
        print(f"{name}'s birthday: {self.birthday[name].year}-{self.birthday[name].month}-{self.birthday[name].day}")
        
    @input_error
    def show_all_contacts(self): #показуе всі контакти
        self.contacts = self.open_contacts()
        if 'Name' in self.contacts:
            self.contacts.pop('Name')
            with open(pkl_name,  'wb') as file:
                pickle.dump(self.contacts, file)
        for name, phone in self.contacts.items():
            print(f"{name} - {phone}")

    @input_error
    def days_to_birthday(self, name): # повертає кількість днів до наступного дня народження.
        self.birthday = self.load_address_book(pkl_birthday)
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
        self.contacts = self.open_contacts()
        if name.lower() in self.contacts:
            print(f'{name.title()}:{self.contacts[name]}')        
        else:
            print(f"There is no {name} in contacts.")
            
                        
class Record():

    def __init__(self, name=None, birthday = None):
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.contacts = AddressBook().open_contacts()
    
    def add_phone(self, phone):
        self.phones.append(phone)
        with open(pkl_name,  'wb') as file:
                pickle.dump(self.contacts, file)

    @input_error #додає контакт
    def add_contact(self, name, phone):
        name_new = Name(name)
        self.contacts[name_new.value] = phone
        with open(pkl_name,  'wb') as file:
            pickle.dump(self.contacts, file)
        print(f"Added contact: {name_new.value} - {phone}")
          
    @input_error #змінює контакт
    def change_contact(self, name, phone):
        if name in self.contacts:
            self.contacts[name] = phone
            with open(pkl_name,  'wb') as file:
                pickle.dump(self.contacts, file)
            print(f"Changed phone for contact {name}")
        else:
            print(f"There is no {name.title()} in contacts.")

    @input_error
    def delete_phone(self, phone):
        key = ''
        for name, value in self.contacts.items():
            if value == phone:
                key += name
        self.contacts.pop(key)
        with open(pkl_name,  'wb') as file:
                pickle.dump(self.contacts, file)
        print('Contact was deleted')

        
def add_contact_command(address_book, name, phone):
    add_contact_curried(address_book, name, phone)

def show_all_command(address_book):
    address_book.show_all_contacts()

def find_command(address_book, part):
    address_book.all(part)

def change_command(contact, name, phone):
    Record().change_contact(name, phone)

def delete_command(contact, name):
    Record().delete_phone(name)

def phone_command(address_book, name):
    address_book.show_phone(name)

def birthday_command(address_book, name):
    address_book.days_to_birthday(name)

def new_birthday_command(address_book, name, data):
    address_book.add_birthday(name, data)

def add_contact_curried(address_book, name, phone):
    name_field = Name(name)
    phone_field = Phone(phone)
    record = Record(name_field)
    record.add_phone(phone_field)
    address_book.add_record(record)
    Record(name).add_contact(name, phone)

def show_page_command(address_book, page):
    page_contacts = AddressBook()
    end = (int(page) * 10) + 1
    text = []
    list_contact = ""
    for i in page_contacts:
        text = i
    for i in text[(end) - 11:(end - 1)]:
        list_contact += i + "\n"
    print(f'Page {page}:\n{list_contact}')

def unknown_command():
    print("Unknown command. Please try again.")

commands = {
    "add": add_contact_command, # work
    "show_all": show_all_command, # work
    "find": find_command, # work
    "change": change_command, #work
    "delete": delete_command, #work
    "phone": phone_command, #work
    "birthday": birthday_command, #work
    "new_birthday": new_birthday_command, # work
    "show_page": show_page_command # work
}

@click.command()
def main():
    address_book = AddressBook()
    add_contact = partial(add_contact_curried, address_book)

    while True:
        command = input("Enter a command: ").lower()
        if command == "hello":
            print("How can I help you?\nMy commands:\n\tadd... - saves the new contact in memory;\n\tfind... - look for all contacts by name and phone number;\n\tchange... - saves the new phone number of the existing contact;\n\tdelete... - delete the contact by phone number;\n\tphone... - displays the phone number for the specified contact;\n\tshow_all - shows all saved contacts with phone numbers;\n\tbirthday... - shows days left till contact's birthday;\n\tnew_birthday... - adds the day of birth ex.(new_birthday Vova 1991-02-18);\n\tshow_page...- shows a page of contacts ex.(show_page 2);\n\tgood bye - close the program.")
        elif command in ("good bye", "close", "exit"):
            print("Good bye! Have a nice day!")
            break
        else:
            parts = command.split()
            if parts[0] in commands:
                func = commands[parts[0]]
                if len(parts) > 1:
                    func(address_book, *parts[1:])
                else:
                    func(address_book)
            else:
                unknown_command()

if __name__ == "__main__":
    main()
