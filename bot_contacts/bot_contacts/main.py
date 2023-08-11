import click

contacts = {'Volodymyr': '0637687226', 'Gorbyl': '0637000226', 'Masha': '0687000996'}

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError):
            return "Invalid input. Please try again."
    return wrapper


@input_error #додає контакт
def add_contact(contact_info):
    name, phone = contact_info.split()
    contacts[name] = phone
    print(f"Added contact: {name} - {phone}")

@input_error #змінює контакт
def change_contact(contact_info):
    name, phone = contact_info.split()
    if name in contacts:
        contacts[name] = phone
        print(f"Changed phone for contact {name}")
    else:
        print(f"There is no {name} in contacts.")

@input_error #показуе введений контакт
def show_phone(name):
    if name in contacts:
        print(f"{name}'s phone number: {contacts[name]}")
    else:
        print(f"There is no {name} in contacts.")

def show_all_contacts(): #показуе всі контакти
    for name, phone in contacts.items():
        print(f"{name} - {phone}")


@click.command()
def main():
    while True:
        command = input("Enter a command: ").lower()
        if command == "hello":
            print("How can I help you?\nMy commands:\n\tadd... - saves the new contact in memory;\n\tchange... - saves the new phone number of the existing contact;\n\tphone... - displays the phone number for the specified contact;\n\tshow all - shows all saved contacts with phone numbers;\n\tgood bye - close the program.")
        elif command.startswith("add "):
            add_contact(command[4:])
        elif command.startswith("change "):
            change_contact(command[7:])
        elif command.startswith("phone "):
            show_phone(command[6:])
        elif command == "show all":
            show_all_contacts()
        elif command in ("good bye", "close", "exit"):
            print("Good bye! Have a nice day!")
            break
        else:
            print("Unknown command. Please try again.")

if __name__ == "__main__":
    main()
#OPTIONS = {"add ":add_contact,"change ":change_contact,"phone ":show_phone}
