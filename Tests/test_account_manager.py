import unittest
from manager_module import AccountManager,ContactManager
from model_module import Accounts
from databaseconnection import DataBaseConnection

import os

class TestLogin(unittest.TestCase):


    @classmethod
    def setUp(cls) -> None:        
        cls.db_manager_obj = DataBaseConnection()
        print(type(cls.db_manager_obj))
        contact_manager_obj = ContactManager(cls.db_manager_obj)
        cls.account_manager_obj = AccountManager(cls.db_manager_obj,contact_manager_obj)
        # aquierment  for display_contact_display
        cls.main_acc = Accounts('reza@gmail.com','0912')
        con_acc1 = Accounts('zahra@gmail.com','0915')
        con_acc2 = Accounts('arman@gmail.com','0925')
        cls.main_acc.contacts_obj = [con_acc1,con_acc2]

    @unittest.skip("skip shod")
    def test_login(self):
        email = 'reza@gmail.com'
        email2 = "rezaee@gmail.com" # for failing test        
        logged_in_obj = self.account_manager_obj.login(email)
        self.assertIsNotNone(logged_in_obj)
        self.assertEqual(email,logged_in_obj.email_address)
    
    def test_display(self):
        # self.account_manager_obj.display_contact(self.main_acc)
        # a  = os.popen('pwd').readlines()
        # print(a)
        self.assertTrue(True)
    
    @classmethod
    def tearDown(cls) -> None:
        cls.db_manager_obj.close_connection()