import random 
import copy
import pandas as pd

class Store():
    '''An object that acts as a store for
    houses to shop from'''

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

class Food():
    def __init__(self, food_data:dict):
        self.type = food_data['Type']
        self.kg = food_data['kg']
        self.servings = food_data['Servings']
        self.expiration_time = random.randint(food_data['Expiration Min.'], food_data['Expiration Max.'])
        self.price_kg = food_data['Price']/self.kg
        self.inedible_parts = food_data['Inedible Parts']
        self.frozen = False
        self.serving_size = self.kg/self.servings
        self.kcal_kg = food_data['kcal_kg']
    def decay(self):
        if self.frozen == False:
            self.expiration_time -= 1

class CookedFood(Food):
    def __init__(self, composition: dict, kg: float, kcal_per_kg: float):
        self.composition = composition
        self.kg = kg
        self.kcal_kg = kcal_per_kg
        self.expiration_time = random.uniform(4, 11)
        self.frozen = False
        self.type = 'Cooked, Prepped, or Leftovers'
        self.inedible_parts = 0

class Person():
    def __init__(self):
        self.age = random.randint(18, 65)
        self.gender = random.randint(0, 1) #1 is female
        self.kcal = random.gauss(2000, 500) - 500*self.gender

    def old(self):
        self.age += 1
        if self.age <= 18:
            self.kcal += 50 + 10*self.gender
        elif self.age > 30 and self.age <= 40:
            self.kcal -= 50 + 10*self.gender

class Child(Person):
    def __init__(self, parent: Person):
        self.age = random.randint(1, 18)
        self.kcal = random.gauss(1200, 200) + self.age*50
        self.gender = random.randint(0,1) #1 is female
        self.parent = parent

class House():
    def __init__(self, store: Store, id: int):
        self.people = []
        self.kcal = 0
        self.generate_people()
        # create a pantry that is a list that can only store Food objects
        self.pantry = [] # stores ingredients
        self.fridge = [] # stores ready-to-eat food
        self.stomach = [] # stores food that has been eaten
        self.store = store
        self.id = id
        self.waste_bin = []
        self.bought_food = []
        self.shopping_frequency = random.randint(1, 7)
        self.time_available_for_meal_prep = [2, 0.5, 0.5, 0.5, 0.5, 1, 2]
        self.budget = 20

    def generate_people(self):
        for i in range(random.randint(1, 5)):
            p = Person()
            self.people.append(p)
            self.kcal += p.kcal

    def shop(self):
        basket = self.fill_basket()
        for item in basket:
            self.bought_food.append(item)
            if item.type == 'Store-Prepared Items':
                self.fridge.append(item)
            else:
                self.pantry.append(item)

    def fill_basket(self):
        basket_df = self.store.shelves.sample(n=2*self.shopping_frequency)
        basket = []
        for i in range(len(basket_df)):
            food_data = basket_df.iloc[i]
            basket.append(Food(food_data))
        return basket

    def cook(self):
        ingredients = self.get_ingredients()
        kg = 0
        composition = {
            'Meat & Fish': 0,
            'Dairy & Eggs':0,
            'Fruits & Vegetables':0,
            'Dry Foods & Baked Goods':0,
            'Snacks, Condiments, Liquids, Oils, Grease, & Other':0
        }
        kcal = 0
        for ingredient in ingredients:
            self.prep(ingredient)
            kg += ingredient.kg
            kcal += ingredient.kcal_kg*ingredient.kg
            composition[ingredient.type] += ingredient.kg
        for key, value in composition.items():
            if value > 0:
                value/=kg # make a percentage
        self.fridge.append(CookedFood(composition, kg, kcal/kg))

    def prep(self, food: Food):
        if food.inedible_parts == 0:
            return
        else:
            inedible = copy.deepcopy(food)
            inedible.kg = food.kg*food.inedible_parts
            food.kg -= inedible.kg
            inedible.inedible_parts = 1
            self.waste(inedible)

    def waste(self, food: Food ):
        if food.inedible_parts == 1:
            self.waste_bin.append(Waste({
                'kg': food.kg,
                'Type': food.type,
                'House': self.id,
                'ed_status': 'Inedible'
            }))
        elif food.type == 'Store-Prepared Items':
            self.waste_bin.append(Waste({
                'kg': food.kg,
                'Type': food.type,
                'House': self.id,
                'ed_status': 'Ed-Cooked'
            }))
        elif food.type == 'Cooked, Prepped, or Leftovers':
            for key, value in c_food.composition.items():
                if value > 0:
                    self.waste_bin.append(Waste({
                        'kg': value*c_food.kg,
                        'Type': key,
                        'House': self.id,
                        'ed_status': 'Ed-Cooked'
                    }))
        else:
            self.waste_bin.append(Waste({
                'kg': food.kg,
                'Type': food.type,
                'House': self.id,
                'ed_status': 'Ed-Uncooked'
            }))

    def get_ingredients(self):
        ingredients = []
        i = 1
        while i <= random.randint(3, 5):
            if len(self.pantry) == 0:
                self.shop()
            else:
                random.shuffle(self.pantry)
                for item in self.pantry:
                    if item.expiration_time <= 0:
                        self.waste(item)
                        self.pantry.remove(item)
                    else:
                        self.pantry.remove(item)
                        ingredients.append(item)
                        i += 1
        return ingredients

    def eat(self, food: Food, kcal: int):
        if food.type != 'Cooked, Prepped, or Leftovers':
            if food.kg*food.kcal_kg > kcal:
                eaten = copy.deepcopy(food)
                food.kg -= kcal/food.kcal_kg
                eaten.kg = kcal/food.kcal_kg
            else:
                eaten = food
                self.fridge.remove(food)
                del food
            self.stomach.append(Eaten({
                'kg': eaten.kg,
                'Type': eaten.type,
                'House': self.id,
                'Exp': eaten.expiration_time
            }))
        else:
            if food.kg*food.kcal_kg > kcal:
                eaten_kg = kcal/food.kcal_kg
                food.kg -= eaten_kg
                for key, value in food.composition.items():
                    if value > 0:
                        self.stomach.append(Eaten({
                            'kg': value*eaten_kg,
                            'Type': key,
                            'House': self.id,
                            'Exp': food.expiration_time
                        }))
            else:
                self.fridge.remove(food)
                for key, value in food.composition.items():
                    if value > 0:
                        self.stomach.append(Eaten({
                            'kg': value*food.kg,
                            'Type': key,
                            'House': self.id,
                            'Exp': food.expiration_time
                        }))

    def choose_meal(self):
        if len(self.fridge) == 0:
            self.out_or_cook()
        else:
            kcal = self.kcal
            for food in reversed(self.fridge):
                if food.expiration_time <= 0:
                    self.waste(food)
                    self.fridge.remove(food)
                elif kcal <= 0:
                    return
                elif food.type == 'Store-Prepared Items':
                    self.eat(food, kcal)
                    kcal -= food.kcal_kg*food.kg
                else:
                    continue
            for food in reversed(self.fridge):
                if food.expiration_time <= 0:
                    self.waste(food)
                    self.fridge.remove(food)
                elif kcal <= 0:
                    return
                elif food.type == 'Cooked, Prepped, or Leftovers':
                    self.eat(food, kcal)
                    kcal -= food.kcal_kg*food.kg
                else:
                    continue

    def out_or_cook(self):
        random.choice([self.cook, self.buy_out])()
        self.choose_meal()

    def buy_out(self):
        food = Food(self.store.food_data(food_type='Store-Prepared Items', servings= len(self.people)))
        self.fridge.append(food)

    def do_a_day(self, day: int):
        if day % self.shopping_frequency == 0:
            self.cook()
        self.choose_meal()
class Waste():
    def __init__(self, waste_data: dict):
        self.kg = waste_data['kg']
        self.type = waste_data['Type']
        self.house = waste_data['House']
        self.ed_status = waste_data['ed_status']

class Eaten():
    def __init__(self, eaten_data: dict):
        self.kg = eaten_data['kg']
        self.type = eaten_data['Type']
        self.house = eaten_data['House']
        self.exp = eaten_data['Exp']

class Neighborhood():
    def __init__(self, n_houses= 10):
        self.store = Store()
        self.houses = []
        for i in range(n_houses):
            self.houses.append(House(id=i, store=self.store))
        self.wasted_food = pd.DataFrame(columns=[
            'Type',
            'kg',
            'Ed-Status',
            'House',
            'Day Wasted'
        ])
        self.eaten_food = pd.DataFrame(columns=[
            'Type',
            'kg',
            'House',
            'Day Eaten'
        ])
        self.bought_food = pd.DataFrame(columns=[
            'Type',
            'kg',
            'House',
            'Day Bought'
        ])

    def run(self, days=56):
        for day in range(days):
            for house in self.houses:
                house.do_a_day(day)
            self.collect_data(day=day)

    def collect_data(self, day: int):
        for house in self.houses:
            for waste in house.waste_bin:
                self.wasted_food = self.wasted_food._append({
                    'Type': waste.type,
                    'kg': waste.kg,
                    'Ed-Status': waste.ed_status,
                    'House': house.id,
                    'Day Wasted': day
                }, ignore_index=True)
            for eaten in house.stomach:
                self.eaten_food = self.eaten_food._append({
                    'Type': eaten.type,
                    'kg': eaten.kg,
                    'House': house.id,
                    'Day Eaten': day
                }, ignore_index=True)
            for bought in house.bought_food:
                self.bought_food = self.bought_food._append({
                    'Type': bought.type,
                    'kg': bought.kg,
                    'House': house.id,
                    'Day Bought': day
                }, ignore_index=True)

    def data_to_csv(self):
        self.wasted_food.to_csv('outputs/wasted_food_1.csv')
        self.eaten_food.to_csv('outputs/eaten_food_1.csv')
        self.bought_food.to_csv('outputs/bought_food_1.csv')
