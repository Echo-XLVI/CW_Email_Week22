class Message:
    def __init__(self, acc_id:int,  subject:str, message:str=None, message_id:int=None):
        self.message_id = message_id
        self.acc_id = acc_id 
        self.subject = subject
        self.message = message
               
class Inbox(Message):
    def __init__(self, from_email_address:str, acc_id:int,  subject:str, message:str=None, message_id:int=None):
        super().__init__(acc_id,subject,message,message_id)
        self.seen = False
        self.from_email_address = from_email_address   

class Sent(Message):
    def __init__(self, to_email_address:str, acc_id:int,  subject:str, message:str=None, message_id:int=None):
        super().__init__(acc_id,subject,message,message_id)
        self.to_email_address = to_email_address   

class Accounts:
    def __init__(self, email_address:str, phone:str, picture:str=None , acc_id:int=None):
        self.acc_id = acc_id
        self.email_address = email_address
        self.phone = phone
        self.picture = picture
        self.contacts_obj = None
        self.inbox = None
    
    def show_inbox(self) -> enumerate:
        print( 50*"-" + " Inbox " + 50*"-")
        for obj,index in enumerate(self.inbox):
            print(100*"-")
            print(f"{index+1}. Subject: {obj.subject}    From: {obj.from_email_address}   Seen: {obj.seen}")

    def __str__(self):
        return f"Email:{self.email_address}\nPhone:{self.phone}"