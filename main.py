import os
from  databaseconnection import DataBaseConnection
from manager_module import ContactManager,AccountManager,SentManager,InboxManager
from validation import Validation

db_manager_obj = DataBaseConnection()
contact_manager_obj = ContactManager(db_manager_obj)
account_manager_obj = AccountManager(db_manager_obj, contact_manager_obj)
inbox_manager_obj = InboxManager(db_manager_obj)
send_manager_obj = SentManager(db_manager_obj)

def main():

    email = input('Enter your email address:')
    Validation.email_validation(email=email)
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


def send_massage(acc_obj:object):
    # origin_acc_obj, send_message , subject , to_email 
    to_email = input("enter email that want to send message ")
    subject = input("enter subject ")
    if not subject :
        raise ValueError ("subject is neccesary")
    send_massage = input("enter message ")
    send_manager_obj.send_message(subject = subject , to_email = to_email , send_message = send_massage)

def delete(acc_obj:object):
    inbox_manager_obj.delete_message(acc_obj)

def logged_in_menu(acc_obj:object):
    inbox_manager_obj.recieve_message(acc_obj)
    while True:
        os.system('cls')
        print("1.Send message\n2.Inbox message\n3.Delete message\n4.Contact menu\n5.Show Trash\n6.Exit")
        op=int(input("Choose an option:"))
        match op:
            case 1:
                pass
            case 2:
                acc_obj.show_inbox()
                message_index = int(input("Choose an email:"))
                ## TODO: showing a message with mote detail
            case 3:
                pass
            case 4:
                contact_menu(acc_obj)
            case 5:
                db_manager_obj.show_trash(acc_obj)
            case 6:
                break
            case __:
                print('Invalid Option!!!')


if __name__ == "__main__":
    main()