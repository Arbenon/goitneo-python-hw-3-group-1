from datetime import datetime, timedelta
from collections import UserDict
from collections import defaultdict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if len(value) == 10 and value.isdigit():
            super().__init__(value)
        else:
            raise ValueError('Phone number must be 10 digits.')

class Birthday(Field):
    def __init__(self, value):
        if value is not None:
            try:
                datetime.strptime(value, '%d.%m.%Y')
                super().__init__(value)
            except ValueError:
                raise ValueError("Wrong input. Make sure you use the format DD.MM.YYYY.")
        else:
            super().__init__(None)

class Record:
    def __init__(self, name, phone, birthday):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phone = Phone(phone)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        
    def __str__(self):
        return f"Contact name: {self.name.value}, phone: {self.phone}, birthday: {self.birthday}"

class AddressBook(UserDict):

    def add_contact(self, name, phone, birthday=None):
        try:
            self.data[name] = Record(name, phone, birthday)
            return "Contact added."
        except:
            print('Contact was not added. Require 10-digit number and the format DD.MM.YYYY.')
    
    def edit_phone(self, name, new_phone):
        if name in self.data:
            self.data[name].add_phone(new_phone)
            return f"Phone number updated for {name}."
        else:
            return f"No contact found with the name {name}."
        
    def show_all_contacts(self):
        print("All contacts:")
        for record in self.data.values():
            print(record)
    
    def find_phone(self, name):
        if name in self.data:
            return self.data[name].phone
        else:
            return f"No contact found with the name {name}."
        
    def add_birthday(self, name, birthday):
        if name in self.data:
            self.data[name].add_birthday(birthday)
            return f"Birthday added for {name}."
        else:
            return f"No contact found with the name {name}."
        
    def show_birthday(self, name):
        if name in self.data:
            return self.data[name].birthday
        else:
            return f"No contact found with the name {name}."


    def get_birthday_per_week(self):
        present_date = datetime.now()
        day_name_bd = defaultdict(list)
        formatted_birthdays = ''

        for name, record in self.data.items():
            birthday = record.birthday.value
            birthday_this_year = datetime.strptime(birthday, '%d.%m.%Y').replace(year=present_date.year)
        
            day_name = 'Later'

            if birthday_this_year > present_date:
                delta_days = (birthday_this_year - present_date).days
                if 0 <= delta_days < 7:
                    day_name = birthday_this_year.strftime("%A")
                    if day_name == 'Saturday':
                        birthday_this_year += timedelta(days=2)
                    elif day_name == 'Sunday':
                        birthday_this_year += timedelta(days=1)
                    day_name = birthday_this_year.strftime("%A")
                    day_name_bd[day_name].append(name)

        for day, names in day_name_bd.items():
            if names:
                formatted_birthdays += f"{day}: {', '.join(names)}\n"

        return formatted_birthdays.rstrip('\n')

def parse_input(user_input):
    command, *args = user_input.split()
    command = command.strip().lower()
    return command, *args


def main():
    contacts = AddressBook()
    print("Welcome! This is your assistant.")
    while True:
        user_input = input('Enter your command: ')
        try:
            command, *args = parse_input(user_input)

            if command in ['close', 'exit']:                  
                print('Goodbye!')
                break
            elif command == 'hello':                          
                print('How can I help you?')
            elif command == "add":                            
                if len(args) == 2:
                    name, phone = args
                    print(contacts.add_contact(name, phone))
                elif len(args) == 3:
                    name, phone, birthday = args
                    print(contacts.add_contact(name, phone, birthday))
                else:
                    print("Invalid number of arguments. Please provide name and phone (and optional birthday).")
            elif command == "change":
                if len(args) == 2:
                    name, new_phone = args
                    print(contacts.edit_phone(name, new_phone))
                else:
                    print("Invalid number of arguments. Please provide name and new phone.")
            elif command == "all":                                 
                contacts.show_all_contacts()   
            elif command == "phone":                              
                if args:
                    name = args[0]
                    phone = contacts.find_phone(name)
                    if phone:
                        print(f"Phone number for {name}: {phone}")
                    else:
                        print(f"No contact found with the name {name}.")
                else:
                    print("Please provide a name to search for.")
            elif command == "add-birthday":
                if len(args) == 2:
                    name, birthday = args
                    print(contacts.add_birthday(name, birthday))
                else:
                    print("Invalid number of arguments. Please provide name and birthday.")
            elif command == "show-birthday":
                if args:
                    name = args[0]
                    birthday = contacts.show_birthday(name)
                    if birthday:
                        print(f"Birthday for {name}: {birthday}")
                    else:
                        print(f"No birthday found for {name}.")
                else:
                    print("Please provide a name to search for.")    
            elif command == "birthdays":
                print("Birthdays this week:")
                print(contacts.get_birthday_per_week())
            else:
                print('Invalid command.')
                continue
        except:
            print('No input.')

if __name__ == "__main__":
    main()
