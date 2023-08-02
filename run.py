from classes import House, Food, CookedFood, Store, Waste, Eaten, Person, Neighborhood

# Create a neighborhood
neighborhood = Neighborhood(n_houses=2)

# run it
neighborhood.run()

# save data to csv
neighborhood.data_to_csv()