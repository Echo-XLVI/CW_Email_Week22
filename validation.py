import re

class Validation :

    def email_validation (self , email) -> bool :
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if re.fullmatch(regex , email) :
            return True 
        else:
            raise ValueError ("your email is not correct")
        
     