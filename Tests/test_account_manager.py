import unittest
from manager_module import AccountManager,ContactManager
from model_module import Accounts
from databaseconnection import DataBaseConnection

import os

class TestLogin(unittest.TestCase):


   
    def setUp(self) -> None:        
        self.db_manager_obj = DataBaseConnection()
        print(type(self.db_manager_obj))
        self.contact_manager_obj = ContactManager(self.db_manager_obj)
        self.account_manager_obj = AccountManager(self.db_manager_obj,self.contact_manager_obj)
        # aquierment  for display_contact_display
        self.main_acc = Accounts(acc_id=1,email_address='reza@gmail.com',phone='0912')
        con_acc1 = Accounts(acc_id=3,email_address='zahra@gmail.com',phone='0937')
        con_acc2 = Accounts(acc_id=4,email_address='mehrzad@gmail.com',phone='0912')
        self.main_acc.contacts_obj = [con_acc1,con_acc2]

    @unittest.skip("skip shod")
    def test_login(self):
        email = 'reza@gmail.com'
        email2 = "rezaee@gmail.com" # for failing test        
        logged_in_obj = self.account_manager_obj.login(email)
        self.assertIsNotNone(logged_in_obj)
        self.assertEqual(email,logged_in_obj.email_address)
    
    def test_display(self):
        str1 = self.account_manager_obj.display_contact(self.main_acc)
        self.assertEqual(str1 ,str(self.main_acc.contacts_obj[1]))
        # a  = os.popen('pwd').readlines()
        # print(a)
    #     self.assertTrue(True)


    def test_export_contact(self):
        list_contact = self.contact_manager_obj.export_contact(1)
        print(list_contact)
        print(list_contact[0].email_address)
        print(self.main_acc.contacts_obj[0].email_address)
        self.assertEqual(list_contact[0].email_address ,self.main_acc.contacts_obj[0].email_address )
        # for obj_contact in list_contact :
        #     list_email 
        # for i in  self.main_acc.contacts_obj :
         
    
   
    # def tearDown(self) -> None:
    #     self.db_manager_obj.close_connection()

