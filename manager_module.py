from model_module import Accounts, Inbox, Sent

class ModelManager:
    def __init__(self, db_manager_obj, table_name, model_class):
        self.db_manager_obj = db_manager_obj
        self.table_name = table_name
        self.model_class = model_class
    
    def insert(self, **kwargs):
        """
            kwargs : {user_id:1,acc_id:2}}
        """
        base_query = f'Insert Into {self.table_name}'
        table_columns = ','.join([key for key in kwargs.keys()])
        values = ','.join([val for val in kwargs.keys()])
        query = f"{base_query} ({table_columns}) values ({values})"
        print(query)

    def delete(self, **kwargs):
        """
            kwargs: contain where clause {column:value}
        """
        base_query =f"DELETE FROM {self.table_name} WHERE"
        where_condition="and".join([f"{key} = %s" for key in kwargs['where'].keys()])
        query= base_query + where_condition
        with self.db_manager_obj as db:
            db.cursor.execute(query)
    
    def select(self, where_clause:dict=None) -> list:
        basic_query=f"Select * from {self.table_name}"
        if where_clause:
            where_condition=' and '.join([f"{key} = %s" for key in where_clause.keys()])
            params = tuple([val for val in where_clause.values()])
            query=basic_query+' WHERE '+where_condition   
        else:
            query=basic_query 
        with self.db_manager_obj as db:
            db.cursor.execute(query,params)
            rows = db.cursor.fetchone()
            columns = [desc[0] for desc in db.cursor.description]
        return dict(zip(columns,rows))

    def filter(self, **kwargs):
        # key_value={'name':'ali'}
        # key_value={'email':'ali@yahoo.com', 'phone_number': '01912234'}
        base_query = f"select * from {self.table_name} where"
        conditional_query = " and ".join([f"{key} = %s" for key in kwargs.keys()])
        query = base_query + conditional_query
        params = tuple(kwargs.values())
        with self.db_manager_obj as db:        
            db.execute_query(query, params)
            rows = db.fetch_all()       # list of tuples
        
        if rows:
            q = f"Select * FROM {self.table_name} LIMIT 0"
            # اتصال به دیتابیس
            with self.db_manager as db:
                # اجرای کویری
                db.execute_query(q)
                # گرفتن نام های ستون های جدول بصورت لیست
                colnames = [desc[0] for desc in db.cursor.description] 
        return [zip(colnames,row) for row in rows]

    def update(self, **kwargs):
        """
            kwarg: contain set clause and where clause {set:{column:value},where:{column:value}}"
        """
        base_query=f"UPDATE {self.table_name}"
        set_condition=",".join([f"{key} = %s" for key in kwargs['set'].keys()])
        param_set=tuple([val for val in kwargs['set'].values()])
        where_condition=" and ".join([f"{key} = %s" for key in kwargs['where'].keys()])
        param_where=tuple([val for val in kwargs['where'].values()])
        query=base_query + ' SET ' + set_condition + ' WHERE ' + where_condition
        print(param_set+param_where)
        with self.db_manager as db:
            db.cursor.execute(query,param_set+param_where)

    def join_contact(self, parent_id:int) -> list:
        query=""" select * from accounts a where a.acc_id in (select child_id from contacts c inner join accounts acc 
                  on acc.acc_id = c.parent_id where c.parent_id=%s)     
              """
        with self.db_manager_obj as db:
            db.cursor.execute(query,(parent_id,))
            result = db.cursor.fetchall()
            columns = [desc[0] for desc in db.cursor.description]
        return [dict(zip(columns,row)) for row in result]

class AccountManager(ModelManager):
    def __init__(self, db_manager_obj:object, contact_manager_obj:object):
        super().__init__(db_manager_obj, 'accounts', Accounts)
        self.contact_manager_obj = contact_manager_obj

    def login(self , email:str) -> object: 
        res=self.select({'email_address':email})  # res =[()]
        if res:
            logged_account = self.model_class(**res)
            # print(logged_account)                   # Baraye khanom Montahaee (XD Didin shod!!!!!)
            logged_account.contacts_obj=self.contact_manager_obj.export_contact(res['acc_id'])
            return logged_account

    def display_contact(self, account_obj:object) -> None:
        for contact in account_obj.contacts_obj:
            print('-'*100)
            print(contact)

    def show_trash(self, acc_obj:object) ->None:
        data = self.select({'logic_delete':True,'acc_id':acc_obj.acc_id})
        print(100*"-")
        for key,val in data.items():
            print(f"{key}:{val}",end="  ")
        print(100*"-")

class ContactManager(ModelManager):
    def __init__(self, db_manager_obj):
        super().__init__(db_manager_obj, 'contacts', Accounts)

    def export_contact(self, parent_id:int) -> list:
        data = self.join_contact(parent_id)
        return [self.model_class(**contact) for contact in data]
    
class InboxManager(ModelManager):
    def __init__(self, db_manager_obj):
        super().__init__(db_manager_obj, 'inbox', Inbox)

    def recieve_message(self, acc_obj:object) -> None:
        messages = self.select({'logic_delete':False,'acc_id':acc_obj.acc_id})
        acc_obj.inbox = [self.model_class(**message) for message in messages]

    def delete_message(self , acc_obj):

        acc_obj.show_inbox()

        choose = int(input("choose what email do you want to delete"))
        message_obj=acc_obj.inbox[choose]

        query = """ DELETE FROM inbox WHERE message_id = %s"""
        param = (message_obj.message.id)
        with self.db_manager_obj as db :
            db.cursor.execute()

    def seen_massage(self):
        # culmn seen message    true   
        pass  

class SentManager(ModelManager):
    def __init__(self, db_manager_obj):
        super().__init__(db_manager_obj, 'sent', Sent)   

    def send_message(self ,origin_acc_obj, send_message , subject , to_email ):
        #fetch info from destination email 
        qury_to_fetch = """ SELECT * FROM  accounts WHERE email_address = %s"""
        param_to_fetch =(to_email,) 
        with self.db_manager_obj as db:
            db.cursor.execute(qury_to_fetch , param_to_fetch)
            result = db.cursor.fetchall()

            columns = [desc[0] for desc in db.cursor.description]
        dest_acc_obj = self.model_class(dict(zip(columns , result)))


        if dest_acc_obj :
            #todo transaction
            qury_to_send_origin = """ INSERT INTO sent values (%s,%s,%s,%s)"""
            params_to_send_origin =(origin_acc_obj.acc_id , to_email , subject , send_message)
            with self.db_manager_obj as db :
                db.cursor.execute(qury_to_send_origin , params_to_send_origin)


            qury_to_inbox_dest = """ INSERT INTO inbox values (%s,%s,%s,%s)"""
            params_to_inbox_dest =(dest_acc_obj.acc_id , origin_acc_obj.email_addres , subject , send_message)
            with self.db_manager_obj as db :
                db.cursor.execute(qury_to_inbox_dest , params_to_inbox_dest)


        else :
            raise ValueError ("this email is not found try correct email")


        

        # take mesage subject account_destination
        # exiting email fetch acc_destination
        # query for inseert message to inbox email destination seen false  and send email origin 
        # message to send compelete 
        

