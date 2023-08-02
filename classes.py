from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

class Data(ABC):
    '''hold the data that must be consistent across all items
    such as food or waste as an abstract class aka for methods only'''
    def __init__(self, day:int, FLW_type:str, kg:float, house: int, price:float, kcal:float):
        self.day = day
        self.type = FLW_type
        self.kg = kg
        self.house = house
        self.price = price
        self.kcal = kcal

    @abstractmethod
    def to_dict(self):
        # return a dictionary of the data
        #* This is the only data transferred by child classes
        #* This is the only data that is saved to the database
        #* All additional data is used only in that childs operations
        return {
            'day': self.day,
            'type': self.type,
            'kg': self.kg,
            'house': self.house,
            'price': self.price,
            'kcal': self.kcal
        }
    
    @abstractmethod
    def to_df(self, df:pd.DataFrame):
        return df.append(self.to_dict(), ignore_index=True)

class Food(Data):
    def __init__(self, day:int, FLW_type:str, kg:float, house: int, price:float, kcal:float):
        super().__init__(day, FLW_type, kg, house, price, kcal)
        
