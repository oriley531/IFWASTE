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
    def throw_away(self):
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
    def portion(self, servings: int = None, kcal: float = None):
        if servings == None and kcal == None:
            raise ValueError('Must specify either servings or kcal')
        elif servings != None and kcal != None:
            raise ValueError('Must specify either servings or kcal, not both')
        elif servings != None:
            if servings > self.servings:
                servings = self.servings
            new_food = Food({
                'Type': self.type,
                'kg': servings*self.serving_size,
                'Expiration Min.': self.exp_time,
                'Expiration Max.': self.exp_time,
                'Price': self.price_kg*servings*self.serving_size,
                'Servings': servings,
                'kcal_kg': self.kcal_kg,
                'Inedible Parts': self.inedible_parts
            })
            self.kg -= new_food.kg
            self.servings -= new_food.servings
            return new_food
        elif kcal != None:
            if kcal > self.kcal_kg*self.kg:
                kcal = self.kcal_kg*self.kg
            new_food = Food({
                'Type': self.type,
                'kg': kcal/self.kcal_kg,
                'Expiration Min.': self.exp_time,
                'Expiration Max.': self.exp_time,
                'Price': self.price_kg*kcal/self.kcal_kg,
                'Servings': (kcal/self.kcal_kg)/self.serving_size,
                'kcal_kg': self.kcal_kg,
                'Inedible Parts': self.inedible_parts
            })
            self.kg -= new_food.kg
            self.servings -= new_food.servings
            return new_food
    def throw(self):
        # return a list of waste
        return [Waste(self)]
class CookedFood(Food):
    def __init__(self, ingredients:list):
        self.ingredients = ingredients
        self.type = 'Cooked, Prepped, Leftovers'
        self.kg = 0
        price = 0
        kcal = 0
        self.scraps = []
        for ingredient in ingredients:
            if ingredient.inedible_parts > 0 : 
                self.scraps.append(Inedible(ingredient))
            self.kg += ingredient.kg
            price += ingredient.price_kg*ingredient.kg
            kcal += ingredient.kcal_kg*ingredient.kg
        self.price_kg = price/self.kg
        self.kcal_kg = kcal/self.kg
    def portion(self, kcal: float ):
        new_ingredients = []
        if kcal > self.kcal_kg*self.kg:
            kcal = self.kcal_kg*self.kg
            for ingredient in self.ingredients:
                new_food = ingredient.portion(kcal=ingredient.kcal_kg*ingredient.kg) # take all of the ingredient
                self.ingredients.remove(ingredient)
                new_ingredients.append(new_food)
        else:
            # ratio to take the proper amount from each ingredient
            kcal_ratio = kcal/(self.kcal_kg*self.kg)
            for ingredient in self.ingredients:
                new_food = ingredient.portion(kcal=ingredient.kcal_kg*ingredient.kg*kcal_ratio) # take the proper amount of each ingredient
                new_ingredients.append(new_food)
        new_cfood = CookedFood(ingredients=new_ingredients)
        self.kg -= new_food.kg
        return new_cfood
    def throw(self):
        # return a list of waste
        waste_list = []
        for ingredient in self.ingredients:
            waste_list.append(Waste(food=ingredient, status='Cooked'))
        return waste_list
class Waste():
    def __init__(self, food:Food, status:str = None):
        self.type = food.type
        self.kg = food.kg
        self.servings = food.servings
        self.price = food.price_kg*food.kg
        self.kcal = food.kcal_kg*food.kg
        if status == None:
            self.status = 'Cooked' if food.type == 'Store-Prepared Items' else'Unprepared'
        else:
            self.status = status
class Inedible(Waste):
    def __init__(self, food:Food):
        # creates a waste from the inedible parts of a food
        self.type = food.type
        self.kg = food.kg*food.inedible_parts
        self.servings = 0
        self.price = food.price_kg*food.kg
        self.kcal = 0
        self.status = 'Inedible'
        # update the food
        food.kg -= self.kg
        food.serving_size *= (1-food.inedible_parts)
        food.kcal_kg /= (1-food.inedible_parts) # assume inedible parts have no calories
        print(f'Ined of {food.type} is {self.kg} kg')

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

# a function that tests all of the methods in food and cookedfood for mass conservation
def test_mass_conservation():
    # make some food and cookedfood
    food1 = Food({
        'Type': 'Store-Prepared Items',
        'kg': 0.12*6,
        'Expiration Min.': 4,
        'Expiration Max.': 6,
        'Price': 10.99,
        'Servings': 6,
        'kcal_kg': 2790,
        'Inedible Parts': 0
    })
    food2 = Food({
        'Type': 'Meat & Fish',
        'kg': 0.09*6,
        'Expiration Min.': 4,
        'Expiration Max.': 6,
        'Price': 10.99,
        'Servings': 6,
        'kcal_kg': 2240,
        'Inedible Parts': 0.1
    })
    print(f'food1 - {food1.kg}')
    print(f'food2 - {food2.kg}')
    food_portion = food1.portion(servings=2)
    print(f'food1 after 2 servings taken - {food1.kg}')
    print(f'portion taken - {food_portion.kg}')
    cfood = CookedFood([food1, food2])
    print(f'cfood - {cfood.kg}')
    for scrap in cfood.scraps:
        print(f'{scrap.type} - {scrap.kg}')
    # test the portion method
    cfood_portion = cfood.portion(kcal=224)
    print(f'cfood left - {cfood.kg}')
    print(f'cfood taken - {cfood_portion.kg}')
    waste = cfood_portion.throw()
    for scrap in waste:
        print(f'waste - {scrap.type} - {scrap.kg}')


test_mass_conservation()