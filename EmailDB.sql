Create Database EmailDB

Create Table accounts
(   acc_id serial Primary Key,
    email_address varchar(100) Constraint UQ_accounts_email_address Unique,
    phone varchar(13) not null,
    picture varchar(100) null
);

Create Table contacts
(   parent_id int Constraint FK_contacts_parent_id References accounts(acc_id) not null,
    child_id int Constraint FK_contacts_child_id References accounts(acc_id) not null
);

-- Create Table messages
-- (
-- );

Create Table inbox
(   message_id serial Constraint PK_inbox_message_id Primary Key,
    acc_id int Constraint FK_inbox_acc_id References accounts(acc_id) not null,
    from_email_address varchar(100) not null,
    "subject" varchar(150) not null, 
    "message" text null,
    Seen bool Default False,    
    logic_delete bool Default False  
);


Create Table sent
(   message_id serial Constraint PK_sent_message_id Primary Key,
    acc_id int Constraint FK_sent_acc_id References accounts(acc_id) not null,
    to_email_address varchar(100) not null,
    "subject" varchar(150) not null, 
    "message" text null,    
    logic_delete bool Default False
);
------------------------------------------ Test
select * from accounts a where a.acc_id in (select child_id from contacts c inner join accounts acc 
                  on acc.acc_id = c.parent_id where c.parent_id=1)
				  
drop table sent;


insert Into accounts(email_address,phone) values ('reza@gmail.com','0939'),
														 ('arman@gmail.com','0991'),
														 ('zahra@gmail.com','0937'),
														 ('mehrzad@gmai.com','0912'),
														 ('majid@gmail.com','0911')
insert into contacts values (1,3),
							(1,4),
							(2,1),
							(2,3),
							(2,5)