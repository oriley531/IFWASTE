import random 
import copy
import pandas as pd

class Store():
    def __init__(self):
        self.shelves = pd.DataFrame(columns= [
            'Type', 
            'Servings', 
            'Expiration Min.', 
            'Expiration Max.',
            'Price',
            'kg',
            'kcal_kg',
            'Inedible Parts'
            ])
        self.stock_shelves()
        self.inventory = []
    
    def stock_shelves(self):
        food_types = [
            "Meat & Fish", 
            "Dairy & Eggs", 
            "Fruits & Vegetables", 
            "Dry Foods & Baked Goods", 
            "Snacks, Condiments, Liquids, Oils, Grease, & Other", 
            'Store-Prepared Items' 
            ]
        for food_type in food_types:
            self.shelves = self.shelves._append(self.food_data(food_type=food_type, servings=6), ignore_index=True)
            self.shelves = self.shelves._append(self.food_data(food_type=food_type, servings=12), ignore_index=True)
            self.shelves = self.shelves._append(self.food_data(food_type=food_type, servings=20), ignore_index=True)

    def food_data(self, food_type: str, servings:int):
        ''' RGO - 
        Could make price smaller per kg for things with more 
        servings to improve accuracy to a real market'''
        inedible_parts = 0
        if food_type == 'Meat & Fish':
            exp_min = 4 # days 
            exp_max = 11 # days
            kg = 0.09*servings # assume 90g meat per serving
            price = 6*2.2*kg # assume $6/lb to total for kg
            kcal_kg = 2240 # assume 2240 kcal per kg of meat
            inedible_parts = 0.1
        elif food_type == 'Dairy & Eggs':
            exp_min = 7 # days 
            exp_max = 28 # days
            kg = 0.109*servings # assume 109g dairy&egg per serving
            price = 6*16/27*2.2*kg # assume $6/27oz to total for kg
            kcal_kg = 1810 # assume 1810 kcal per kg of dairy&eggs
            inedible_parts = 0.1
        elif food_type == 'Fruits & Vegetables':
            exp_min = 5 # days 
            exp_max = 15 # days
            kg = 0.116*servings # assume 116g f,v per serving
            price = 3.62*2.2*kg # assume $3.62/lb to total for kg
            kcal_kg = 790 # assume 790 kcal per kg of f,v
        elif food_type == 'Dry Foods & Baked Goods':
            exp_min = 7 # days 
            exp_max = 8*7 # days
            kg = 0.065*servings # assume 65g per serving
            price = 1.5*2.2*kg # assume $1.50/lb to total for kg
            kcal_kg = 3360 # assume 3360 kcal per kg
        elif food_type == 'Snacks, Condiments, Liquids, Oils, Grease, & Other':
            exp_min = 7 # days 
            exp_max = 8*7 # days
            kg = 0.095*servings # assume 95g per serving
            price = 3.3*2.2*kg # assume $3.30/lb to total for kg
            kcal_kg = 2790 # assume 2790 kcal per kg
        elif food_type == 'Store-Prepared Items':
            exp_min = 2 # days 
            exp_max = 7 # days
            kg = 0.095*servings # assume 95g per serving
            price = 0.33*16*2.2*kg # assume $0.33/oz to total for kg
            kcal_kg = 2790 # assume 2790 kcal per kg
        else:
            raise ValueError(f"{food_type}is not a listed Food Type")
        new_food = {
            'Type': food_type, 
            'Servings': servings, 
            'Expiration Min.': exp_min, 
            'Expiration Max.': exp_max,
            'Price': price,
            'kg': kg,
            'kcal_kg': kcal_kg,
            'Inedible Parts': inedible_parts
            }
        return new_food
class House():
    def __init__(self):
        pass
    def do_a_day(self):
        pass
    def cook(self):
        pass
    def prep(self):
        pass
    def choose_meal(self):
        pass
    def eat(self):
        pass
    def get_recipe(self) -> dict:
        # return a dictionary of ideal ingredients and servings
        pass
    def prep_ingredients(self) -> list:
        pass
    def shop(self):
        pass
    def waste(self):
        pass

class Food():
    def __init__(self, food_data:dict):
        self.type = food_data['Type']
        self.kg = food_data['kg']
        self.servings = food_data['Servings']
        self.exp_time = random.randint(food_data['Expiration Min.'], food_data['Expiration Max.'])
        self.price_kg = food_data['Price']/self.kg
        self.inedible_parts = food_data['Inedible Parts']
        self.frozen = False
        self.serving_size = self.kg/self.servings
        self.kcal_kg = food_data['kcal_kg']
    def decay(self):
        if self.frozen == False:
            self.exp_time -= 1
    def split(self) -> (Food, Waste):
        pass
class CookedFood(Food):
    def __init__(self, ingredients:list):
        pass
class Waste():
    def __init__(self, food:Food):
        if not isinstance(CookedFood):
            self.type = food.type
            self.kg = food.kg*food.inedible_parts
            self.servings = food.servings*food.inedible_parts
            self.exp_time = food.exp_time
            self.price = food.price_kg*food.kg
            self.serving_size = self.kg/self.servings
            self.kcal = food.kcal_kg*food.kg
        else:
            for ingredient in food.ingredients:
                self.type = ingredient.type
                self.kg = ingredient.kg*ingredient.inedible_parts
                self.servings = ingredient.servings*ingredient.inedible_parts
                self.exp_time = ingredient.exp_time
                self.price = ingredient.price_kg*ingredient.kg
                self.serving_size = self.kg/self.servings
                self.kcal = ingredient.kcal_kg*ingredient.kg

class Neighborhood():
    def __init__(self, num_houses= 10):
        houses = []
        for i in range(num_houses):
            houses.append(House())
    def run(self, days= 365):
        for i in range(days):
            for house in houses:
                house.do_a_day()
    def collect_data(self):
        pass
    def get_storage(self):
        pass
    def data_to_csv(self):
        pass