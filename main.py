import os
from  databaseconnection import DataBaseConnection
from manager_module import ContactManager,AccountManager

db_manager_obj = DataBaseConnection()
contact_manager_obj = ContactManager(db_manager_obj)
account_manager_obj = AccountManager(db_manager_obj, contact_manager_obj)

def main():
    email = input('Enter your email address:')
    acc_obj = account_manager_obj.login(email)
    if acc_obj:
        logged_in_menu(acc_obj)
    else:
        print('Entered email doesnt exist!!!')

def wait_for_key():
    input("To continue press enter...")

def contact_menu(acc_obj:object):
    while True:
        os.system('cls')
        print("1.Add contact\n2.Display contact\n3.Exit")
        op=int(input("Choose an option:"))
        match op:
            case 1:
                pass
            case 2:
                account_manager_obj.display_contact(acc_obj)
                wait_for_key()
            case 3:
                break
            case 4:
                print('Invalid Option!!!')



def logged_in_menu(acc_obj:object):
    while True:
        os.system('cls')
        print("1.Send message\n2.Inbox message\n3.Delete message\n4.Contact menu\n5.Exit")
        op=int(input("Choose an option:"))
        match op:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                contact_menu(acc_obj)
            case 5:
                break
            case __:
                print('Invalid Option!!!')


if __name__ == "__main__":
    main()