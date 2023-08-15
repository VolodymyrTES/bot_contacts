from collections import UserDict
import click

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "Invalid input. Please try again."
    return wrapper

class Field:
    def __init__(self, value):
        self.value = value 

class Name(Field):
    pass

class Phone(Field):
    pass

class AddressBook(UserDict):
    contacts = {'Volodymyr': '0637687226', 'Gorbyl': '0637000226', 'Masha': '0687000996'}
    
    def add_record(self, record):
        self.data[record.name.value] = record

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
    def __init__(self, name):
        self.name = name
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(phone)

    @input_error #додає контакт
    def add_contact(self, name, phone):
        self.contacts[name] = phone

        print(f"Added contact: {name} - {phone}")
    
    @input_error #змінює контакт
    def change_contact(self, contact_info):
        name, phone = contact_info.split()
        if name in self.contacts:
            self.contacts[name] = phone
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
        print('Contact was deleted')

                    
@click.command()
def main():
    list = AddressBook()
    while True:
        command = input("Enter a command: ")
        if command.lower() == "hello":
            print("How can I help you?\nMy commands:\n\tadd... - saves the new contact in memory;\n\tchange... - saves the new phone number of the existing contact;\n\tdelete... - delete the contact by phone number;\n\tphone... - displays the phone number for the specified contact;\n\tshow all - shows all saved contacts with phone numbers;\n\tgood bye - close the program.")
        elif command.lower().startswith("add "):
            name, phone = command[4:].split()
            name_field = Name(name)
            phone_field = Phone(phone)
            record = Record(name_field)
            record.add_phone(phone_field)
            list.add_record(record)
            print(f"Added contact: {name} - {phone}")
        elif command.lower() == "show all":
            print(list.contacts)
        elif command.lower().startswith("change "): 
            Record().change_contact(command[7:])
        elif command.lower().startswith('delete '):
            Record().delete_phone(command[7:])
        elif command.lower().startswith("phone "):
            list.show_phone(command[6:])
        elif command.lower() in ("good bye", "close", "exit"):
            print("Good bye! Have a nice day!")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()

