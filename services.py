from models import CarModel, ClientModel, EmployeModel
import json

class CarService:
    def __init__(self):
        self.model = CarModel()
    
    def create(self, columns):
        return self.model.create(columns)
    
    def update(self, columns, conditions=''):
        return self.model.update(columns, conditions)

    def read_car_table(self, columns=[]):
        return self.model.read_car_table(columns)

class ClientService:
    def __init__(self):
        self.model = ClientModel()
        
    def create(self, columns:dict):
        return self.model.create(columns)

    def read(self, columns=[], conditions=''):
        return self.model.read(columns, conditions)
    
class EmployeService:
    def __init__(self):
        self.model = EmployeModel()
    
    def get_access(self, username, password):
        return self.model.get_access(username, password)

    def create(self, columns:dict):
        return self.model.create(columns)

