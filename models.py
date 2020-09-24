'''
Car
- ID
- Plate
- Model
- Color
- is_parked
- owner (foreign key from Client username)

Client
- ID
- Name
- username
- email

Employe
- ID
- name
- username
- password
- email
'''

import sqlite3

class Schema():
    def __init__(self):
        self.db = DataBase()
        self.create_client_table()
        self.create_car_table()
        self.create_employe_table()

    def create_client_table(self):
        columns = {
            'id': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
            'name': 'TEXT NOT NULL',
            'username': 'TEXT NOT NULL UNIQUE',
            'email': 'TEXT NOT NULL'
        }
        self.db.create_table('Client', columns)
    
    def create_car_table(self):
        columns = {
            'id': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
            'plate': 'TEXT NOT NULL UNIQUE',
            'model': 'TEXT NOT NULL',
            'color': 'TEXT NOT NULL',
            'owner': 'TEXT NOT NULL',
            'is_parked': 'BOOLEAN NOT NULL DEFAULT 0',
            'FOREIGN KEY(owner)': 'REFERENCES Client(username)'
        }
        self.db.create_table('Car', columns)
    
    def create_employe_table(self):
        columns = {
            'id': 'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
            'name': 'TEXT NOT NULL',
            'username': 'TEXT NOT NULL UNIQUE',
            'password': 'TEXT NOT NULL', 
            'email': 'TEXT NOT NULL'
        }
        self.db.create_table('Employe', columns)

class DataBase:

    ##DataBase Operations Required
    def create_table(self, table_name, columns = {}):
        conn = sqlite3.connect('Parking.db')
        query = f"CREATE TABLE {table_name}("
        for key, value in columns.items():
            query += f"{key} {value}, "
        query = query.strip(', ')
        query += ');'
        try:
            conn.execute(query)
            conn.commit()
            conn.close()
            return True
        except sqlite3.OperationalError:
            conn.close()
            return False

    ##Table Operations Required
    '''
    This method will be called as part of superclass
    at the DataBase's tables
    '''
    def create(self, table_name, columns:dict):
        conn = sqlite3.connect('Parking.db')
        query = f'INSERT INTO {table_name} ('
        for key in columns:
            query += f'{key}, '
        query = query.strip(', ')
        query += ') VALUES ('
        for value in columns.values():
            if isinstance(value, str):
                query += f"'{value}', "
            else:
                query += f"{value}, "
        query = query.strip(', ')
        query += ');'
        try:
            conn.execute(query)
            conn.commit()
            conn.close()
            return True
        except:
            conn.close()
            return False

    def read(self, table_name, columns=[], conditions=''):
        '''
        if a empty list is given, will return SELECT *
        '''
        conn = sqlite3.connect('Parking.db')
        query = ''
        if columns != []:
            query += f'SELECT '
            for att in columns:
                query += f'{att}, '
            query = query.strip(', ')
            query += f' FROM {table_name}'
        else:
            query += f'SELECT * FROM {table_name}'
        if conditions != '':
            query += ' WHERE ' + conditions
        query += ';'
        try:
            table = conn.execute(query).fetchall()
            conn.close()
            return table
        except sqlite3.OperationalError:
            conn.close()
            return 0

    def update(self, table_name, columns, conditions = ''):
        conn = sqlite3.connect('Parking.db')
        query = ''
        if columns != {}:
            query += f"UPDATE {table_name} SET "
            for key, value in columns.items():
                if isinstance(value, str):
                    query += f"{key} = '{value}', "
                else:
                    query += f"{key} = {value}, "
            query = query.strip(', ')
            if conditions != '':
                query += f' WHERE {conditions}'
            query += ';'
        try:
            nrows = conn.execute(query).rowcount
            conn.commit()
            conn.close()
            if nrows == 1:
                return True
            else:
                return False #do not exist or is duplicated
        except sqlite3.OperationalError:
            return False #did not worked
    


class CarModel(DataBase):
   
    def create(self, columns):
        table_name='Car'
        return super().create(table_name, columns)

    def read(self, columns=[], conditions=''):
        tables_name = 'Car'
        return super().read(table_name, columns, conditions)

    def update(self, columns, conditions=''):
        table_name = 'Car'
        return super().update(table_name, columns, conditions)

    def read_car_table(self, columns=[]):
        conn = sqlite3.connect('Parking.db')
        if columns != []:
            query = f'SELECT '
            for column_name in columns:
                query += f'{column_name}, '
            query = query.strip(', ')
            query += ' FROM Car '
        else:
            query = f'SELECT * FROM Car '
        query += 'JOIN Client ON Client.username = owner WHERE Car.is_parked = 1;'
        try:
            table = conn.execute(query).fetchall()
            conn.close()
            return table
        except sqlite3.OperationalError:
            conn.close()
            return False #atenção 
        
class ClientModel(DataBase):

    def create(self, columns:dict):
        table_name = 'Client'
        return super().create(table_name, columns)

    def read(self, columns=[], conditions=''):
        table_name = 'Client'
        return super().read(table_name, columns, conditions)
        
class EmployeModel(DataBase):

    def get_access(self, username, password):
        table_name = 'Employe'
        columns = ['username', 'password']
        conditions = f"username = '{username}' AND password = '{password}'"
        table = super().read(table_name, columns, conditions)
        if len(table) != 0:
            if len(table) == 1:
                return True
            else:
                return False #duplicated
        else:
            return False #do not exist

    def create(self, columns:dict):
        table_name = 'Employe'
        return super().create(table_name, columns)

