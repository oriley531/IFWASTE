from classes import House, Food, CookedFood, Store, Waste
import pandas as pd
def init(num_of_houses=100):
    # Store data for tidiverse later
    global bought_food
    bought_food = pd.DataFrame(columns=[
        'Type', 
        'Servings', 
        'Expiration time',
        'Price',
        'kg',
        'kcal_kg',
        'Inedible Parts',
        'Day Bought',
        'House'
    ])
    global eaten_food
    eaten_food = pd.DataFrame(columns=[
        'Type',
        'kg',
        'kcal',
        'expiration time',
        'House',
        'Day Eaten'
    ])
    global wasted_food
    wasted_food = pd.DataFrame(columns=[
        'Type',
        'kg',
        'Ed-Status',
        'House',
        'Day Wasted'
    ])
    global still_owned
    still_owned = pd.DataFrame(columns=[
        'Type',
        'kg',
        'kcal',
        'House'
        ])
    #----------------------------
    # Create a store and all of the houses
    store = Store()
    global houses
    houses = []
    for i in range(num_of_houses):
        house = House(id=i, store= store)
        houses.append(house)
        house.shop()
    #----------------------------

def run(days=54):
    for day in range(days):
        for house in houses:
            house.do_a_day(day=day)
            collect_data(day=day, house= house)

def collect_data(day:int, house:House):
    # food bought
    for food in house.store.inventory:
        bought_food.loc[len(bought_food)] = {
        'Type': food.type, 
        'Servings': food.servings, 
        'Expiration time': food.expiration_time,
        'Price': food.price_kg*food.kg,
        'kg':food.kg,
        'kcal_kg': food.kcal_kg,
        'Inedible Parts': food.inedible_parts,
        'Day Bought': day,
        'House': house.id
        }
        house.store.inventory.remove(food)
        del food
    for waste in house.waste_bin:
        wasted_food.loc[len(wasted_food)] = {
        'Type':waste.type,
        #'Part of Home-Cooked Meal', - to be implemented
        'kg': waste.kg,
        #'kcal', - to be implemented ln 
        #'price', - to be implemented
        'House': house.id,
        'Day Wasted': day,
        'Ed-Status': waste.ed_status
        }
        house.waste_bin.remove(waste)
        del waste
    for food in house.stomach:
        eaten_food.loc[len(eaten_food)] = {
        'Type':food.type,
        #'Part of Home-Cooked Meal',
        'kg': food.kg,
        'kcal':food.kcal_kg*food.kg,
        #'price':food.price_kg*food.kg, - not yet implemented
        'expiration time':food.expiration_time,
        'House':house.id,
        'Day Eaten':day
        }
        house.stomach.remove(food)
        del food

def collect_still_owned(house:House):
    for house in houses:
        for food in house.pantry:
            still_owned._append_({
                'Type':food.type,
                'kg':food.kg,
                'kcal':food.kcal_kg*food.kg,
                'House':house.id
            })
        for food in house.fridge:
            still_owned._append_({
                'Type':food.type,
                'kg':food.kg,
                'kcal':food.kcal_kg*food.kg,
                'House':house.id
            })

def data_to_csv(trial=1):
    bought_food.to_csv(f'outputs/bought_food_{trial}.csv')
    eaten_food.to_csv(f'outputs/eaten_food_{trial}.csv')
    wasted_food.to_csv(f'outputs/wasted_food_{trial}.csv')
    still_owned.to_csv(f'outputs/still_owned_{trial}.csv')