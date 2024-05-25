import psycopg2

class DataBaseConnection:
    CONFIG={
         'dbname':'emaildb',
         'host':'localhost',
         'port':5648,
         'user':'postgres',
         'password':'1380ACreZA46'
    }
    def __init__(self) -> None:
        self.connection_obj=None
        self.cursor=None

    def __enter__(self) -> object:
        """ returns the connection object """
        self.create_connection()
        self.create_cursor()
        return self

    def __exit__(self,exc_type,exc_value,exc_traceback):
        if exc_type or exc_value or exc_traceback:
            self.connection_obj.rollback()
            print(exc_type,exc_value,exc_traceback)
        else:
          self.connection_obj.commit()
          self.close_cursor()

    def create_connection(self) -> None:
        """ Create a connection """
        self.connection_obj=psycopg2.connect(**self.CONFIG)
    
    def create_cursor(self) -> None:
        """ Create a cursor """
        self.cursor=self.connection_obj.cursor()
    
    def close_cursor(self) -> None:
        """ Close the instantiated cursor """
        self.cursor.close()

    def rollback(self) -> None:
        """" Rollback the operation """
        self.connection_obj.rollback()

    def commit(self) -> None:       
        """ Commite the operation """ 
        self.connection_obj.commit()

    def close_connection(self) -> None:
        """ colse the instantiated connection """
        self.connection_obj.close()

    def close(self) -> None:
        """ close the instantiated cursor and connection """
        self.cursor.close()
        self.connection_obj.close()